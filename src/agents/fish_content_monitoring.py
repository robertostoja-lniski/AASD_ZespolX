import asyncio
from spade.behaviour import CyclicBehaviour
from src import spec
from src.agents.base_agent import BaseAgent


class FishContentMonitoring(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            await asyncio.sleep(1)

    async def setup(self):
        self.agents_to_subscribe = [spec.water_monitoring]
        await super().setup()

