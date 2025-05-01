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

        maquinas_a_proteger = ["10.0.0.20"]

        if sys.argv[1] == "-s":     # assinaturas
            flag_init = 1
            interface_list = [interface1, interface2, interface3]
            
            cordenadorASSINATURA = CordenadorAgent(jid=f"cordenadorASSINATURA@{ip}", password="NOPASSWORD", maquinas_a_proteger=maquinas_a_proteger,flag_init=flag_init)
            await cordenadorASSINATURA.start()

            analiseASSINATURA = AnaliseAgent(jid=f"analiseASSINATURA@{ip}", password="NOPASSWORD", agenteCordenador=cordenadorASSINATURA.jid, flag_init=flag_init)
            await analiseASSINATURA.start()

            monitorASSINATURA = MonitorAgent(jid=f"monitorASSINATURA@{ip}", password="NOPASSWORD", agenteAnalise=analiseASSINATURA.jid,interface=interface_list, flag_init=flag_init)
            await monitorASSINATURA.start()

        elif sys.argv[1] == "-a":   # anomalias
            flag_init = 2
            interface_list = [interface1]
            
            cordenadorANOMALIA = CordenadorAgent(jid=f"cordenadorANOMALIA@{ip}", password="NOPASSWORD", maquinas_a_proteger=maquinas_a_proteger,flag_init=flag_init)
            await cordenadorANOMALIA.start()

            analiseANOMALIA = AnaliseAgent(jid=f"analiseANOMALIA@{ip}", password="NOPASSWORD", agenteCordenador=cordenadorANOMALIA.jid, flag_init=flag_init)
            await analiseANOMALIA.start()

            monitorANOMALIA = MonitorAgent(jid=f"monitorANOMALIA@{ip}", password="NOPASSWORD", agenteAnalise=analiseANOMALIA.jid,interface=interface_list, flag_init=flag_init)
            await monitorANOMALIA.start()
        
        elif sys.argv[1] == "-asm":   # normal
            flag_init = 0 
            interface_list = [interface1, interface2, interface3]
            
            cordenadorNORMAL = CordenadorAgent(jid=f"cordenadorNORMAL@{ip}", password="NOPASSWORD", maquinas_a_proteger=maquinas_a_proteger, flag_init=flag_init)
            await cordenadorNORMAL.start()

            analiseNORMAL = AnaliseAgent(jid=f"analiseNORMAL@{ip}", password="NOPASSWORD", agenteCordenador=cordenadorNORMAL.jid, flag_init=flag_init)
            await analiseNORMAL.start()

            monitorNORMAL = MonitorAgent(jid=f"monitorNORMAL@{ip}", password="NOPASSWORD", agenteAnalise=analiseNORMAL.jid,interface=interface_list, flag_init=flag_init)
            await monitorNORMAL.start()

        else:
            print("Flag inválida!")
            return

    print(f"Ip: {ip}\nInterfaces: {interface_list}")

    try:
        while True:
            await asyncio.sleep(0.01)
    except KeyboardInterrupt:
        if flag_init == 1:
            await monitorASSINATURA.stop()
            await analiseASSINATURA.stop()
            await cordenadorASSINATURA.stop()
        elif flag_init == 2:
            await monitorANOMALIA.stop()
            await analiseANOMALIA.stop()
            await cordenadorANOMALIA.stop()
        elif flag_init == 0:
            await monitorNORMAL.stop()
            await analiseNORMAL.stop()
            await cordenadorNORMAL.stop()

if __name__ == "__main__":
    spade.run(main())