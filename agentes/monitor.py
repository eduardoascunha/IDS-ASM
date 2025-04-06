import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from scapy.all import sniff, IP 
from spade.message import Message
import json
import jsonpickle
from datetime import datetime

from behaviours.MonitorBehaviour import MonitorBehaviour
from behaviours.SendPacketBehaviour import SendPacketBehaviour

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class MonitorAgent(Agent):
    def __init__(self, jid, password, agenteAnalise, ip,interface):
        super().__init__(jid=jid, password=password)
        self.packet_queue = asyncio.Queue()
        self.agenteAnalise = agenteAnalise
        self.ip = ip
        self.interface = interface

    async def setup(self):
        print(GREEN + f"[Monitor] Agente Monitor a rodar." + RESET)
        self.add_behaviour(MonitorBehaviour())
        self.add_behaviour(SendPacketBehaviour())
