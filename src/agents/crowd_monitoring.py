import asyncio
import random

from spade.behaviour import CyclicBehaviour
from spade.message import Message

from src import spec
from src.agents.base_agent import BaseAgent


class CrowdMonitoring(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            msg = Message(to=spec.data_accumulator)
            msg.body = str(random.randint(0, 22))
            await self.send(msg)
            self.agent.logger.info('sent crowd data: ' + msg.body)
            await asyncio.sleep(1)

    async def setup(self):
        self.agents_to_subscribe = []
        await super().setup()