import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from misc.flow_info import FlowInfo

from behaviours.MonitorBehaviour import MonitorBehaviour
from behaviours.SendPacketBehaviour import SendPacketBehaviour
from behaviours.MonitorFlowBehaviour import MonitorFlowBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class MonitorAgent(Agent):
    def __init__(self, jid, password, agenteAnalise, interface, flag_init, ip=None):
        super().__init__(jid=jid, password=password)
        self.packet_queue = asyncio.Queue()
        self.agenteAnalise = agenteAnalise
        #self.ip = ip
        self.interface = interface
        self.flow_controller = FlowInfo()
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

        