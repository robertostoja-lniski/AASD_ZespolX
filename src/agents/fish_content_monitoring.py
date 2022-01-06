import asyncio
import json
from enum import Enum

from spade.behaviour import CyclicBehaviour
from spade.message import Message

from src import spec
from src.agents.base_agent import BaseAgent
from src.generators.FishContentGenerator import FishContentGenerator
from src.generators.WaterQualityGenerator import WaterQuality
from src.spec import DataType


class FishContentMonitoring(BaseAgent):
    class Behaviour(CyclicBehaviour):

        def __init__(self):
            super().__init__()
            self.generator = FishContentGenerator()

        async def run(self):
            water_quality = None
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                water_quality = WaterQuality.deserialize(body['data'])
            else:
                self.agent.logger.info("Didn't receive any water quality data")

            fish_content = self.generator.next()
            fish_content_rating = self.agent.get_fish_content_rating(water_quality, fish_content)
            contacts = self.agent.presence.get_contacts()
            for contact in contacts:
                if contacts[contact]['subscription'] == 'from':
                    msg = Message(to=str(contact))
                    msg.body = json.dumps({
                        "type": DataType.FISH_CONTENT.value,
                        "fishery": self.agent.fishery.name,
                        "data": fish_content_rating.value
                    })
                    await self.send(msg)
                    self.agent.logger.info('sent fish content data: ' + msg.body)
                    await asyncio.sleep(2)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        await super().setup()

    def get_fish_content_rating(self, water_quality: WaterQuality, fish_content: int) -> Enum:
        # TODO
        return self.FishContentRating.AVERAGE

    class FishContentRating(Enum):
        VERY_LOW = 'Very low'
        LOW = 'Low'
        AVERAGE = 'Average'
        DECENT = 'Decent'
        HIGH = 'High'
        VERY_HIGH = 'Very high'

