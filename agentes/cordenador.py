import asyncio
import spade
from spade.agent import Agent
from misc.signatures import DEFENSE_SIGNATURES

from behaviours.CS_ReceiveAlertsBehaviour import ReceiveAlertsBehaviour
from behaviours.CS_PreventionBehaviour import PreventionBehaviour
from behaviours.CA_ReceiveAnomaliaBehaviour import ReceiveAnomaliaBehaviour
from behaviours.CS_ApagaAlertasBehaviour import ApagaAlertasBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class CordenadorAgent(Agent):
    def __init__(self, jid, password, flag_init):
        super().__init__(jid=jid, password=password)
        self.alerts = []
        self.alerts_resolved = []
        self.alerts_anomalias = []
        self.flag_init = flag_init
        self.defense_signatures = DEFENSE_SIGNATURES

    async def setup(self):
        print(RED + f"[Cordenador] Agente Cordenador a rodar." + RESET)

        if self.flag_init == 1: # assinatura
            self.add_behaviour(ReceiveAlertsBehaviour())
            self.add_behaviour(PreventionBehaviour())
        
        elif self.flag_init == 2: # anomalia
            self.add_behaviour(ReceiveAnomaliaBehaviour())

        else: # asm
            self.add_behaviour(ReceiveAlertsBehaviour())
            self.add_behaviour(PreventionBehaviour())
            self.add_behaviour(ReceiveAnomaliaBehaviour())
        
        self.add_behaviour(ApagaAlertasBehaviour(period=3600)) # 1h

    
