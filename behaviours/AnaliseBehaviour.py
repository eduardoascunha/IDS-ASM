import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import pandas as pd

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class AnaliseBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                # Recebe mensagem do agente monitor
                msg = await self.receive(timeout=10)
                if msg:

                    if msg.metadata["performative"] == 'inform-fluxo':
                         print(BLUE + "Received message from sender" + RESET)
                         flow_info = jsonpickle.decode(msg.body)
                         flow_data = flow_info.get_flow_data()
                         if flow_data:
                             df = pd.DataFrame(flow_data)
                             print(BLUE + "\nReceived DataFrame with shape: " + str(df.shape) + RESET)
                             print(BLUE + "Sample data:" + RESET)
                             print(BLUE + str(df.head()) + RESET)
 
                             try:
                                 # Predict using the loaded model
                                 predictions = self.agent.model.predict(df)
                                 df['prediction'] = predictions
                                 if 1 in predictions or "ANOMALY" in predictions:
                                     print(BLUE + "\nAnomaly detected in the incoming flow!" + RESET)
                                     print(BLUE + str(df[df['prediction'] == 'ANOMALY']) + RESET)  # Show only anomalies
                                 else:
                                     print(BLUE + "\nAll clear. No anomalies detected." + RESET)
                             except Exception as e:
                                 print(BLUE + "Error during prediction:", str(e) + RESET)


                    try:
                        packet_data = jsonpickle.decode(msg.body)

                        # Se for uma lista de pacotes, processa um por um
                        if isinstance(packet_data, list):
                            print(BLUE + f"[Analise] {len(packet_data)} lista de pacotes recebidos, com {len(packet_data)} pacotes." + RESET)
                            for packet in packet_data:
                                await self.analyze_packet(packet)
                        else:
                            print(BLUE + f"[Analise] Pacote recebido: {packet_data}" + RESET)
                            await self.analyze_packet(packet_data)

                    except Exception as e:
                        print(BLUE + f"[Analise] Erro ao decodificar mensagem: {e}" + RESET)
                else:
                    print(BLUE + "[Analise] Nenhuma mensagem recebida" + RESET)

            except Exception as e:
                print(BLUE + f"[Analise] Erro na análise: {e}" + RESET)

        async def analyze_packet(self, packet):
            # Adiciona timestamp ao pacote
            packet["timestamp"] = asyncio.get_event_loop().time()
            self.agent.recent_packets.append(packet)
            
            # Remove pacotes antigos (mais de 10 segundos)
            current_time = asyncio.get_event_loop().time()
            self.agent.recent_packets = [
                p for p in self.agent.recent_packets 
                if current_time - p["timestamp"] <= 10
            ]

            # Analisa assinaturas
            await self.check_port_scan(packet)
            await self.check_ping_flood()
            await self.check_syn_flood()
            await self.check_dns_flood()
            await self.check_http_flood()

        async def check_port_scan(self, packet):
            if packet.get("src_port") is None:
                return

            # Verifica se há múltiplas tentativas de ligação de um mesmo IP
            src_ip = packet["src_ip"]
            current_time = asyncio.get_event_loop().time()
            recent_attempts = [
                p for p in self.agent.recent_packets
                if p["src_ip"] == src_ip 
                and current_time - p["timestamp"] <= self.agent.signatures["port_scan"]["conditions"]["time_window"]
            ]

            unique_ports = set(p["dst_port"] for p in recent_attempts if p["dst_port"] is not None)
            
            if len(unique_ports) >= self.agent.signatures["port_scan"]["conditions"]["min_attempts"]:
                alert = {
                    "type": "port_scan",
                    "src_ip": src_ip,
                    "timestamp": current_time,
                    "details": f"Detetadas {len(unique_ports)} tentativas de ligação em portas diferentes proveniente do ip: {src_ip}"
                }
                print(BLUE + f"[Analise] ALERTA: {alert}" + RESET)
                self.agent.alerts.append(alert)

        async def check_ping_flood(self):
            current_time = asyncio.get_event_loop().time()
            recent_icmp = [
                p for p in self.agent.recent_packets
                if p["protocol"] == 1  # ICMP
                and current_time - p["timestamp"] <= self.agent.signatures["ping_flood"]["conditions"]["time_window"]
            ]

            if len(recent_icmp) >= self.agent.signatures["ping_flood"]["conditions"]["count_threshold"]:
                alert = {
                    "type": "ping_flood",
                    "timestamp": current_time,
                    "details": f"Detetados {len(recent_icmp)} pacotes ICMP em {self.agent.signatures['ping_flood']['conditions']['time_window']} segundo"
                }
                print(BLUE + f"[Analise] ALERTA: {alert}" + RESET)
                self.agent.alerts.append(alert)

        async def check_syn_flood(self):
            current_time = asyncio.get_event_loop().time()
            recent_tcp = [
                p for p in self.agent.recent_packets
                if p["protocol"] == 6  # TCP
                and current_time - p["timestamp"] <= self.agent.signatures["syn_flood"]["conditions"]["time_window"]
            ]

            if len(recent_tcp) >= self.agent.signatures["syn_flood"]["conditions"]["count_threshold"]:
                alert = {
                    "type": "syn_flood",
                    "timestamp": current_time,
                    "details": f"Detetados {len(recent_tcp)} pacotes TCP em {self.agent.signatures['syn_flood']['conditions']['time_window']} segundo"
                }
                print(BLUE + f"[Analise] ALERTA: {alert}" + RESET)
                self.agent.alerts.append(alert)

        async def check_dns_flood(self):
            current_time = asyncio.get_event_loop().time()
            recent_dns = [
                p for p in self.agent.recent_packets
                if p["protocol"] == 17  # UDP
                and p.get("dst_port") == 53  # DNS port
                and current_time - p["timestamp"] <= self.agent.signatures["dns_flood"]["conditions"]["time_window"]
            ]

            if len(recent_dns) >= self.agent.signatures["dns_flood"]["conditions"]["count_threshold"]:
                alert = {
                    "type": "dns_flood",
                    "timestamp": current_time,
                    "details": f"Detetados {len(recent_dns)} pacotes DNS em {self.agent.signatures['dns_flood']['conditions']['time_window']} segundo"
                }
                print(BLUE + f"[Analise] ALERTA: {alert}" + RESET)
                self.agent.alerts.append(alert)

        async def check_http_flood(self):
            current_time = asyncio.get_event_loop().time()
            recent_http = [
                p for p in self.agent.recent_packets
                if p["protocol"] == 6  # TCP
                and p["dst_port"] == 80  # HTTP port
                and current_time - p["timestamp"] <= self.agent.signatures["http_flood"]["conditions"]["time_window"]
            ]

            if len(recent_http) >= self.agent.signatures["http_flood"]["conditions"]["count_threshold"]:
                alert = {
                    "type": "http_flood",
                    "timestamp": current_time,
                    "details": f"Detetados {len(recent_http)} pacotes HTTP em {self.agent.signatures['http_flood']['conditions']['time_window']} segundo"
                }
                print(BLUE + f"[Analise] ALERTA: {alert}" + RESET)
                self.agent.alerts.append(alert)
