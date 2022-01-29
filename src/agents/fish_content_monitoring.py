import asyncio
import json
import random
from enum import Enum
from typing import Dict

import jsonpickle
from spade.message import Message
from spade.template import Template

from src.agents.base_agent import BaseAgent
from src.generators.FishContentGenerator import FishContentGenerator
from src.generators.WaterQualityGenerator import WaterQuality
from src.spec import DataType, MessageMetadata, MSG_LANGUAGE, Perfomatives, ONTOLOGY


class FishContentMonitoring(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()
            self.generator = FishContentGenerator()

        async def run(self):
            await super().run()
            water_quality = None
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                water_quality = jsonpickle.decode(body['data'])
            else:
                self.agent.logger.info("Didn't receive any water quality data")

            fish_content = self.generator.next()
            fish_content_rating = self.agent.get_fish_content_rating(water_quality, fish_content)
            msg = Message()
            msg.body = json.dumps({
                "fishery": self.agent.fishery.name,
                "data": json.dumps({
                    "fish_content": fish_content,
                    "fish_content_rating": fish_content_rating.value
                })
            })
            msg.metadata = {
                    MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                    MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
                    MessageMetadata.TYPE.value: DataType.FISH_CONTENT.value,
                    MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
                }
            await self.send_to_all_contacts(msg, lambda contact: self.agent.logger.info('sent fish content data: ' + msg.body))
            await asyncio.sleep(2)

    def __init__(self, username: str, password: str, host: str, verbose: bool):
        super().__init__(username, password, host, verbose)
        self.behaviour = self.Behaviour()

    async def setup(self):
        template = Template()
        template.metadata = {
                    MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                    MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
                    MessageMetadata.TYPE.value: DataType.WATER_QUALITY.value,
                    MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
                }
        self.add_behaviour(self.behaviour, template=template)
        await super().setup()

    def get_fish_content_rating(self, water_quality: WaterQuality, fish_content: Dict[str, int]) -> Enum:

        if sum(fish_content.values()) < 30 and water_quality.temperature > 10:
            return self.FishContentRating.VERY_LOW

        if sum(fish_content.values()) < 30 and water_quality.temperature < 10:
            return self.FishContentRating.LOW

        if 30 <= sum(fish_content.values()) <= 50:
            return self.FishContentRating.AVERAGE

        if sum(fish_content.values()) >= 1000:
            return self.FishContentRating.VERY_HIGH

        return self.FishContentRating(random.choice([e.value for e in FishContentMonitoring.FishContentRating]))

    class FishContentRating(Enum):
        VERY_LOW = 0
        LOW = 0.2
        AVERAGE = 0.4
        DECENT = 0.6
        HIGH = 0.8
        VERY_HIGH = 1

