from typing import Callable

from spade.behaviour import CyclicBehaviour

from src.agents.base_agent import BaseAgent


class DataAccumulator(BaseAgent):
    class Behaviour(CyclicBehaviour):
        def __init__(self, set_crowd: Callable):
            super().__init__()
            self.crowd = ...
            self.set_crowd = set_crowd

        async def run(self):
            msg = await self.receive(timeout=10)
            self.agent.logger.info('received crowd data: ' + msg.body)
            self.crowd = int(msg.body)
            self.set_crowd(self.crowd)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour(self.set_crowd)
        self.crowd = 0

    def set_crowd(self, crowd: int):
        self.crowd = crowd

    async def setup(self):
        await super().setup()


