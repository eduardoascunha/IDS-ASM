import spade
import asyncio
import sys
import os
from agentes.cordenador import CordenadorAgent
from agentes.monitor import MonitorAgent
from agentes.analise import AnaliseAgent

async def main():
    interface1 = "eth2"
    interface2 = "eth3"
    interface3 = "eth4"

    flag_init = 0
    if len(sys.argv) < 2:
        print("Uso: python3 run.py <flag [-a,-s,-asm]>")
        return
    else:
        #os.system("sudo service openfire start")
        
        ip = "10.0.6.1" # ip do openfire host

        if sys.argv[1] == "-s":     # assinaturas
            flag_init = 1
            interface_list = [interface1, interface2, interface3]
            
            cordenador = CordenadorAgent(jid=f"cordenadorASSINATURA@{ip}", password="NOPASSWORD", flag_init=flag_init)
            await cordenador.start()

            analise = AnaliseAgent(jid=f"analiseASSINATURA@{ip}", password="NOPASSWORD", agenteCordenador=cordenador.jid, flag_init=flag_init)
            await analise.start()

            monitor = MonitorAgent(jid=f"monitorASSINATURA@{ip}", password="NOPASSWORD", agenteAnalise=analise.jid,interface=interface_list, flag_init=flag_init)
            await monitor.start()

        elif sys.argv[1] == "-a":   # anomalias
            flag_init = 2
            interface_list = [interface1]
            
            cordenador = CordenadorAgent(jid=f"cordenadorANOMALIA@{ip}", password="NOPASSWORD", flag_init=flag_init)
            await cordenador.start()

            analise = AnaliseAgent(jid=f"analiseANOMALIA@{ip}", password="NOPASSWORD", agenteCordenador=cordenador.jid, flag_init=flag_init)
            await analise.start()

            monitor = MonitorAgent(jid=f"monitorANOMALIA@{ip}", password="NOPASSWORD", agenteAnalise=analise.jid,interface=interface_list, flag_init=flag_init)
            await monitor.start()
        
        elif sys.argv[1] == "-asm":   # normal
            flag_init = 0 
            interface_list = [interface1, interface2, interface3]
            cordenador = CordenadorAgent(jid=f"cordenadorNORMAL@{ip}", password="NOPASSWORD", flag_init=flag_init)
            await cordenador.start()

            analise = AnaliseAgent(jid=f"analiseNORMAL@{ip}", password="NOPASSWORD", agenteCordenador=cordenador.jid, flag_init=flag_init)
            await analise.start()

            monitor = MonitorAgent(jid=f"monitorNORMAL@{ip}", password="NOPASSWORD", agenteAnalise=analise.jid,interface=interface_list, flag_init=flag_init)
            await monitor.start()

        else:
            print("Flag inválida!")
            return

    print(f"Ip: {ip}\nInterfaces: {interface_list}")

    try:
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        await monitor.stop()
        await analise.stop()

if __name__ == "__main__":
    spade.run(main())