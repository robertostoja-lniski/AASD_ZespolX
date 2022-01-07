import asyncio
import json

from spade.behaviour import CyclicBehaviour
from spade.message import Message

from src.agents.base_agent import BaseAgent
from src.generators.WeatherGenerator import WeatherGenerator
from src.spec import DataType


class WeatherMonitoring(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()
            self.generator = WeatherGenerator()

        async def run(self):
            await super().run()
            contacts = self.agent.presence.get_contacts()
            weather = self.generator.next()
            for contact in contacts:
                if contacts[contact]['subscription'] == 'from':
                    msg = Message(to=str(contact))
                    msg.body = json.dumps({
                        "fishery": self.agent.fishery.name,
                        "data": weather.toJSON()
                    })
                    msg.metadata = {"type": DataType.WEATHER.value}
                    await self.send(msg)
                    self.agent.logger.info('sent weather data: ' + msg.body)
                    await asyncio.sleep(2)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.add_behaviour(self.behaviour)
        await super().setup()

