import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from misc.flow_info import FlowInfo

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class MonitorFlowBehaviour(CyclicBehaviour):
    async def run(self):
        print(GREEN + "[Monitor] Captura de fluxos em execução" + RESET)
        self.agent.flow_controller.capture_traffic(iface=self.agent.interface, timeout=5, filter=f"not src host {self.agent.ip}")  # Capture traffic for 5 seconds
        flow_data = self.agent.flow_controller.get_flow_data()
        # Create DataFrame after capture is complete
        if flow_data:
            msg = Message(to=f"{self.agent.agenteAnalise}")     # Instantiate the message
            msg.set_metadata("performative", "inform-fluxo")  # Set the "inform" FIPA performative
            msg.body = jsonpickle.encode(self.agent.flow_controller)            # Set the message content

            await self.send(msg)
            print(GREEN + "[Monitor] Mensagem enviada!" + RESET)
        else:
            print(GREEN + "[Monitor] Nada relevante capturado" + RESET)
        self.agent.flow_controller.wipe_flows()