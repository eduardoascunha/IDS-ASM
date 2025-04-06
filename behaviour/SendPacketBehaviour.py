import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import jsonpickle

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class SendPacketBehaviour(CyclicBehaviour):
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