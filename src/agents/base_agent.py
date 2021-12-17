from spade.agent import Agent
from src.mas_logging import create_logger


class BaseAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = create_logger(self.__class__.__name__)
        self.logger.info('initialization')
        self.agents_to_subscribe = []

    async def setup(self):
        self.add_behaviour(self.Behaviour())

        self.presence.approve_all = True
        self.presence.set_available()
        for jid in self.agents_to_subscribe:
            self.presence.subscribe(jid)

        self.logger.info('is running')