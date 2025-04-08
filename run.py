import spade
import asyncio
import sys
from agentes.cordenador import CordenadorAgent
from agentes.monitor import MonitorAgent
from agentes.analise import AnaliseAgent

async def main():
    if len(sys.argv) == 1:
        ip = "10.0.6.1"
        interface = "eth2"
    elif len(sys.argv) == 2:
        ip = sys.argv[1]
        interface = "eth2"
    elif len(sys.argv) >= 3:
        ip = sys.argv[1]
        interface = sys.argv[2]

    print(f"Ip: {ip}\nInterface: {interface}")

    cordenador = CordenadorAgent(jid=f"cordenador@{ip}", password="NOPASSWORD")
    await cordenador.start()

    analise = AnaliseAgent(jid=f"analise@{ip}", password="NOPASSWORD", agenteCordenador=cordenador.jid)
    await analise.start()

    monitor = MonitorAgent(jid=f"monitor@{ip}", password="NOPASSWORD", agenteAnalise=analise.jid, ip=ip,interface=interface)
    await monitor.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await monitor.stop()
        await analise.stop()

if __name__ == "__main__":
    spade.run(main())