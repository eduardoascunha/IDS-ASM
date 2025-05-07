import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle


RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m' 
RESET = '\033[0m'

class ReceiveLogsBehaviour(CyclicBehaviour):

    async def run(self):
        try:
            msg = await self.receive(timeout=60) # 1 minuto
            if msg:
                self.agent.agenteCordenador = msg.sender
                if msg.metadata["performative"] == "inform":
                    log_data = jsonpickle.decode(msg.body)
                    await self.agent.logs.put(log_data['numero_ficheiro'])
                    #print(YELLOW + f"[Engenheiro] Log recebido: {log_data}" + RESET)

            else:
                print(YELLOW + "[Engenheiro] Nenhum log recebido" + RESET)

        except Exception as e:
            print(YELLOW + f"[Engenheiro] Erro ao receber log: {e}" + RESET)