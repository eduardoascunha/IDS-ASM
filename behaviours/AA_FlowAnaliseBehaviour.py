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

class FlowAnaliseBehaviour(CyclicBehaviour):
    async def run(self):

        if self.agent.recent_flows:
            flow_data_dict = await self.agent.recent_flows.get()

            for ip, flow_data in flow_data_dict.items():
                df = pd.DataFrame(flow_data)
                print(BLUE + "[Analise] DataFrame recebido com shape:", str(df.shape) + RESET)
                print(BLUE + "[Analise] Sample data:" + RESET)
                print(BLUE + str(df.head()) + RESET)

                try:
                    # Save the DataFrame to a CSV file
                    file_path = "anomalyModel/data/csvs/flow_data_clean_v2.csv"

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
                            'Source IP': ip,
                            'Destination Port': df["Destination Port"],
                            'Flow Duration': df["Flow Duration"],
                            'Total Fwd Packets': df["Total Fwd Packets"],
                            'Flow Bytes/s': df["Flow Bytes/s"],
                            'SYN Flag Count': df["SYN Flag Count"],
                            'RST Flag Count': df["RST Flag Count"],
                            'FIN Flag Count': df["FIN Flag Count"],
                            'ACK Flag Count': df["ACK Flag Count"],
                            'Average Packet Size': df["Average Packet Size"],
                        })

                    else:
                        print(BLUE + "\n[Analise] Tudo Ok. Nenhuma anomalia detetada." + RESET)
                
                except Exception as e:
                    print(BLUE + "[Analise] Erro na predicao:", str(e) + RESET)
        
        else:
            print(BLUE + "[Analise] Nenhum fluxo a ser analisado" + RESET)