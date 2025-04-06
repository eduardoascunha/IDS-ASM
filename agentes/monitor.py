import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from scapy.all import sniff, IP 
from spade.message import Message
import json
import jsonpickle
from datetime import datetime

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class MonitorAgent(Agent):
    def __init__(self, jid, password, agenteAnalise, ip,interface):
        super().__init__(jid=jid, password=password)
        self.packet_queue = asyncio.Queue()
        self.agenteAnalise = agenteAnalise
        self.ip = ip
        self.interface = interface

    async def setup(self):
        print(GREEN + f"[Monitor] Agente Monitor a rodar." + RESET)
        self.add_behaviour(self.MonitorBehaviour())
        self.add_behaviour(self.SendBehaviour())

    class MonitorBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                packet = await asyncio.get_event_loop().run_in_executor(None, self.capture_packet)
                if packet:
                    print(GREEN + f"[Monitor] Pacote capturado do Router: {packet}" + RESET)
                    # Coloca cada pacote individualmente na fila
                    for pkt in packet:
                        await self.agent.packet_queue.put(pkt)
                await asyncio.sleep(0.1)
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


    
    class SendBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                i = 0
                packets = []

                # Aguardar até 5 pacotes ou 1 segundo
                start_time = asyncio.get_event_loop().time()
                while (not self.agent.packet_queue.empty() or i < 5) and (asyncio.get_event_loop().time() - start_time < 1):
                    if not self.agent.packet_queue.empty():
                        packets.append(await self.agent.packet_queue.get())
                        i += 1
    
                if packets:
                    msg = Message(to=f"{self.agent.agenteAnalise}")
                    msg.set_metadata("performative", "inform")
                    msg.body = jsonpickle.encode(packets)  # Enviar varios pacotes
                    
                    await self.send(msg)
                    print(GREEN + f"[Monitor] {len(packets)} pacotes enviados com sucesso" + RESET)
                
                await asyncio.sleep(0.1)

            except Exception as e:
                print(GREEN + f"[Monitor] Erro ao enviar pacotes: {e}" + RESET) 
