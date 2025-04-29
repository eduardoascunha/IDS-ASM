import spade
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class ApagaAlertasBehaviour(PeriodicBehaviour):
    async def run(self):

        if self.agent.alertas_detetados:
            print(BLUE + f"[Analise] A apagar alertas!" + RESET)
            self.agent.alertas_detetados = {}