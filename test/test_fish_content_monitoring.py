import asyncio

import time
import unittest

import aiounittest
from aioxmpp import PresenceShow
from spade.message import Message

from src import spec
from src.agents.fish_content_monitoring import FishContentMonitoring
from src.agents.water_monitoring import WaterMonitoring
from src.fishery.Fishery import Fishery
from src.spec import DataType
from test.basic_receive_message_agent import BasicReceiveMessageAgent


class TestFishContentMonitoring(aiounittest.AsyncTestCase):
    fish_content_monitoring_agent = ...
    @classmethod
    def setUpClass(cls):
        fishery = Fishery('sample_fishery')
        cls.fish_content_monitoring_agent = FishContentMonitoring("fish_content_monitoring_0", spec.password, spec.host)
        cls.fish_content_monitoring_agent.set_fishery(fishery)
        cls.fish_content_monitoring_agent.start()

        cls.water_quality_data_agent = WaterMonitoring("water_monitoring_0", spec.password, spec.host)
        cls.water_quality_data_agent.set_fishery(fishery)
        cls.water_quality_data_agent.start()

        cls.fish_content_monitoring_agent.subscribe_to([cls.water_quality_data_agent])

    async def test_should_send_message_in_timeout(self):
        basic_receive_agent = BasicReceiveMessageAgent("basic_receive_agent", spec.password, spec.host)
        basic_receive_agent.subscribe_to([TestFishContentMonitoring.fish_content_monitoring_agent])
        await asyncio.wrap_future(basic_receive_agent.start())

        while basic_receive_agent.presence.state.show == PresenceShow.CHAT:
            time.sleep(1)

        self.assertIsInstance(basic_receive_agent.received_message, Message)

    async def test_should_receive_water_quality_data(self):
        received = [msg for msg in TestFishContentMonitoring.fish_content_monitoring_agent.traces.all() if msg[1].to == TestFishContentMonitoring.fish_content_monitoring_agent.jid]
        wait_for = 0
        while len(received) == 0 and wait_for < 10:
            time.sleep(3)
            received = [msg for msg in
                        TestFishContentMonitoring.fish_content_monitoring_agent.traces.all() if msg[1].to == TestFishContentMonitoring.fish_content_monitoring_agent.jid]
            wait_for += 1

        self.assertTrue(len(received) > 0)
        self.assertTrue(all([event[1].metadata['type'] == DataType.WATER_QUALITY.value for event in received]))

