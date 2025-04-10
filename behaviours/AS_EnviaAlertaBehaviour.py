import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import jsonpickle

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class EnviaAlertaBehaviour(CyclicBehaviour):
    async def run(self):
        if self.agent.alerts:
            for alerta in self.agent.alerts:
                print(BLUE + f"[Analise] A enviar alerta {alerta}" + RESET)
                msg = Message(to=f"{self.agent.agenteCordenador}")
                msg.set_metadata("performative", "inform")
                msg.body = jsonpickle.encode(alerta)
                await self.send(msg)

        self.agent.alerts = []