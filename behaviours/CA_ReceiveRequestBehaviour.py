import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle

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
                    request_data = jsonpickle.decode(msg.body)
                    print(RED + f"[Cordenador] Request Recebido: {request_data}" + RESET)

                    ip = request_data['src_ip']

                    self.tratar_request(ip)

            else:
                print(RED + "[Cordenador] Nenhum request recebido" + RESET)

        except Exception as e:
            print(RED + f"[Cordenador] Erro ao receber request: {e}" + RESET)

    def tratar_request(self, ip):
        print(RED + f"[Defesa] {action['description']} em execução para o IP {ip}." + RESET)
        command = f"sudo iptables -A FORWARD -s {ip} -j DROP\n"
        
        print(RED + f"[Cordenador -> Firewall] A executar: {command}" + RESET)
        subprocess.run(command, shell=True)

        print(RED + f"[Cordenador] Sucesso!" + RESET)


    