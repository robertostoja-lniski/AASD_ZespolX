import asyncio
import json

from spade.message import Message

from src.agents.base_agent import BaseAgent
from src.generators.CrowdGenerator import CrowdGenerator
from src.spec import DataType


class CrowdMonitoring(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()
            self.generator = CrowdGenerator()

        async def run(self):
            await super().run()
            contacts = self.agent.presence.get_contacts()
            for contact in contacts:
                if contacts[contact]['subscription'] == 'from':
                    msg = Message(to=str(contact))
                    msg.body = json.dumps({
                        "fishery": self.agent.fishery.name,
                        "data": str(self.generator.next())
                    })
                    msg.metadata = {"type": DataType.CROWD.value}
                    await self.send(msg)
                    self.agent.logger.info('sent crowd data: ' + msg.body)
                    await asyncio.sleep(2)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.add_behaviour(self.behaviour)
        await super().setup()
