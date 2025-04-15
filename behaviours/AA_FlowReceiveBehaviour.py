import asyncio
import spade
import os
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import pandas as pd

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[35m'
RESET = '\033[0m'

class FlowReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            print(BLUE + "FlowReceiveBehaviour running" + RESET)
            msg = await self.receive(timeout=120)  # wait for a message for t seconds
            if msg and msg.metadata["performative"] == 'inform-fluxo':
                print(BLUE + "Received message from sender" + RESET)
                flow_info = jsonpickle.decode(msg.body)
                flow_data = flow_info.get_flow_data()
                if flow_data:
                    df = pd.DataFrame(flow_data)
                    print(BLUE + "\nReceived DataFrame with shape:", str(df.shape) + RESET)
                    print(BLUE + "Sample data:" + RESET)
                    print(df.head())

                    try:
                        # Save the DataFrame to a CSV file
                        file_path = "anomalyModel/data/flow_data.csv"

                        if not os.path.exists(file_path):
                            df.to_csv(file_path, index=False)
                            print(BLUE + "\nDataFrame saved to CSV file" + RESET)
                        
                        else:
                            df.to_csv(file_path, index=False, mode='a', header=False)
                            print(BLUE + "\nDataFrame appended to CSV file" + RESET)

                        # Predict using the loaded model
                        predictions = self.agent.model.predict(df)
                        df['prediction'] = predictions
                        if 1 in predictions or "ANOMALY" in predictions:
                            print(BLUE + "\nAnomaly detected in the incoming flow!" + RESET)
                            print(BLUE + str(df[df['prediction'] == 'ANOMALY']) + RESET)  # Show only anomalies
                            self.agent.alerts_anomalias.append((df, 'ANOMALY')) #toDo VERIFICAR ISTO
                        else:
                            print(BLUE + "\nAll clear. No anomalies detected." + RESET)
                    
                    except Exception as e:
                        print(BLUE + "Error during prediction:", str(e) + RESET)
 
            else:
                print(BLUE + "Did not receive any message after 60 seconds" + RESET)