import asyncio
import json

from spade.message import Message

from src.agents.base_agent import BaseAgent
from src.generators.CrowdGenerator import CrowdGenerator
from src.spec import DataType, ONTOLOGY, Perfomatives, MSG_LANGUAGE, MessageMetadata


class CrowdMonitoring(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()
            self.generator = CrowdGenerator()

        async def run(self):
            await super().run()
            msg = Message()
            msg.metadata = {
                MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
                MessageMetadata.TYPE.value: DataType.CROWD.value,
                MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
            }
            msg.body = json.dumps({
                "fishery": self.agent.fishery.name,
                "data": str(self.generator.next())
            })
            await self.send_to_all_contacts(msg, lambda contact: self.agent.logger.info('sent crowd data: ' + msg.body))
            await asyncio.sleep(2)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.add_behaviour(self.behaviour)
        await super().setup()
