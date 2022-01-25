from aioxmpp import PresenceShow
from spade.behaviour import OneShotBehaviour

from src.agents.base_agent import BaseAgent
from test.spec import MESSAGE_TIMEOUT


class BasicReceiveMessageAgent(BaseAgent):
    class Behaviour(OneShotBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            msg = await self.receive(timeout=MESSAGE_TIMEOUT)
            if msg is not None:
                self.agent.logger.info("Received message: " + msg.body + " from " + str(msg.sender))
            await self.agent.stop()

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.behaviour = self.Behaviour()

    async def setup(self):
        self.add_behaviour(self.behaviour)
        self.presence.set_available(show=PresenceShow.CHAT)
        await super().setup()
