from src.agents.base_agent import BaseAgent


class DataAccumulator(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)