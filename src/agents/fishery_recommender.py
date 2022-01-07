import json

from aioxmpp import JID
from spade.message import Message
from spade.template import Template

from src.agents.base_agent import BaseAgent
from src.spec import DataType


class FisheryRecommender(BaseAgent):
    class HandleRecommendationRequestBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                self.agent.recommendation_requests_queue.add(msg.sender)
                if not self.agent.data_request_sent:
                    contacts = self.agent.presence.get_contacts()
                    for contact in contacts:
                        if contacts[contact]['subscription'] == 'from':
                            msg = Message(to=str(contact))
                            msg.metadata = {"type": DataType.DATA_REQUEST.values}
                            await self.send(msg)
                            self.agent.data_request_sent = True
                            self.agent.logger.info('sent data request to ' + str(contact))

    class HandleDataResponseBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                data = json.loads(msg.body)['data']
                recommendation = self.agent.get_recommendation(data)
                for requester in self.agent.recommendation_requests_queue:
                    self.agent.save_recommandation_for_user(requester, recommendation)
                    self.agent.recommendation_requests_queue.discard(requester)
                self.agent.data_request_sent = False

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.recommendation_request_behaviour = self.HandleRecommendationRequestBehaviour()
        self.data_response_behaviour = self.HandleDataResponseBehaviour()
        self.recommendation_requests_queue = set([])
        self.data_request_sent = False

    async def setup(self):
        template = Template()
        template.metadata = {"type": DataType.RECOMMENDATION_REQUEST.value}
        self.add_behaviour(self.recommendation_request_behaviour, template=template)
        template = Template()
        template.metadata = {"type": DataType.DATA_RESPONSE.value}
        self.add_behaviour(self.data_response_behaviour, template=template)
        await super().setup()

    def get_recommendation(self, data):
        # TODO
        print("Creating recommendation...")
        return ""

    def save_recommandation_for_user(self, user: JID, recommendation):
        # TODO
        print("Saving recommendation for user " + str(user))
        pass
