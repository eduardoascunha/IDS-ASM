import spade
import asyncio
from monitor import MonitorAgent
from analise import AnaliseAgent

async def main():

    router_ip = "10.0.2.1"

    analise = AnaliseAgent(jid="analise@10.0.2.1", password="NOPASSWORD")
    await analise.start()
    
    monitor = MonitorAgent(jid="monitor@10.0.2.1", password="NOPASSWORD", router_ip=router_ip)
    await monitor.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await monitor.stop()
        await analise.stop()

if __name__ == "__main__":
    spade.run(main())