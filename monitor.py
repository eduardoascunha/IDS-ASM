import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from scapy.all import sniff, IP 


class MonitorAgent(Agent):
    def __init__(self, jid, password, router_ip):
        super().__init__(jid=jid, password=password)
        self.router_ip = router_ip 

    async def setup(self):
        print(f"Agent Monitor iniciado. Monitorando o Router: {self.router_ip}")
        self.add_behaviour(self.MonitorBehaviour())

    class MonitorBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                packet = await asyncio.get_event_loop().run_in_executor(None, self.capture_packet)
                if packet:
                    print(f"Pacote capturado do router {self.agent.router_ip}: {packet}")
                
                await asyncio.sleep(1)  # intervalo entre capturas
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
                print(f"Erro na captura de pacote: {e}")
                return None

    
async def main():
    
    router_ip = "10.0.1.1"  

    monitor = MonitorAgent(jid="dummy2@10.0.0.20", password="NOPASSWORD", router_ip=router_ip)

    await monitor.start()
    
    # Mantém o agente rodando
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await monitor.stop()

if __name__ == "__main__":
    asyncio.run(main())  
