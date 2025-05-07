import asyncio
import spade
from spade.agent import Agent
from dotenv import load_dotenv
import os

from behaviours.EA_ReceiveLogsBehaviour import ReceiveLogsBehaviour
from behaviours.EA_AnaliseLogsBehaviour import AnaliseLogsBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m' 
RESET = '\033[0m'

class EngenheiroAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)

        self.logs = asyncio.Queue()
        self.alerts = []
        self.agenteCordenador = None
        
        load_dotenv()
        self.RELATORIO_PATH_incomplete = os.getenv("RELATORIO_PATH") 

    async def setup(self):
        print(YELLOW + f"[Engenheiro] Agente Engenheiro a rodar." + RESET)

        self.add_behaviour(ReceiveLogsBehaviour())
        self.add_behaviour(AnaliseLogsBehaviour())
        
        

    
