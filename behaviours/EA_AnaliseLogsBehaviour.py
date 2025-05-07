import asyncio
import spade
import os
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
import re

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
RESET = '\033[0m'

class AnaliseLogsBehaviour(CyclicBehaviour):
    async def run(self):

        if self.agent.logs:
            numero_file = await self.agent.logs.get()

            RELATORIO_PATH = f"{self.agent.RELATORIO_PATH_incomplete}_{numero_file}.txt"

            print(YELLOW + f"[Engenheiro] A analisar log..." + RESET)
            lista = self.parse_log2(RELATORIO_PATH)

            if lista:
                print(YELLOW + f"[Engenheiro] Anomalias encontradas nestes IPs: {lista}" + RESET)
                msg = Message(to=f"{self.agent.agenteCordenador}")
                msg.set_metadata("performative", "request")
                msg.body = jsonpickle.encode(lista)
                await self.send(msg)
            else:
                print(YELLOW + f"[Engenheiro] Nenhuma Log com anomalias" + RESET)

        else:
            print(YELLOW + "[Engenheiro] Nenhum log pra ser analisado" + RESET)

    def parse_log(self, path):
        ips_anomalos = []
        with open(path, 'r') as file:
            lines = file.readlines()
        
        # ignora a primeira linha
        lines = lines[1:]
        
        current_ip = None
        current_log_lines = []
        log_iniciada = False
        
        for line in lines:
            line = line.strip()
            
            # detetar inicio de uma log
            if line.startswith('=== Anomalia Recebida'):
                
                # processar log anterior se existir
                if log_iniciada and current_ip:
                    # calcular tamanho médio das linhas na log atual
                    tamanho_medio = sum(len(l) for l in current_log_lines) / len(current_log_lines) if current_log_lines else 0
                    
                    # se o tamanho medio for maior que 100 caracteres, considera anomala
                    if tamanho_medio > 70:
                        ips_anomalos.append(current_ip)
                
                # iniciar nova log
                current_log_lines = [line]
                current_ip = None
                log_iniciada = True
                
            elif log_iniciada:
                current_log_lines.append(line)
                # extrair IP da fonte
                if line.startswith('Source IP:'):
                    current_ip = line.split(':')[1].strip()
        
        # processar a última log
        if log_iniciada and current_ip:
            tamanho_medio = sum(len(l) for l in current_log_lines) / len(current_log_lines) if current_log_lines else 0
            if tamanho_medio > 70:
                ips_anomalos.append(current_ip)
        
        return ips_anomalos

    def parse_log2(self, path):
        anomalias = []
        
        with open(path, 'r') as f:
            linhas = f.readlines()
    
        entrada_atual = {}
        coletando = False
        
        for linha in linhas[1:]:
            linha = linha.strip()
            
            if linha.startswith("=== Anomalia Recebida"):
                if entrada_atual:
                    if any(v > 100 for v in entrada_atual.get('lengths', [])):
                        anomalias.append(entrada_atual['source_ip'])
                entrada_atual = {'source_ip': None, 'lengths': []}
                coletando = True
                continue
                
            if not coletando:
                continue
                
            if linha.startswith("Source IP:"):
                entrada_atual['source_ip'] = linha.split(": ")[1].strip()
            
            match = re.search(r"Length: (\d+)", linha)
            if match:
                entrada_atual['lengths'].append(int(match.group(1)))
        
        if entrada_atual and any(v > 100 for v in entrada_atual.get('lengths', [])):
            anomalias.append(entrada_atual['source_ip'])
        
        return anomalias

        