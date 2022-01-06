import json

from spade.behaviour import CyclicBehaviour

from src.agents.base_agent import BaseAgent


class DataAccumulator(BaseAgent):
    class Behaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.crowd = {}

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                self.agent.logger.info('received crowd data: ' + body['data'] + " from " + sender + " for fishery: " + body['fishery'])
                self.crowd[sender] = int(body['data'])
                self.agent.set_crowd(self.crowd, sender)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()
        self.crowd = {}

    def set_crowd(self, crowd: int, sender_jid_str: str):
        self.crowd[sender_jid_str] = crowd

    async def setup(self):
        await super().setup()


