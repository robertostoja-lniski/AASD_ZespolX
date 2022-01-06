from aioxmpp import PresenceShow
from spade.agent import Agent

from src.fishery.Fishery import Fishery
from src.mas_logging import create_logger


class BaseAgent(Agent):
    @staticmethod
    def createJID(username: str, host: str):
        return f"{username}@{host}"

    def __init__(self, username: str, password: str, host: str):
        super().__init__(jid=self.createJID(username, host), password=password)
        self.logger = create_logger(f"{username} ({self.__class__.__name__})")
        self.logger.info('initialization')
        self.agents_to_subscribe = []
        self.behaviour = ...
        self.fishery = ...

    async def setup(self):
        self.add_behaviour(self.behaviour)
        self.presence.approve_all = True
        self.presence.set_available()
        for agent in self.agents_to_subscribe:
            self.presence.subscribe(str(agent.jid))

        contacts = self.presence.get_contacts()
        for contact in contacts:
            if 'ask' in contacts[contact].keys() and contacts[contact]['ask'] == 'subscription':
                self.presence.approve(str(contact))

        self.logger.info('is running')

    def subscribe_to(self, producers: [Agent]):
        self.agents_to_subscribe.extend(producers)

    def set_fishery(self, fishery: Fishery):
        self.fishery = fishery
