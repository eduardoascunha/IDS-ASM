import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from scapy.all import sniff, IP 
from spade.message import Message
import json
import jsonpickle


class MonitorAgent(Agent):
    def __init__(self, jid, password, router_ip):
        super().__init__(jid=jid, password=password)
        self.router_ip = router_ip
        self.packet_queue = asyncio.Queue()

    async def setup(self):
        print(f"Agente Monitor a rodar. A monitorizar o Router: {self.router_ip}")
        self.add_behaviour(self.MonitorBehaviour())
        self.add_behaviour(self.SendBehaviour())

    class MonitorBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                packet = await asyncio.get_event_loop().run_in_executor(None, self.capture_packet)
                if packet:
                    print(f"Pacote capturado do Router {self.agent.router_ip}: {packet}")
                    await self.agent.packet_queue.put(packet)
                await asyncio.sleep(1)

            except Exception as e:
                print(f"Erro no comportamento: {e}")

        def packet_callback(self, pkt):
            if IP in pkt:
                return {
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
                # captura um pacote
                packets = sniff(iface="eth0", count=1, prn=self.packet_callback, filter="icmp") 
                
                if packets and len(packets) > 0:
                    return self.packet_callback(packets[0])
                return None
            
            except Exception as e:
                print(f"Erro na captura do pacote: {e}")
                return None

    
    class SendBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                packet = await self.agent.packet_queue.get()
                if packet:
                    # enviar para o agente de analise
                    msg = Message(to="analise@10.0.0.20")
                    msg.set_metadata("performative", "inform")  
                    #msg.body = json.dumps(packet)
                    msg.body = jsonpickle.encode(packet)
                    
                    print(f"A enviar pacote para análise: {packet}")  # Debug
                    await self.send(msg)
                    print("Pacote enviado com sucesso")  # Debug
                    
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
            
            await asyncio.sleep(0.1)

async def main():
    
    router_ip = "10.0.1.1"  

    monitor = MonitorAgent(jid="monitor@10.0.0.20", password="NOPASSWORD", router_ip=router_ip)

    await monitor.start()
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await monitor.stop()

if __name__ == "__main__":
    spade.run(main())
