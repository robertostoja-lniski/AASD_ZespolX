import asyncio
import json
from enum import Enum

import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from src.agents.base_agent import BaseAgent
from src.generators.WaterQualityGenerator import WaterQualityGenerator, WaterQuality
from src.generators.WeatherGenerator import Weather
from src.spec import DataType


class WaterMonitoring(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()
            self.generator = WaterQualityGenerator()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            water_quality = self.generator.next()
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                weather = jsonpickle.decode(body['data'])
                water_quality_rating = self.agent.get_water_quality_rating(weather, water_quality)
                self.agent.setup_cleansing(water_quality_rating)
            else:
                self.agent.logger.info("Didn't receive any weather data. Water cleansing will not be triggered/ended.")

            msg = Message()
            msg.body = json.dumps({
                "fishery": self.agent.fishery.name,
                "data": jsonpickle.encode(water_quality)
            })
            msg.metadata = {"type": DataType.WATER_QUALITY.value}
            await self.send_to_all_contacts(msg, lambda contact: self.agent.logger.info(
                'sent water quality data: ' + msg.body))
            await asyncio.sleep(2)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.generator = WaterQualityGenerator()
        self.behaviour = self.Behaviour()
        self.cleansing_running = False

    async def setup(self):
        template = Template()
        template.metadata = {"type": DataType.WEATHER.value}
        self.add_behaviour(self.behaviour, template=template)
        await super().setup()

    def get_water_quality_rating(self, weather: Weather, water_quality: WaterQuality) -> Enum:
        # TODO
        return self.WaterQualityRating.BAD

    def trigger_cleansing(self):
        #TODO
        self.logger.info("Triggering water cleansing")
        self.cleansing_running = True

    def stop_cleansing(self):
        #TODO
        self.logger.info("Stopping cleansing")
        self.cleansing_running = False

    def setup_cleansing(self, water_quality_rating):
        if water_quality_rating is self.WaterQualityRating.BAD and not self.cleansing_running:
            self.trigger_cleansing()
        if water_quality_rating is self.WaterQualityRating.GOOD and self.cleansing_running:
            self.stop_cleansing()

    class WaterQualityRating(Enum):
        GOOD = 'Good'
        BAD = 'Bad'


