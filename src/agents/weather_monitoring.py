from spade.behaviour import CyclicBehaviour
from src.agents.base_agent import BaseAgent


class WeatherMonitoring(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            pass

    async def setup(self):
        self.agents_to_subscribe = []
        await super().setup()

