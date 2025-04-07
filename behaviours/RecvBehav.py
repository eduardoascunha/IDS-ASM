import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import pandas as pd

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class RecvBehav(CyclicBehaviour):
         async def run(self):
             print(BLUE + "RecvBehav running" + RESET)
             msg = await self.receive(timeout=120)  # wait for a message for t seconds
             if msg and msg.metadata["performative"] == 'inform-fluxo':
                 print(BLUE + "Received message from sender" + RESET)
                 flow_info = jsonpickle.decode(msg.body)
                 flow_data = flow_info.get_flow_data()
                 if flow_data:
                     df = pd.DataFrame(flow_data)
                     print(BLUE + "\nReceived DataFrame with shape:", df.shape + RESET)
                     print(BLUE + "Sample data:" + RESET)
                     print(df.head())
 
                     try:
                         # Predict using the loaded model
                         predictions = self.agent.model.predict(df)
                         df['prediction'] = predictions
                         if 1 in predictions or "ANOMALY" in predictions:
                             print(BLUE + "\nAnomaly detected in the incoming flow!" + RESET)
                             print(BLUE + str(df[df['prediction'] == 'ANOMALY']) + RESET)  # Show only anomalies
                         else:
                             print(BLUE + "\nAll clear. No anomalies detected." + RESET)
                     except Exception as e:
                         print(BLUE + "Error during prediction:", str(e) + RESET)
 
             else:
                 print(BLUE + "Did not receive any message after 60 seconds" + RESET)
                 self.kill()
 
async def on_end(self):
    await self.agent.stop()