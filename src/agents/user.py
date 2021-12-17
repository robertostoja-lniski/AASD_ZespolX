import asyncio

import keyboard
from spade.behaviour import CyclicBehaviour

from src.agents.base_agent import BaseAgent


class UserAgent(BaseAgent):
    class UserBehaviour(CyclicBehaviour):
        async def run(self):
            if keyboard.is_pressed('f'):
                self.logger.info('f key has been pressed, generating recommendation')
                await asyncio.sleep(1)
                # send message to fishery recommender and print recommendation
                return
            elif keyboard.is_pressed('r'):
                self.logger.info('r key has been pressed, generating report')
                await asyncio.sleep(1)
                # send message to client reporter and print report
                return

    async def setup(self):
        super().setup()
        b = self.UserBehaviour()
        self.add_behaviour(b)
