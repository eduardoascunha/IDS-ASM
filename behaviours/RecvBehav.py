class RecvBehav(CyclicBehaviour):
         async def run(self):
             print("RecvBehav running")
             msg = await self.receive(timeout=120)  # wait for a message for t seconds
             if msg and msg.metadata["performative"] == 'inform-fluxo':
                 print(BLUE,"Received message from sender")
                 flow_info = jsonpickle.decode(msg.body)
                 flow_data = flow_info.get_flow_data()
                 if flow_data:
                     df = pd.DataFrame(flow_data)
                     print(BLUE,"\nReceived DataFrame with shape:", df.shape)
                     print(BLUE,"Sample data:")
                     print(df.head())
 
                     try:
                         # Predict using the loaded model
                         predictions = self.agent.model.predict(df)
                         df['prediction'] = predictions
                         if 1 in predictions or "ANOMALY" in predictions:
                             print(BLUE,"\nAnomaly detected in the incoming flow!")
                             print(df[df['prediction'] == 'ANOMALY'])  # Show only anomalies
                         else:
                             print(BLUE,"\nAll clear. No anomalies detected.")
                     except Exception as e:
                         print(BLUE,"Error during prediction:", str(e))
 
             else:
                 print(BLUE,"Did not receive any message after 60 seconds")
                 self.kill()
 
     async def on_end(self):
         await self.agent.stop()