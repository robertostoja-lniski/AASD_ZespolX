import asyncio
from spade.behaviour import CyclicBehaviour
from src import spec
from src.agents.base_agent import BaseAgent


class ClientReporter(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            pass

    async def setup(self):
        self.agents_to_subscribe = [spec.user, spec.data_accumulator]
        await super().setup()

