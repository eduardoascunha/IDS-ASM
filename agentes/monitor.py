import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from misc.flow_info import FlowInfo

from behaviours.MS_MonitorBehaviour import MonitorBehaviour
from behaviours.MS_SendPacketBehaviour import SendPacketBehaviour
from behaviours.MA_MonitorFlowBehaviour import MonitorFlowBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class MonitorAgent(Agent):
    def __init__(self, jid, password, agenteAnalise, interface, flag_init):
        super().__init__(jid=jid, password=password)

        if flag_init == 1: # assinaturas
            self.packet_queue = asyncio.Queue()

        elif flag_init == 2: # anomalias
            self.flow_controller = FlowInfo()

        else: # asm
            self.packet_queue = asyncio.Queue()
            self.flow_controller = FlowInfo()
        
        self.interface = interface
        self.agenteAnalise = agenteAnalise
        self.flag_init = flag_init

    async def setup(self):
        print(GREEN + f"[Monitor] Agente Monitor a rodar." + RESET)

        if self.flag_init == 1:
            self.add_behaviour(MonitorBehaviour())
            self.add_behaviour(SendPacketBehaviour())
        
        elif self.flag_init == 2:
            self.add_behaviour(MonitorFlowBehaviour())

        else:
            self.add_behaviour(MonitorBehaviour())
            self.add_behaviour(MonitorFlowBehaviour())
            self.add_behaviour(SendPacketBehaviour())

        