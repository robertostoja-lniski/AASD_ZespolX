import json
from typing import Dict

from spade.behaviour import CyclicBehaviour

from src.agents.base_agent import BaseAgent


class DataAccumulator(BaseAgent):
    class Behaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.data = {}

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = body['type']
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if type not in self.data.keys():
                    self.data[type] = {}
                self.data[type][sender] = body['data']
                self.agent.set_data(self.data)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()
        self.data = {}

    def set_data(self, data: Dict):
        self.data = data

    async def setup(self):
        await super().setup()


