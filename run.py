import spade
import asyncio
import sys
from agentes.cordenador import CordenadorAgent
from agentes.monitor import MonitorAgent
from agentes.analise import AnaliseAgent

async def main():
    ip = "10.0.6.1"
    interface1 = "eth2"
    interface2 = "eth3"
    interface3 = "eth4"
    interface_list = [interface1, interface2, interface3]

    flag_init = 0
    if len(sys.argv) > 1:
        if sys.argv[1] == "-s":     # assinaturas
            flag_init = 1
        elif sys.argv[1] == "-a":   # anomalias
            flag_init = 2
        else:                       # normal
            flag_init = 0 

    print(f"Ip: {ip}\nInterface1: {interface1}\nInterface2: {interface2}\nInterface3: {interface3}")

    cordenador = CordenadorAgent(jid=f"cordenador@{ip}", password="NOPASSWORD")
    await cordenador.start()

    analise = AnaliseAgent(jid=f"analise@{ip}", password="NOPASSWORD", agenteCordenador=cordenador.jid, flag_init=flag_init)
    await analise.start()

    monitor = MonitorAgent(jid=f"monitor@{ip}", password="NOPASSWORD", agenteAnalise=analise.jid, ip=ip,interface=interface_list, flag_init=flag_init)
    await monitor.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await monitor.stop()
        await analise.stop()

if __name__ == "__main__":
    spade.run(main())