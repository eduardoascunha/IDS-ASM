import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import jsonpickle

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class AnomaliaResponseBehaviour(CyclicBehaviour):
    async def run(self):
        # receber alertas de anomalias

        # alerta ao administrador de rede
        
        print("ola")