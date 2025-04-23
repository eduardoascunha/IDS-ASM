import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from misc.signatures import ATTACK_SIGNATURES   
import joblib

from behaviours.AS_AnaliseBehaviour import AnaliseBehaviour
from behaviours.AS_EnviaAlertaBehaviour import EnviaAlertaBehaviour
from behaviours.AA_FlowReceiveBehaviour import FlowReceiveBehaviour
from behaviours.AA_EnviaAnomaliaBehaviour import EnviaAnomaliaBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class AnaliseAgent(Agent):
    def __init__(self, jid, password, agenteCordenador, flag_init):
        super().__init__(jid=jid, password=password)
        self.signatures = ATTACK_SIGNATURES
        self.recent_packets = []
        self.alerts = []
        self.alerts_anomalias = []
        self.agenteCordenador = agenteCordenador
        self.flag_init = flag_init

        try:
            #self.model = joblib.load('anomalyModel/binary_classification_model.pkl')
            self.model = joblib.load('anomalyModel/isolation_model_clean_smote.pkl')
        except Exception as e:
            print(BLUE + f"[Analise] Erro ao carregar modelo: {e}" + RESET)
            raise  

    async def setup(self):
        print(BLUE + "[Analise] Agente de Análise iniciado." + RESET)

        if self.flag_init == 1:
            self.add_behaviour(AnaliseBehaviour())
            self.add_behaviour(EnviaAlertaBehaviour())
            
        elif self.flag_init == 2:
            self.add_behaviour(FlowReceiveBehaviour())
            self.add_behaviour(EnviaAnomaliaBehaviour())

        else:
            self.add_behaviour(AnaliseBehaviour())
            self.add_behaviour(FlowReceiveBehaviour())
            self.add_behaviour(EnviaAlertaBehaviour())
        