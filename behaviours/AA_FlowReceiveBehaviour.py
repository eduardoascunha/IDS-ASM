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
            #print(BLUE + "FlowReceiveBehaviour a correr!" + RESET)
            msg = await self.receive(timeout=60)  # wait for a message for t seconds
            if msg and msg.metadata["performative"] == 'inform-fluxo':
                print(BLUE + "[Analise] Mensagem recebida do sender" + RESET)
                flow_info = jsonpickle.decode(msg.body)
                flow_data = flow_info.get_flow_data()
                if flow_data:
                    df = pd.DataFrame(flow_data)
                    print(BLUE + "[Analise] DataFrame recebido com shape:", str(df.shape) + RESET)
                    print(BLUE + "[Analise] Sample data:" + RESET)
                    print(BLUE + str(df.head()) + RESET)

                    try:
                        # Save the DataFrame to a CSV file
                        file_path = "anomalyModel/data/csvs/flow_data_clean.csv"

                        if not os.path.exists(file_path):
                            df.to_csv(file_path, index=False)
                            print(BLUE + "\n[Analise] DataFrame guardado para o CSV file" + RESET)
                        
                        else:
                            df.to_csv(file_path, index=False, mode='a', header=False)
                            print(BLUE + "\n[Analise] DataFrame appended para o CSV file" + RESET)

                        # Predict using the loaded model
                        predictions = self.agent.model.predict(df)

                        predictions = np.where(predictions == 1, "BENIGN", "ANOMALY")

                        df['prediction'] = predictions
                        
                        if "ANOMALY" in predictions:
                            print(BLUE + "\n[Analise] Anomalia detetada no fluxo!" + RESET)
                            print(BLUE + str(df[df['prediction'] == 'ANOMALY']) + RESET)  # Show only anomalies
                            
                            self.agent.alerts_anomalias.append({
                                'Destination Port': df["Destination Port"],
                                'Flow Duration': df["Flow Duration"],
                                'Total Fwd Packets': df["Total Fwd Packets"],
                                'Total Backward Packets': df["Total Backward Packets"],
                                'Total Length of Fwd Packets': df["Total Length of Fwd Packets"],
                                'Total Length of Bwd Packets': df["Total Length of Bwd Packets"],
                                'Flow Bytes/s': df["Flow Bytes/s"],
                                'Flow Packets/s': df["Flow Packets/s"],
                                'Fwd Packet Length Std': df["Fwd Packet Length Std"],
                                'Bwd Packet Length Std': df["Bwd Packet Length Std"],
                                'Packet Length Variance': df["Packet Length Variance"],
                                'SYN Flag Count': df["SYN Flag Count"],
                                'RST Flag Count': df["RST Flag Count"],
                                'FIN Flag Count': df["FIN Flag Count"],
                                'ACK Flag Count': df["ACK Flag Count"],
                                'Flow IAT Mean': df["Flow IAT Mean"],
                                'Flow IAT Std': df["Flow IAT Std"],
                                'Down/Up Ratio': df["Down/Up Ratio"],
                                'Average Packet Size': df["Average Packet Size"],
                                'Active Mean': df["Active Mean"],
                                'Idle Mean': df["Idle Mean"]
                            })

                        else:
                            print(BLUE + "\n[Analise] Tudo Ok. Nenhuma anomalia detetada." + RESET)
                    
                    except Exception as e:
                        print(BLUE + "[Analise] Erro na predicao:", str(e) + RESET)
 
            else:
                print(BLUE + "[Analise] Nenhuma mensagem recebida em 60 segundos" + RESET)