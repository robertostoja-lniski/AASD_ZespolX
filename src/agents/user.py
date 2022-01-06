import asyncio
from datetime import datetime

import keyboard
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour

from src import spec
from src.agents.base_agent import BaseAgent


def quit_spade():
    pass


class User(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            if keyboard.is_pressed('f'):
                self.agent.logger.info('f key has been pressed, generating recommendation')
                await asyncio.sleep(1)
                # send message to fishery recommender and print recommendation
                return
            elif keyboard.is_pressed('r'):
                self.agent.logger.info('r key has been pressed, generating report')
                await asyncio.sleep(1)
                # send message to client reporter and print report
                return

            await asyncio.sleep(0.1)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        await super().setup()



