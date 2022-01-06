from spade.behaviour import CyclicBehaviour

from src import spec
from src.agents.base_agent import BaseAgent


class ClientReporter(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            pass

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.agents_to_subscribe = [spec.user, spec.data_accumulator]
        await super().setup()

