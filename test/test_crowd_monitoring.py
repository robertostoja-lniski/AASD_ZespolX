import asyncio
import time

import aiounittest
from aioxmpp import PresenceShow
from spade.message import Message
from spade.template import Template

from src import spec
from src.agents.crowd_monitoring import CrowdMonitoring
from src.fishery.Fishery import Fishery
from src.spec import MessageMetadata, ONTOLOGY, Perfomatives, DataType, MSG_LANGUAGE
from test.basic_receive_message_agent import BasicReceiveMessageAgent


class TestCrowdMonitoring(aiounittest.AsyncTestCase):
    crowd_monitoring_agent = ...
    @classmethod
    def setUpClass(cls):
        fishery = Fishery('sample_fishery')
        cls.crowd_monitoring_agent = CrowdMonitoring("crowd_monitoring_0", spec.password, spec.host)
        cls.crowd_monitoring_agent.set_fishery(fishery)
        cls.crowd_monitoring_agent.start()

    async def test_should_send_message_in_timeout(self):
        basic_receive_agent = BasicReceiveMessageAgent("basic_receive_agent", spec.password, spec.host)
        basic_receive_agent.subscribe_to([TestCrowdMonitoring.crowd_monitoring_agent])
        await asyncio.wrap_future(basic_receive_agent.start())

        while basic_receive_agent.presence.state.show == PresenceShow.CHAT:
            time.sleep(1)

        self.assertIsInstance(basic_receive_agent.received_message, Message)

    async def test_should_send_message_in_proper_format(self):
        basic_receive_agent = BasicReceiveMessageAgent("basic_receive_agent", spec.password, spec.host)
        basic_receive_agent.subscribe_to([TestCrowdMonitoring.crowd_monitoring_agent])
        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
            MessageMetadata.TYPE.value: DataType.CROWD.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        basic_receive_agent.behaviour.set_template(template)
        await asyncio.wrap_future(basic_receive_agent.start())

        while basic_receive_agent.presence.state.show == PresenceShow.CHAT:
            time.sleep(1)

        self.assertIsInstance(basic_receive_agent.received_message, Message)


