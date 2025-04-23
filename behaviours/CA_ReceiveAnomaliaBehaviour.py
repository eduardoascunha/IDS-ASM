import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime


RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class ReceiveAnomaliaBehaviour(CyclicBehaviour):

    async def run(self):
        try:
            msg = await self.receive(timeout=10)
            if msg:
                if msg.metadata["performative"] == "inform-fluxo":
                    alert_data = jsonpickle.decode(msg.body)
                    print(RED + f"[Cordenador] Anomalia Recebida: {alert_data}" + RESET)

                    self.agent.alerts_anomalias.append(alert_data)

                    # gera relatorio de anomalias
                    self.relatorio_anomalias(alert_data)
                
                    # ids anomaly based apenas avisa o administrador de rede
                    #self.enviar_email_alerta(alert_data) # nao consegue enviar email por estar a ser rodado no core

            else:
                print(RED + "[Cordenador] Nenhum alerta recebido" + RESET)

        except Exception as e:
            print(RED + f"[Cordenador] Erro ao receber alerta: {e}" + RESET)


    def enviar_email_alerta(self, alert_data):
        try:
            load_dotenv()

            EMAIL_ADDRESS_DEST = os.getenv("EMAIL_ADDRESS_DEST")
            EMAIL_ADDRESS_ORIGIN = os.getenv("EMAIL_ADDRESS_ORIGIN")
            EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

            msg = EmailMessage()
            msg["Subject"] = "ALERTA DE ANOMALIA - IDS"
            msg["From"] = EMAIL_ADDRESS_ORIGIN
            msg["To"] = EMAIL_ADDRESS_DEST
            msg.set_content(f"Foi detetada uma anomalia no sistema:\n{alert_data}")

            # Conectar ao servidor SMTP (Gmail como exemplo)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS_ORIGIN, EMAIL_PASSWORD)
                smtp.send_message(msg)

            print(RED + "[Cordenador] E-mail enviado ao administrador de rede!" + RESET)

        except Exception as e:
            print(RED + f"[Cordenador] Erro ao enviar e-mail: {e}" + RESET)


    def relatorio_anomalias(self, alert_data):    
        try:
            load_dotenv()
            RELATORIO_PATH = os.getenv("RELATORIO_PATH")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(RELATORIO_PATH, "a") as f:
                f.write(f"=== Anomalia Recebida - {timestamp} ===\n")
                
                for chave, valor in alert_data.items():
                    valor_str = str(valor).strip().replace('\n', ' | ')
                    f.write(f"{chave}: {valor_str}\n")
                
                f.write("\n")
                
            print(RED + f"[Cordenador] Relatório atualizado!" + RESET)

        except Exception as e:
            print(RED + f"[Cordenador] Erro ao escrever no relatório: {e}" + RESET)