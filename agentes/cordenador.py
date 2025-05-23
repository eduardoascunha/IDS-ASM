import asyncio
import spade
from spade.agent import Agent
from misc.signatures import DEFENSE_SIGNATURES

from behaviours.CS_ReceiveAlertsBehaviour import ReceiveAlertsBehaviour
from behaviours.CS_PreventionBehaviour import PreventionBehaviour
from behaviours.CS_ApagaAlertasBehaviour import ApagaAlertasBehaviour
from behaviours.CA_ReceiveAnomaliaBehaviour import ReceiveAnomaliaBehaviour
from behaviours.CA_ReceiveRequestBehaviour import ReceiveRequestBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class CordenadorAgent(Agent):
    def __init__(self, jid, password, maquinas_a_proteger, flag_init, agenteEngenheiro=None):
        super().__init__(jid=jid, password=password)

        if flag_init == 1: # assinaturas
            self.alerts = []
            self.alerts_resolved = []
            self.defense_signatures = DEFENSE_SIGNATURES

        elif flag_init == 2: # anomalias
            self.loggerCounter = 0
            self.fileLogCounter = 0
            self.agenteEngenheiro = agenteEngenheiro

        else: # asm
            self.alerts = []
            self.alerts_resolved = []
            self.defense_signatures = DEFENSE_SIGNATURES
            self.loggerCounter = 0
            self.fileLogCounter = 0
            self.agenteEngenheiro = agenteEngenheiro
        
        self.maquinas_a_proteger = maquinas_a_proteger
        self.flag_init = flag_init

    async def setup(self):
        print(RED + f"[Cordenador] Agente Cordenador a rodar." + RESET)

        if self.flag_init == 1: # assinatura
            self.add_behaviour(ReceiveAlertsBehaviour())
            self.add_behaviour(PreventionBehaviour())
            self.add_behaviour(ApagaAlertasBehaviour(period=3600)) # 1h
        
        elif self.flag_init == 2: # anomalia
            self.add_behaviour(ReceiveAnomaliaBehaviour())
            self.add_behaviour(ReceiveRequestBehaviour())

        else: # asm
            self.add_behaviour(ReceiveAlertsBehaviour())
            self.add_behaviour(PreventionBehaviour())
            self.add_behaviour(ApagaAlertasBehaviour(period=3600)) # 1h
            self.add_behaviour(ReceiveAnomaliaBehaviour())
            self.add_behaviour(ReceiveRequestBehaviour())
            
            
        
        

    
