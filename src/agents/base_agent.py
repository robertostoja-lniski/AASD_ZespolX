from aioxmpp import PresenceShow
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from src.fishery.Fishery import Fishery
from src.mas_logging import create_logger


class BaseAgent(Agent):
    @staticmethod
    def createJID(username: str, host: str):
        return f"{username}@{host}"

    class BaseAgentBehaviour(CyclicBehaviour):
        async def run(self):
            contacts = self.agent.presence.get_contacts()
            for agent in self.agent.agents_to_subscribe:
                if agent.jid not in contacts.keys():
                    # try to subscribe again
                    self.agent.presence.subscribe(str(agent.jid))
            for contact in contacts:
                self.agent.accept_subscription(contacts, contact)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(jid=self.createJID(username, host), password=password)
        self.logger = create_logger(f"{username} ({self.__class__.__name__})")
        self.logger.info('initialization')
        self.agents_to_subscribe = []
        self.behaviour = ...
        self.fishery = ...

    async def setup(self):
        self.presence.approve_all = True
        self.presence.set_available(show=PresenceShow.CHAT)
        for agent in self.agents_to_subscribe:
            self.presence.subscribe(str(agent.jid))

        contacts = self.presence.get_contacts()
        for contact in contacts:
            self.accept_subscription(contacts, contact)

        self.logger.info('is running')

    def accept_subscription(self, contacts, contact):
        if 'ask' in contacts[contact].keys() and contacts[contact]['ask'] == 'subscribe':
            self.presence.approve(str(contact))

    def subscribe_to(self, producers: [Agent]):
        self.agents_to_subscribe.extend(producers)

    def set_fishery(self, fishery: Fishery):
        self.fishery = fishery
