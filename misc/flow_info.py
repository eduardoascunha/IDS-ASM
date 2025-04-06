from scapy.all import sniff, IP, TCP, UDP
 import math
 from collections import defaultdict
 import pandas as pd
 import time
 import sys
 
 class FlowInfo:
     def __init__(self):
         self._flows = {}
         self._flow_data = []
     
     def get_flows(self) -> dict:
         return self._flows
    
     def set_flows(self, value: dict):
         self._flows = value
 
     def get_flow_data(self) -> list:
         return self._flow_data
 
     def set_flow_data(self, value: list):
         self._flow_data = value
     
     def wipe_flows(self):
         self._flows = {}
         self._flow_data = []
     
     def __repr__(self):
         return f"FlowInfo(flows_count={len(self._flows)}, flow_data_count={len(self._flow_data)})"
 
     @staticmethod
     def safe_int_convert(value):
         """Safely convert a value to int, handling infinity and NaN cases"""
         if isinstance(value, (int, float)):
             if math.isinf(value):
                 return sys.maxsize if value > 0 else -sys.maxsize
             elif math.isnan(value):
                 return 0
             return int(value)
         return 0
 
     @staticmethod
     def get_flow_key(src_ip, dst_ip, src_port, dst_port, proto):
         src_port = src_port or 0
         dst_port = dst_port or 0
         if src_ip < dst_ip:
             key_ip = (src_ip, dst_ip)
             port_order = True
         elif src_ip > dst_ip:
             key_ip = (dst_ip, src_ip)
             port_order = False
         else:
             if src_port <= dst_port:
                 key_ip = (src_ip, dst_ip)
                 port_order = True
             else:
                 key_ip = (dst_ip, src_ip)
                 port_order = False
 
         if port_order:
             key_port = (src_port, dst_port)
         else:
             key_port = (dst_port, src_port)
 
         return (key_ip[0], key_ip[1], key_port[0], key_port[1], proto)
 
     @staticmethod
     def update_stats(stats, value):
         stats['sum'] += value
         stats['sum_sq'] += value ** 2
         stats['min'] = min(stats['min'], value)
         stats['max'] = max(stats['max'], value)
         stats['count'] += 1
 
     @staticmethod
     def compute_stats(stats):
         if stats['count'] == 0:
             return (0.0, 0.0, 0.0)
         mean = stats['sum'] / stats['count']
         variance = (stats['sum_sq'] / stats['count']) - (mean ** 2)
         std = math.sqrt(variance) if variance >= 0 else 0.0
         return (mean, std, variance)
 
     def create_flow_entry(self, flow):
         duration = flow['end_time'] - flow['start_time']
         total_bytes = flow['forward_bytes'] + flow['backward_bytes']
         total_packets = flow['forward_packets'] + flow['backward_packets']
         
         # Compute statistics
         fwd_length_mean, fwd_length_std, fwd_length_var = self.compute_stats(flow['forward_length'])
         fwd_iat_mean, fwd_iat_std, fwd_iat_var = self.compute_stats(flow['forward_iat'])
         bwd_length_mean, bwd_length_std, bwd_length_var = self.compute_stats(flow['backward_length'])
         bwd_iat_mean, bwd_iat_std, bwd_iat_var = self.compute_stats(flow['backward_iat'])
         flow_iat_mean, flow_iat_std, flow_iat_var = self.compute_stats(flow['flow_iat'])
         
         # Packet length stats
         min_pkt_len = min(flow['forward_length']['min'], flow['backward_length']['min'])
         max_pkt_len = max(flow['forward_length']['max'], flow['backward_length']['max'])
         avg_pkt_size = total_bytes / total_packets if total_packets > 0 else 0
         
         # Create the flow entry dictionary with all required columns
         entry = {
             # Basic flow information
             'Destination Port': self.safe_int_convert(flow['original_dst_port']),
             'Flow Duration': self.safe_int_convert(duration),
             'Total Fwd Packets': self.safe_int_convert(flow['forward_packets']),
             'Total Backward Packets': self.safe_int_convert(flow['backward_packets']),
             'Total Length of Fwd Packets': self.safe_int_convert(flow['forward_bytes']),
             'Total Length of Bwd Packets': self.safe_int_convert(flow['backward_bytes']),
             
             # Forward packet length statistics
             'Fwd Packet Length Max': self.safe_int_convert(flow['forward_length']['max']),
             'Fwd Packet Length Min': self.safe_int_convert(flow['forward_length']['min']),
             'Fwd Packet Length Mean': fwd_length_mean,
             'Fwd Packet Length Std': fwd_length_std,
             
             # Backward packet length statistics
             'Bwd Packet Length Max': self.safe_int_convert(flow['backward_length']['max']),
             'Bwd Packet Length Min': self.safe_int_convert(flow['backward_length']['min']),
             'Bwd Packet Length Mean': bwd_length_mean,
             'Bwd Packet Length Std': bwd_length_std,
             
             # Flow rate statistics
             'Flow Bytes/s': total_bytes / duration if duration > 0 else 0,
             'Flow Packets/s': total_packets / duration if duration > 0 else 0,
             
             # Flow IAT (Inter Arrival Time) statistics
             'Flow IAT Mean': flow_iat_mean,
             'Flow IAT Std': flow_iat_std,
             'Flow IAT Max': self.safe_int_convert(flow['flow_iat']['max']),
             'Flow IAT Min': self.safe_int_convert(flow['flow_iat']['min']),
             
             # Forward IAT statistics
             'Fwd IAT Total': self.safe_int_convert(flow['forward_iat']['sum']),
             'Fwd IAT Mean': fwd_iat_mean,
             'Fwd IAT Std': fwd_iat_std,
             'Fwd IAT Max': self.safe_int_convert(flow['forward_iat']['max']),
             'Fwd IAT Min': self.safe_int_convert(flow['forward_iat']['min']),
             
             # Backward IAT statistics
             'Bwd IAT Total': self.safe_int_convert(flow['backward_iat']['sum']),
             'Bwd IAT Mean': bwd_iat_mean,
             'Bwd IAT Std': bwd_iat_std,
             'Bwd IAT Max': self.safe_int_convert(flow['backward_iat']['max']),
             'Bwd IAT Min': self.safe_int_convert(flow['backward_iat']['min']),
             
             # TCP Flags
             'Fwd PSH Flags': self.safe_int_convert(flow['forward_tcp_flags']['PSH']),
             'Bwd PSH Flags': self.safe_int_convert(flow['backward_tcp_flags']['PSH']),
             'Fwd URG Flags': self.safe_int_convert(flow['forward_tcp_flags']['URG']),
             'Bwd URG Flags': self.safe_int_convert(flow['backward_tcp_flags']['URG']),
             
             # Header lengths
             'Fwd Header Length': self.safe_int_convert(flow['fwd_header_length']),
             'Bwd Header Length': self.safe_int_convert(flow['bwd_header_length']),
             
             # Packet rate statistics
             'Fwd Packets/s': flow['forward_packets'] / duration if duration > 0 else 0,
             'Bwd Packets/s': flow['backward_packets'] / duration if duration > 0 else 0,
             
             # Packet length statistics
             'Min Packet Length': self.safe_int_convert(min_pkt_len),
             'Max Packet Length': self.safe_int_convert(max_pkt_len),
             'Packet Length Mean': (fwd_length_mean * flow['forward_packets'] + bwd_length_mean * flow['backward_packets']) / total_packets if total_packets > 0 else 0,
             'Packet Length Std': math.sqrt(
                 (fwd_length_std**2 * flow['forward_packets'] + bwd_length_std**2 * flow['backward_packets']) / total_packets
             ) if total_packets > 0 else 0,
             'Packet Length Variance': (
                 fwd_length_var * flow['forward_packets'] + bwd_length_var * flow['backward_packets']
             ) / total_packets if total_packets > 0 else 0,
             
             # TCP Flag counts
             'FIN Flag Count': self.safe_int_convert(flow['flow_tcp_flags']['FIN']),
             'SYN Flag Count': self.safe_int_convert(flow['flow_tcp_flags']['SYN']),
             'RST Flag Count': self.safe_int_convert(flow['flow_tcp_flags']['RST']),
             'PSH Flag Count': self.safe_int_convert(flow['flow_tcp_flags']['PSH']),
             'ACK Flag Count': self.safe_int_convert(flow['flow_tcp_flags']['ACK']),
             'URG Flag Count': self.safe_int_convert(flow['flow_tcp_flags']['URG']),
             'CWE Flag Count': self.safe_int_convert(flow['flow_tcp_flags']['CWR']),
             'ECE Flag Count': self.safe_int_convert(flow['flow_tcp_flags']['ECE']),
             
             # Ratio and size statistics
             'Down/Up Ratio': flow['backward_packets'] / flow['forward_packets'] if flow['forward_packets'] > 0 else 0,
             'Average Packet Size': avg_pkt_size,
             'Avg Fwd Segment Size': flow['forward_bytes'] / flow['forward_packets'] if flow['forward_packets'] > 0 else 0,
             'Avg Bwd Segment Size': flow['backward_bytes'] / flow['backward_packets'] if flow['backward_packets'] > 0 else 0,
             
             # Bulk transfer statistics (placeholder values)
             'Fwd Avg Bytes/Bulk': 0,
             'Fwd Avg Packets/Bulk': 0,
             'Fwd Avg Bulk Rate': 0,
             'Bwd Avg Bytes/Bulk': 0,
             'Bwd Avg Packets/Bulk': 0,
             'Bwd Avg Bulk Rate': 0,
             
             # Subflow statistics
             'Subflow Fwd Packets': self.safe_int_convert(flow['forward_packets']),
             'Subflow Fwd Bytes': self.safe_int_convert(flow['forward_bytes']),
             'Subflow Bwd Packets': self.safe_int_convert(flow['backward_packets']),
             'Subflow Bwd Bytes': self.safe_int_convert(flow['backward_bytes']),
             
             # Window sizes
             'Init_Win_bytes_forward': self.safe_int_convert(flow['init_win_fwd'] or 0),
             'Init_Win_bytes_backward': self.safe_int_convert(flow['init_win_bwd'] or 0),
             
             # Active data packets (placeholder)
             'act_data_pkt_fwd': self.safe_int_convert(flow['forward_packets']),
             'min_seg_size_forward': self.safe_int_convert(flow['forward_length']['min']),
             
             # Active/Idle times (placeholder)
             'Active Mean': 0,
             'Active Std': 0,
             'Active Max': 0,
             'Active Min': 0,
             'Idle Mean': 0,
             'Idle Std': 0,
             'Idle Max': 0,
             'Idle Min': 0,
         }
         
         return entry
 
     def process_packet(self, packet):
         if not packet.haslayer(IP):
             return
 
         ip = packet[IP]
         src_ip = ip.src
         dst_ip = ip.dst
         proto = ip.proto
         src_port, dst_port, proto_name = None, None, 'Other'
 
         if packet.haslayer(TCP):
             tcp = packet[TCP]
             src_port, dst_port = tcp.sport, tcp.dport
             proto_name = 'TCP'
         elif packet.haslayer(UDP):
             udp = packet[UDP]
             src_port, dst_port = udp.sport, udp.dport
             proto_name = 'UDP'
 
         flow_key = self.get_flow_key(src_ip, dst_ip, src_port, dst_port, proto)
 
         if flow_key not in self._flows:
             self._flows[flow_key] = {
                 'original_src_ip': src_ip,
                 'original_dst_ip': dst_ip,
                 'original_src_port': src_port,
                 'original_dst_port': dst_port,
                 'proto': proto_name,
                 'start_time': packet.time,
                 'end_time': packet.time,
                 'forward_packets': 0,
                 'forward_bytes': 0,
                 'forward_iat': {'sum':0.0, 'sum_sq':0.0, 'min':float('inf'), 'max':0.0, 'count':0, 'last_time': None},
                 'forward_length': {'sum':0, 'sum_sq':0, 'min':float('inf'), 'max':0, 'count':0},
                 'forward_tcp_flags': defaultdict(int),
                 'backward_packets': 0,
                 'backward_bytes': 0,
                 'backward_iat': {'sum':0.0, 'sum_sq':0.0, 'min':float('inf'), 'max':0.0, 'count':0, 'last_time': None},
                 'backward_length': {'sum':0, 'sum_sq':0, 'min':float('inf'), 'max':0, 'count':0},
                 'backward_tcp_flags': defaultdict(int),
                 'flow_iat': {'sum':0.0, 'sum_sq':0.0, 'min':float('inf'), 'max':0.0, 'count':0, 'last_time': None},
                 'flow_tcp_flags': defaultdict(int),
                 'fwd_header_length': 0,
                 'bwd_header_length': 0,
                 'init_win_fwd': None,
                 'init_win_bwd': None,
             }
         
         flow = self._flows[flow_key]
 
         direction = 'forward' if (
             src_ip == flow['original_src_ip'] and
             dst_ip == flow['original_dst_ip'] and
             src_port == flow['original_src_port'] and
             dst_port == flow['original_dst_port']
         ) else 'backward'
 
         flow['start_time'] = min(flow['start_time'], packet.time)
         flow['end_time'] = max(flow['end_time'], packet.time)
         flow[f'{direction}_packets'] += 1
         pkt_len = len(packet)
         flow[f'{direction}_bytes'] += pkt_len
         self.update_stats(flow[f'{direction}_length'], pkt_len)
 
         # Update IAT for direction
         iat_stats = flow[f'{direction}_iat']
         current_time = packet.time
         if iat_stats['last_time'] is not None:
             iat = current_time - iat_stats['last_time']
             self.update_stats(iat_stats, iat)
         iat_stats['last_time'] = current_time
 
         # Update flow IAT
         flow_iat = flow['flow_iat']
         if flow_iat['last_time'] is not None:
             iat = current_time - flow_iat['last_time']
             self.update_stats(flow_iat, iat)
         flow_iat['last_time'] = current_time
 
         # TCP Flags
         if proto_name == 'TCP':
             tcp = packet[TCP]
             flags = []
             if tcp.flags.F: flags.append('FIN')
             if tcp.flags.S: flags.append('SYN')
             if tcp.flags.R: flags.append('RST')
             if tcp.flags.P: flags.append('PSH')
             if tcp.flags.A: flags.append('ACK')
             if tcp.flags.U: flags.append('URG')
             if tcp.flags.E: flags.append('ECE')
             if tcp.flags.C: flags.append('CWR')
             for flag in flags:
                 flow[f'{direction}_tcp_flags'][flag] += 1
                 flow['flow_tcp_flags'][flag] += 1
 
         # Header Length
         ip_header_len = ip.ihl * 4
         transport_header_len = len(packet[TCP]) if proto_name == 'TCP' else len(packet[UDP]) if proto_name == 'UDP' else 0
         if direction == 'forward':
             flow['fwd_header_length'] += ip_header_len + transport_header_len
             if flow['forward_packets'] == 1 and proto_name == 'TCP':
                 flow['init_win_fwd'] = tcp.window
         else:
             flow['bwd_header_length'] += ip_header_len + transport_header_len
             if flow['backward_packets'] == 1 and proto_name == 'TCP':
                 flow['init_win_bwd'] = tcp.window
 
         # Create flow entry for DataFrame
         flow_entry = self.create_flow_entry(flow)
         self._flow_data.append(flow_entry)
 
     def capture_traffic(self, timeout=60):
         """Start packet capture for the specified timeout period"""
         print("Starting network traffic monitoring...")
         sniff(prn=self.process_packet, store=0, timeout=timeout, iface="en0")
 
         
         if self._flow_data:
            print("Timeout reached. Stopping capture.")
         else:
             print("No network flows captured during the monitoring period.")