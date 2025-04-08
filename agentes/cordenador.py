import asyncio
import spade
from spade.agent import Agent

from behaviours.ReceiveAlertsBehaviour import ReceiveAlertsBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class CordenadorAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.alerts = []

    async def setup(self):
        print(RED + f"[Cordenador] Agente Cordenador a rodar." + RESET)
        self.add_behaviour(ReceiveAlertsBehaviour())
