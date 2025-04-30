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

class FlowReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=60)  # wait for a message for t seconds
            if msg and msg.metadata["performative"] == 'inform-fluxo':
                print(BLUE + "[Analise] Mensagem recebida do sender" + RESET)
                flow_info = jsonpickle.decode(msg.body)
                flow_data_dict = flow_info.get_flow_data()
                #print(BLUE + f"[Analise] Fluxo recebido: {flow_data_dict}" + RESET)
                await self.agent.recent_flows.put(flow_data_dict)
 
            else:
                print(BLUE + "[Analise] Nenhuma mensagem recebida em 60 segundos" + RESET)