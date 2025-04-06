import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from misc.signatures import ATTACK_SIGNATURES   
import joblib
import pandas as pd

from behaviours.AnaliseBehaviour import AnaliseBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class AnaliseAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.signatures = ATTACK_SIGNATURES
        self.recent_packets = []
        self.alerts = []
        self.model = joblib.load('anomalyModel/binary_classification_model.pkl')
        self.add_behaviour(RecvBehav())

    async def setup(self):
        print(BLUE + "[Analise] Agente de Análise iniciado." + RESET)
        self.add_behaviour(AnaliseBehaviour())
