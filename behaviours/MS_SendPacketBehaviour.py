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
            packets = []

            while not self.agent.packet_queue.empty():
                packets.append(await self.agent.packet_queue.get())

            if packets:
                msg = Message(to=f"{self.agent.agenteAnalise}")
                msg.set_metadata("performative", "inform")
                msg.body = jsonpickle.encode(packets)
                
                await self.send(msg)
                print(GREEN + f"[Monitor] {len(packets)} pacotes enviados com sucesso" + RESET)

            await asyncio.sleep(1)  # 1 segundo entre cada batch

        except Exception as e:
            print(GREEN + f"[Monitor] Erro ao enviar pacotes: {e}" + RESET)