import asyncio
import spade
from spade.agent import Agent

from behaviours.ReceiveAlertsBehaviour import ReceiveAlertsBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class CordenadorAgent(Agent):
    def __init__(self, jid, password, flag_init):
        super().__init__(jid=jid, password=password)
        self.alerts = []
        self.alerts_anomalias = []
        self.flag_init = flag_init

    async def setup(self):
        print(RED + f"[Cordenador] Agente Cordenador a rodar." + RESET)
        self.add_behaviour(ReceiveAlertsBehaviour())
        self.add_behaviour(ReceiveAnomaliaBehaviour())

        if self.flag_init == 1:
            #self.add_behaviour(MonitorBehaviour())
            print("a")
        
        elif self.flag_init == 2:
            #self.add_behaviour(MonitorFlowBehaviour())
            self.add_behaviour(CordenadorAnomaliaBehaviour())
            print("a")

        else:
            #self.add_behaviour(MonitorBehaviour())
            print("a")
