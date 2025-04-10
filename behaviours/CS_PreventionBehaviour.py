import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import jsonpickle
import subprocess

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

class PreventionBehaviour(CyclicBehaviour):
    async def run(self):
        if self.agent.alerts:
            for ip,type in self.agent.alerts:
                print(RED + f"[Cordenador] A resolver alerta {ip} - {type}" + RESET)

                self.tratar_alerta(ip,type)

    def tratar_alerta(self, ip, type):
        action = self.agent.defense_signatures.get(type)
        
        if action:    
            print(RED + f"[Defesa] {action['description']} em execução para o IP {ip}." + RESET)
            command = action["command"](ip)
            
            for line in command.split("\n"):
                print(RED + f"[Cordenador -> Firewall] A executar: {line}" + RESET)
                subprocess.run(line, shell=True)
                
        else:
            print(RED + f"[Defesa] Tipo de ataque '{type}' não reconhecido." + RESET)
            
        
