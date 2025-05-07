import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import subprocess

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class ReceiveRequestBehaviour(CyclicBehaviour):
    # assinaturas
    async def run(self):
        try:
            msg = await self.receive(timeout=10)
            if msg:
                if msg.metadata["performative"] == 'request':
                    lista_ip_anomalias = jsonpickle.decode(msg.body)
                    print(RED + f"[Cordenador] Request Recebido: {lista_ip_anomalias}" + RESET)

                    self.tratar_request(lista_ip_anomalias)

            else:
                print(RED + "[Cordenador] Nenhum request recebido" + RESET)

        except Exception as e:
            print(RED + f"[Cordenador] Erro ao receber request: {e}" + RESET)

    def tratar_request(self, lista_ips):
        for ip in lista_ips:
            print(RED + f"[Cordenador] A bloquear o IP: {ip}" + RESET)
            command = f"sudo iptables -A FORWARD -s {ip} -j DROP\n"
            
            print(RED + f"[Cordenador -> Firewall] A executar: {command}" + RESET)
            subprocess.run(command, shell=True)


    