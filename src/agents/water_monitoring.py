import asyncio
import json

from spade.behaviour import CyclicBehaviour
from spade.message import Message

from src import spec
from src.agents.base_agent import BaseAgent
from src.generators.WaterQualityGenerator import WaterQualityGenerator
from src.spec import DataType


class WaterMonitoring(BaseAgent):
    class Behaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.generator = WaterQualityGenerator()

        async def run(self):
            msg = Message(to=BaseAgent.createJID(spec.data_accumulator['username'], spec.host))
            msg.body = json.dumps({
                "type": str(DataType.WATER),
                "fishery": self.agent.fishery.name,
                "data": str(self.generator.next())
            })
            await self.send(msg)
            self.agent.logger.info('sent water quality data: ' + msg.body)
            await asyncio.sleep(1)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        await super().setup()

