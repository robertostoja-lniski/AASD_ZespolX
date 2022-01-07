import json

from spade.template import Template

from src.agents.base_agent import BaseAgent
from src.generators.WaterQualityGenerator import WaterQuality
from src.generators.WeatherGenerator import Weather
from src.spec import DataType


class DataAccumulator(BaseAgent):
    class ReceiveWaterQualityBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = DataType.WATER_QUALITY.value
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if type not in self.agent.data.keys():
                    self.agent.data[type] = {}

                self.agent.data[type][sender] = WaterQuality.deserialize(body['data'])

    class ReceiveWeatherBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = DataType.WEATHER.value
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if type not in self.agent.data.keys():
                    self.agent.data[type] = {}

                self.agent.data[type][sender] = Weather.deserialize(body['data'])

    class ReceiveCrowdBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = DataType.CROWD.value
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if type not in self.agent.data.keys():
                    self.agent.data[type] = {}

                self.agent.data[type][sender] = body['data']

    class ReceiveFishContentBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = DataType.FISH_CONTENT.value
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if type not in self.agent.data.keys():
                    self.agent.data[type] = {}

                self.agent.data[type][sender] = json.loads(body['data'])

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.receive_water_quality_behaviour = self.ReceiveWaterQualityBehaviour()
        self.receive_weather_behaviour = self.ReceiveWeatherBehaviour()
        self.receive_crowd_behaviour = self.ReceiveCrowdBehaviour()
        self.receive_fish_content_behaviour = self.ReceiveFishContentBehaviour()
        self.data = {}

    async def setup(self):
        template = Template()
        template.metadata = {"type": DataType.WATER_QUALITY.value}
        self.add_behaviour(self.receive_water_quality_behaviour, template=template)

        template = Template()
        template.metadata = {"type": DataType.WEATHER.value}
        self.add_behaviour(self.receive_weather_behaviour, template=template)

        template = Template()
        template.metadata = {"type": DataType.CROWD.value}
        self.add_behaviour(self.receive_crowd_behaviour, template=template)

        template = Template()
        template.metadata = {"type": DataType.FISH_CONTENT.value}
        self.add_behaviour(self.receive_fish_content_behaviour, template=template)
        await super().setup()


