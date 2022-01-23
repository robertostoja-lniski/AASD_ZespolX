import asyncio

import keyboard
from spade.message import Message

from src.agents.base_agent import BaseAgent
from src.spec import DataType, MessageMetadata, MSG_LANGUAGE, Perfomatives, ONTOLOGY


class User(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        async def run(self):
            await super().run()
            if keyboard.is_pressed('f'):
                self.agent.logger.info('f key has been pressed, generating recommendation')
                msg = Message()
                msg.metadata = {
                    MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                    MessageMetadata.PERFOMATIVE.value: Perfomatives.REQUEST.value,
                    MessageMetadata.TYPE.value: DataType.RECOMMENDATION_REQUEST.value,
                    MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
                }
                await self.send_to_all_contacts(msg, lambda contact: self.agent.logger.info(
                    'sent recommendation request to ' + str(contact)))

            elif keyboard.is_pressed('r'):
                self.agent.logger.info('r key has been pressed, generating report')
                await asyncio.sleep(1)
                # send message to client reporter and print report

            await asyncio.sleep(0.5)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.add_behaviour(self.behaviour)
        await super().setup()



