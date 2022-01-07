import asyncio
import json
from datetime import datetime

import keyboard
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message

from src import spec
from src.agents.base_agent import BaseAgent
from src.spec import DataType


def quit_spade():
    pass


class User(BaseAgent):
    class Behaviour(BaseAgent.BaseAgentBehaviour):
        async def run(self):
            await super().run()
            if keyboard.is_pressed('f'):
                self.agent.logger.info('f key has been pressed, generating recommendation')
                contacts = self.agent.presence.get_contacts()
                for contact in contacts:
                    if 'subscription' in contacts[contact].keys() and contacts[contact]['subscription'] == 'from':
                        msg = Message(to=str(contact))
                        msg.metadata = {"type": DataType.RECOMMENDATION_REQUEST.value}
                        await self.send(msg)
                        self.agent.logger.info('sent recommendation request to ' + str(contact))
            elif keyboard.is_pressed('r'):
                self.agent.logger.info('r key has been pressed, generating report')
                await asyncio.sleep(1)
                # send message to client reporter and print report

            await asyncio.sleep(0.1)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.add_behaviour(self.behaviour)
        await super().setup()



