from spade.behaviour import CyclicBehaviour

from src import spec
from src.agents.base_agent import BaseAgent


class WaterMonitoring(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            pass

    async def setup(self):
        self.agents_to_subscribe = [spec.weather_monitoring]
        await super().setup()

