import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from misc.signatures import ATTACK_SIGNATURES   
import joblib

from behaviours.AnaliseBehaviour import AnaliseBehaviour
from behaviours.RecvBehav import RecvBehav
from behaviours.EnviaAlertaBehaviour import EnviaAlertaBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class AnaliseAgent(Agent):
    def __init__(self, jid, password, agenteCordenador):
        super().__init__(jid=jid, password=password)
        self.signatures = ATTACK_SIGNATURES
        self.recent_packets = []
        self.alerts = []
        self.agenteCordenador = agenteCordenador

        try:
            self.model = joblib.load('anomalyModel/binary_classification_model.pkl')
        except Exception as e:
            print(BLUE + f"[Analise] Erro ao carregar modelo: {e}" + RESET)
            raise  

    async def setup(self):
        print(BLUE + "[Analise] Agente de Análise iniciado." + RESET)
        self.add_behaviour(AnaliseBehaviour())
        #self.add_behaviour(RecvBehav())
        self.add_behaviour(EnviaAlertaBehaviour())
