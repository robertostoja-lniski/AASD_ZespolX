from src.agents.base_agent import BaseAgent


class WaterMonitoring(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup(self):
        self.logger.info('is running')