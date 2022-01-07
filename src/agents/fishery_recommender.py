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
                self.agent.logger.info("Received recommendation request from " + str(msg.sender))
                self.agent.recommendation_requests_queue.add(msg.sender)
                if not self.agent.data_request_sent:
                    msg = Message()
                    msg.metadata = {"type": DataType.DATA_REQUEST.value}
                    await self.send_to_all_contacts(msg, lambda contact: self.agent.logger.info(
                        'sent data request to ' + str(contact)))
                    self.agent.data_request_sent = True

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
                    self.agent.save_recommendation_for_user(requester, recommendation)
                self.agent.recommendation_requests_queue = set([])
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
        self.logger.info("Creating recommendation...")
        return ""

    def save_recommendation_for_user(self, user: JID, recommendation):
        # TODO
        self.logger.info("Saving recommendation for user " + str(user))
        pass
