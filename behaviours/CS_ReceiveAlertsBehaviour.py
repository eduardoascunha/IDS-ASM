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

class ReceiveAlertsBehaviour(CyclicBehaviour):
    # assinaturas
    async def run(self):
        try:
            msg = await self.receive(timeout=10)
            if msg:
                alert_data = jsonpickle.decode(msg.body)
                print(RED + f"[Cordenador] Alerta Recebido: {alert_data}" + RESET)

                ip = alert_data['src_ip']
                type = alert_data['type']

                if (ip,type) not in self.agent.alerts:
                    self.agent.alerts.append((ip,type))

            else:
                print(RED + "[Cordenador] Nenhum alerta recebido" + RESET)

        except Exception as e:
            print(RED + f"[Cordenador] Erro ao receber alerta: {e}" + RESET)