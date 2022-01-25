import asyncio
import time
from unittest import mock
from unittest.mock import MagicMock

import aiounittest

from src.agents.water_monitoring import WaterMonitoring
from src.agents.weather_monitoring import WeatherMonitoring
from src.fishery.Fishery import Fishery
from src import spec
from test.basic_receive_message_agent import BasicReceiveMessageAgent
from test.spec import MESSAGE_TIMEOUT
from test.util import get_messages_to


class TestWaterCleansing(aiounittest.AsyncTestCase):
    water_quality_monitoring_agent = ...
    weather_monitoring_agent = ...

    @classmethod
    def setUpClass(cls):
        fishery = Fishery('sample_fishery')
        cls.water_quality_monitoring_agent = WaterMonitoring(f"{spec.water_monitoring['username']}_0", spec.password,
                                                             spec.host)
        cls.water_quality_monitoring_agent.set_fishery(fishery)

        cls.weather_monitoring_agent = WeatherMonitoring(f"{spec.weather_monitoring['username']}_0", spec.password,
                                                         spec.host)
        cls.weather_monitoring_agent.set_fishery(fishery)

        cls.water_quality_monitoring_agent.subscribe_to([cls.weather_monitoring_agent])

        cls.water_quality_monitoring_agent.start()
        cls.weather_monitoring_agent.start()

    @classmethod
    def tearDownClass(cls):
        cls.water_quality_monitoring_agent.stop()
        cls.weather_monitoring_agent.stop()

    async def test_should_trigger_cleansing_when_water_quality_is_bad(self):
        basic_receive_agent = BasicReceiveMessageAgent("basic_receive_agent", spec.password, spec.host)
        basic_receive_agent.subscribe_to([TestWaterCleansing.water_quality_monitoring_agent])
        await asyncio.wrap_future(basic_receive_agent.start())

        TestWaterCleansing.water_quality_monitoring_agent.get_water_quality_rating = MagicMock(return_value=WaterMonitoring.WaterQualityRating.BAD)

        with mock.patch.object(TestWaterCleansing.water_quality_monitoring_agent, 'trigger_cleansing',
                               wraps=TestWaterCleansing.water_quality_monitoring_agent.trigger_cleansing) as mocked_setup_cleansing:
            wait_for = 0
            # wait till water_monitoring sends te data data
            while len(get_messages_to(basic_receive_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
                time.sleep(1)
                wait_for += 1
            mocked_setup_cleansing.assert_called()
        await asyncio.wrap_future(basic_receive_agent.stop())

    async def test_should_not_trigger_cleansing_when_water_quality_is_bad(self):
        basic_receive_agent = BasicReceiveMessageAgent("basic_receive_agent", spec.password, spec.host)
        basic_receive_agent.subscribe_to([TestWaterCleansing.water_quality_monitoring_agent])
        await asyncio.wrap_future(basic_receive_agent.start())

        TestWaterCleansing.water_quality_monitoring_agent.get_water_quality_rating = MagicMock(return_value=WaterMonitoring.WaterQualityRating.GOOD)

        with mock.patch.object(TestWaterCleansing.water_quality_monitoring_agent, 'trigger_cleansing',
                               wraps=TestWaterCleansing.water_quality_monitoring_agent.trigger_cleansing) as mocked_setup_cleansing:
            wait_for = 0
            # wait till water_monitoring sends te data data
            while len(get_messages_to(basic_receive_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
                time.sleep(1)
                wait_for += 1
            mocked_setup_cleansing.assert_not_called()
        await asyncio.wrap_future(basic_receive_agent.stop())

