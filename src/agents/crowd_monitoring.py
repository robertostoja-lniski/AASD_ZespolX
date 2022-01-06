import asyncio
import random

from spade.behaviour import CyclicBehaviour
from spade.message import Message

from src import spec
from src.agents.base_agent import BaseAgent


class CrowdMonitoring(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            msg = Message(to=BaseAgent.createJID(spec.data_accumulator['username'], spec.host))
            msg.body = str(random.randint(0, 22))
            await self.send(msg)
            self.agent.logger.info('sent crowd data: ' + msg.body)
            await asyncio.sleep(1)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        await super().setup()