import asyncio
import spade
import os
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import pandas as pd
import numpy as np

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class AnaliseLogsBehaviour(CyclicBehaviour):
    async def run(self):

        if self.agent.logs:
            log_data = await self.agent.logs.get()

            # analisar log
            print(YELLOW + "[Engenheiro] Log recebido:" + RESET)
            print(log_data)

            # caso anomalia enviar ao agente cordenador

        else:
            print(YELLOW + "[Engenheiro] Nenhum log pra ser analisado" + RESET)