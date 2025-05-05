import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from behaviours.AA_FlowAnaliseBehaviour import FlowAnaliseBehaviour
from misc.signatures import ATTACK_SIGNATURES   
import joblib

from behaviours.AS_AnaliseBehaviour import AnaliseBehaviour
from behaviours.AS_EnviaAlertaBehaviour import EnviaAlertaBehaviour
from behaviours.AS_ApagaAlertasBehaviour import ApagaAlertasBehaviour
from behaviours.AA_FlowReceiveBehaviour import FlowReceiveBehaviour
from behaviours.AA_EnviaAnomaliaBehaviour import EnviaAnomaliaBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class AnaliseAgent(Agent):
    def __init__(self, jid, password, agenteCordenador, flag_init):
        super().__init__(jid=jid, password=password)

        if flag_init == 1: # assinaturas
            self.signatures = ATTACK_SIGNATURES # s
            self.recent_packets = []            # s 
            self.alerts = []                    # s   
            self.alertas_detetados = {}         # s

        elif flag_init == 2: # anomalias
            self.recent_flows = asyncio.Queue() # a
            self.alerts_anomalias = []          # a
            try:
                self.model = joblib.load('anomalyModel/isolation_model_clean.pkl')
            except Exception as e:
                print(BLUE + f"[Analise] Erro ao carregar modelo: {e}" + RESET)
                raise  

        else: # asm
            self.signatures = ATTACK_SIGNATURES # s
            self.recent_packets = []            # s 
            self.alerts = []                    # s   
            self.alertas_detetados = {}         # s
            self.recent_flows = asyncio.Queue() # a
            self.alerts_anomalias = []          # a
            try:
                self.model = joblib.load('anomalyModel/isolation_model_clean.pkl')
            except Exception as e:
                print(BLUE + f"[Analise] Erro ao carregar modelo: {e}" + RESET)
                raise  
        
        self.agenteCordenador = agenteCordenador
        self.flag_init = flag_init

    async def setup(self):
        print(BLUE + "[Analise] Agente de Análise iniciado." + RESET)

        if self.flag_init == 1:
            self.add_behaviour(AnaliseBehaviour())
            self.add_behaviour(EnviaAlertaBehaviour())
            self.add_behaviour(ApagaAlertasBehaviour(period=3600)) # 1h
            
        elif self.flag_init == 2:
            self.add_behaviour(FlowReceiveBehaviour())
            self.add_behaviour(FlowAnaliseBehaviour())
            self.add_behaviour(EnviaAnomaliaBehaviour())

        else:
            self.add_behaviour(AnaliseBehaviour())
            self.add_behaviour(FlowReceiveBehaviour())
            self.add_behaviour(FlowAnaliseBehaviour())
            self.add_behaviour(EnviaAlertaBehaviour())
        