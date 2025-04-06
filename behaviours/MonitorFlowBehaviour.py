import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from misc.flow_info import FlowInfo

class MonitorFlowBehaviour(CyclicBehaviour):
    async def run(self):
        print(GREEN,"[Monitor] Captura de fluxos em execução")
        self.agent.flow_controller.capture_traffic(iface=f"{self.agent.interface}", timeout=5, filter=f"not src host {self.agent.ip}")  # Capture traffic for 5 seconds
        flow_data = self.agent.flow_controller.get_flow_data()
        # Create DataFrame after capture is complete
        if flow_data:
            msg = Message(to="analise@10.0.6.1")     # Instantiate the message
            msg.set_metadata("performative", "inform-fluxo")  # Set the "inform" FIPA performative
            msg.body = jsonpickle.encode(self.agent.flow_controller)            # Set the message content

            await self.send(msg)
            print(GREEN,"[Monitor ]Mensagem enviada!")
        else:
            print(GREEN,"[Monitor] Nada relevante capturado")
        self.agent.flow_controller.wipe_flows()