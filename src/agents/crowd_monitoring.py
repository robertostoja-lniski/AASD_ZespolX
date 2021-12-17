import asyncio
from spade.behaviour import CyclicBehaviour
from src.agents.base_agent import BaseAgent


class CrowdMonitoring(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            await asyncio.sleep(1)

    async def setup(self):
        self.agents_to_subscribe = []
        await super().setup()
