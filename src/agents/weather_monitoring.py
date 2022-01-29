import asyncio
import json

import jsonpickle as jsonpickle
from spade.message import Message

from src.agents.base_agent import BaseAgent
from src.generators.WeatherGenerator import WeatherGenerator
from src.spec import DataType, MSG_LANGUAGE, Perfomatives, ONTOLOGY, MessageMetadata


class WeatherMonitoring(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()
            self.generator = WeatherGenerator()

        async def run(self):
            await super().run()
            weather = self.generator.next()
            msg = Message()
            msg.body = json.dumps({
                "fishery": self.agent.fishery.name,
                "data": jsonpickle.encode(weather)
            })
            msg.metadata = {
                MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
                MessageMetadata.TYPE.value: DataType.WEATHER.value,
                MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
            }
            await self.send_to_all_contacts(msg, lambda contact: self.agent.logger.info('sent weather data: ' + msg.body))
            await asyncio.sleep(2)

    def __init__(self, username: str, password: str, host: str, verbose: bool):
        super().__init__(username, password, host, verbose)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.add_behaviour(self.behaviour)
        await super().setup()

