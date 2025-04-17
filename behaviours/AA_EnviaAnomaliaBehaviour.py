import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import jsonpickle

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class EnviaAnomaliaBehaviour(CyclicBehaviour):
    async def run(self):
        try:
            if self.agent.alerts_anomalias:
                for alerta in self.agent.alerts_anomalias:
                    print(BLUE + f"[Analise] A enviar anomalia para Agente Cordenador!" + RESET)
                    msg = Message(to=f"{self.agent.agenteCordenador}")
                    msg.set_metadata("performative", "inform-fluxo")
                    msg.body = jsonpickle.encode(alerta)
                    await self.send(msg)

        except Exception as e:
            print(BLUE + f"[Analise] Erro ao enviar anomalia: {e}" + RESET)

        self.agent.alerts_anomalias = []