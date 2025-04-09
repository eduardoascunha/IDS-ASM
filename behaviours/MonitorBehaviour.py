import spade
from spade.behaviour import CyclicBehaviour
from datetime import datetime
from scapy.all import sniff, IP
import asyncio

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class MonitorBehaviour(CyclicBehaviour):
    async def run(self):
        try:
            packet = await asyncio.get_event_loop().run_in_executor(None, self.capture_packet)
            if packet:
                print(GREEN + f"[Monitor] Pacote capturado do Router: {packet}" + RESET)
                # Coloca cada pacote individualmente na fila
                for pkt in packet:
                    await self.agent.packet_queue.put(pkt)

        except Exception as e:
            print(GREEN + f"[Monitor] Erro no comportamento: {e}" + RESET)

    def packet_callback(self, pkt):
        if IP in pkt:
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
                "src_ip": pkt[IP].src,
                "dst_ip": pkt[IP].dst,
                "protocol": pkt[IP].proto,
                "size_bytes": len(pkt),
                "src_port": pkt.sport if hasattr(pkt, 'sport') else None,
                "dst_port": pkt.dport if hasattr(pkt, 'dport') else None,
            }
        return None

    def capture_packet(self):
        try:
            packets = sniff(iface=self.agent.interface, timeout=1, filter=f"not src host {self.agent.ip}")
            processed_packets = [self.packet_callback(pkt) for pkt in packets if self.packet_callback(pkt)]
            return processed_packets if processed_packets else None  # Retorna uma lista de pacotes processados ou None
        except Exception as e:
            print(GREEN + f"[Monitor] Erro na captura do pacote: {e}" + RESET)
            return None