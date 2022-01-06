from spade.behaviour import CyclicBehaviour

from src.agents.base_agent import BaseAgent


class FisheryRecommender(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            pass

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        await super().setup()
