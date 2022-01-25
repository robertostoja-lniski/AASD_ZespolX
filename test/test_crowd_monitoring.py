import asyncio
import time

import aiounittest
from spade.message import Message
from spade.template import Template

from src import spec
from src.agents.crowd_monitoring import CrowdMonitoring
from src.fishery.Fishery import Fishery
from src.spec import MessageMetadata, ONTOLOGY, Perfomatives, DataType, MSG_LANGUAGE
from test.basic_receive_message_agent import BasicReceiveMessageAgent
from test.spec import MESSAGE_TIMEOUT
from test.util import get_messages_to


class TestCrowdMonitoring(aiounittest.AsyncTestCase):
    crowd_monitoring_agent = ...
    @classmethod
    def setUpClass(cls):
        cls.fishery = Fishery('sample_fishery')
        cls.crowd_monitoring_agent = CrowdMonitoring("crowd_monitoring_0", spec.password, spec.host)
        cls.crowd_monitoring_agent.set_fishery(cls.fishery)
        cls.crowd_monitoring_agent.start()

    @classmethod
    def tearDownClass(cls):
        cls.crowd_monitoring_agent.stop()

    async def test_should_send_message_in_timeout(self):
        # Cannot initialize it in setUp, because the tests are run simultanously and the reference to the agent is lost
        basic_receive_agent = BasicReceiveMessageAgent("basic_receive_agent", spec.password, spec.host)
        basic_receive_agent.subscribe_to([TestCrowdMonitoring.crowd_monitoring_agent])
        await asyncio.wrap_future(basic_receive_agent.start())

        wait_for = 0
        while len(get_messages_to(basic_receive_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
            time.sleep(1)
            wait_for += 1

        messages = get_messages_to(basic_receive_agent)
        self.assertTrue(all([isinstance(message, Message) for message in messages]), "Did not receive messages")

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

        while len(get_messages_to(basic_receive_agent)) == 0:
            time.sleep(1)

        messages = get_messages_to(basic_receive_agent)
        self.assertTrue(all([isinstance(message, Message) for message in messages]), "Did not receive all messages")
