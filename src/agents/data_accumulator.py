import asyncio
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from src import spec
from src.agents.base_agent import BaseAgent

class DataAccumulator(BaseAgent):
    class Behaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if str(msg.sender) == spec.crowd_monitoring:
                self.agent.logger.info('received crowd data: ' + msg.body)
                self.crowd = int(msg.body)

    async def setup(self):
        self.agents_to_subscribe = [spec.weather_monitoring, spec.crowd_monitoring, spec.fish_content_monitoring, spec.water_monitoring]
        await super().setup()


