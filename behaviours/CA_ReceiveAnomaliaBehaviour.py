import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class ReceiveAnomaliaBehaviour(CyclicBehaviour):

    async def run(self):
        try:
            msg = await self.receive(timeout=10)
            if msg.metadata["performative"] == "inform-fluxo":
                alert_data = jsonpickle.decode(msg.body)
                print(RED + f"[Cordenador] Anomalia Recebida: {alert_data}" + RESET)

                if (alert_data) not in self.agent.alerts_anomalia:
                    self.agent.alerts_anomalia.append(alert_data)
                
                # receve e atua
                # ids anomaly based apenas avisa o administrador de rede
                # avisar o administrador de rede
                print(RED + f"[Cordenador] ADMINISTRADOR DE REDE, NOVO ALERTA!" + RESET)

            else:
                print(RED + "[Cordenador] Nenhum alerta recebido" + RESET)

        except Exception as e:
            print(RED + f"[Cordenador] Erro ao receber alerta: {e}" + RESET)