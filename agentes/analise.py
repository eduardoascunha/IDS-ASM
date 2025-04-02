import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
from signatures import ATTACK_SIGNATURES  
import jsonpickle


class AnaliseAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.signatures = ATTACK_SIGNATURES
        self.recent_packets = []
        self.alerts = []

    async def setup(self):
        print("Agente de Análise iniciado. A monitorizar pacotes...")
        self.add_behaviour(self.AnaliseBehaviour())

    class AnaliseBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                # Recebe mensagem do agente monitor
                print("Aguardando mensagem do monitor")
                msg = await self.receive(timeout=10)
                print(f"Mensagem recebida: {msg}")
                if msg:
                    #packet_data = json.loads(msg.body
                    print(f"recebi algo!!!!!!!!!!!!")
                    packet_data = jsonpickle.decode(msg.body)
                    print(f"Pacote recebido: {packet_data}")
                    await self.analyze_packet(packet_data)
                else:
                    print("Nenhuma mensagem recebida")
                
                await asyncio.sleep(1)
            
            except Exception as e:
                print(f"Erro na análise: {e}")

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
                    "details": f"Detetadas {len(unique_ports)} tentativas de ligação em portas diferentes"
                }
                print(f"ALERTA: {alert}")
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
                    "details": f"Detectados {len(recent_icmp)} pacotes ICMP em {self.agent.signatures['ping_flood']['conditions']['time_window']} segundo"
                }
                print(f"ALERTA: {alert}")
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
                    "details": f"Detectados {len(recent_tcp)} pacotes TCP em {self.agent.signatures['syn_flood']['conditions']['time_window']} segundo"
                }
                print(f"ALERTA: {alert}")
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
                    "details": f"Detectados {len(recent_dns)} pacotes DNS em {self.agent.signatures['dns_flood']['conditions']['time_window']} segundo"
                }
                print(f"ALERTA: {alert}")
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
                    "details": f"Detectados {len(recent_http)} pacotes HTTP em {self.agent.signatures['http_flood']['conditions']['time_window']} segundo"
                }
                print(f"ALERTA: {alert}")
                self.agent.alerts.append(alert)

async def main():
    analise = AnaliseAgent(jid="analise@10.0.0.20", password="NOPASSWORD")
    await analise.start()
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await analise.stop()

if __name__ == "__main__":
    spade.run(main())