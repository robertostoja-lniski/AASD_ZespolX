import time

import aiounittest

from src import spec
from src.agents.crowd_monitoring import CrowdMonitoring
from src.agents.data_accumulator import DataAccumulator
from src.agents.fish_content_monitoring import FishContentMonitoring
from src.agents.water_monitoring import WaterMonitoring
from src.agents.weather_monitoring import WeatherMonitoring
from src.fishery.Fishery import Fishery
from src.spec import DataType
from test.spec import MESSAGE_TIMEOUT
from test.util import get_messages_to_from


class TestDataAccumulator(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.fishery = Fishery('sample_fishery')
        cls.data_accumulator_agent = DataAccumulator(f"{spec.data_accumulator['username']}", spec.password, spec.host)
        cls.data_accumulator_agent.start()

        cls.water_monitoring_agent = WaterMonitoring(f"{spec.water_monitoring['username']}_0",
                                                     spec.password, spec.host)
        cls.water_monitoring_agent.set_fishery(cls.fishery)

        cls.fish_content_monitoring_agent = FishContentMonitoring(f"{spec.fish_content_monitoring['username']}_0",
                                                                  spec.password, spec.host)
        cls.fish_content_monitoring_agent.set_fishery(cls.fishery)
        cls.fish_content_monitoring_agent.subscribe_to([cls.water_monitoring_agent])

        cls.weather_monitoring_agent = WeatherMonitoring(f"{spec.weather_monitoring['username']}_0",
                                                         spec.password, spec.host)
        cls.weather_monitoring_agent.set_fishery(cls.fishery)
        cls.water_monitoring_agent.subscribe_to([cls.weather_monitoring_agent])

        cls.crowd_monitoring_agent = CrowdMonitoring(f"{spec.crowd_monitoring['username']}_0", spec.password, spec.host)
        cls.crowd_monitoring_agent.set_fishery(cls.fishery)

        cls.data_accumulator_agent.subscribe_to(
            [cls.water_monitoring_agent, cls.fish_content_monitoring_agent, cls.weather_monitoring_agent,
             cls.crowd_monitoring_agent])

        for agent in [cls.water_monitoring_agent, cls.fish_content_monitoring_agent, cls.weather_monitoring_agent,
             cls.crowd_monitoring_agent]:
            agent.start()

    @classmethod
    def tearDownClass(cls):
        cls.data_accumulator_agent.stop()
        cls.water_monitoring_agent.stop()
        cls.fish_content_monitoring_agent.stop()
        cls.weather_monitoring_agent.stop()
        cls.crowd_monitoring_agent.stop()

    async def test_should_receive_weather_data_in_timeout_limit(self):
        wait_for = 0
        while len(get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                       TestDataAccumulator.weather_monitoring_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
            time.sleep(1)
            wait_for += 1

        self.assertTrue(len(get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                                 TestDataAccumulator.weather_monitoring_agent)) > 0, "Did not receive any message from weather_monitoring_agent")

        self.assertTrue(all([event.metadata['type'] == DataType.WEATHER.value for event in
                             get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                                  TestDataAccumulator.weather_monitoring_agent)]), "Message type from weather_monitoring_agent is not correct")

    async def test_should_receive_water_data_in_timeout_limit(self):
        wait_for = 0
        while len(get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                       TestDataAccumulator.water_monitoring_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
            time.sleep(1)
            wait_for += 1

        self.assertTrue(len(get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                                 TestDataAccumulator.water_monitoring_agent)) > 0, "Did not receive any message from water_monitoring_agent.")

        self.assertTrue(all([event.metadata['type'] == DataType.WATER_QUALITY.value for event in
                             get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                                  TestDataAccumulator.water_monitoring_agent)]), "Message type from water_monitoring_agent is not correct.")

    async def test_should_receive_fish_content_data_in_timeout_limit(self):
        wait_for = 0
        while len(get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                       TestDataAccumulator.fish_content_monitoring_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
            time.sleep(1)
            wait_for += 1

        self.assertTrue(len(get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                                 TestDataAccumulator.fish_content_monitoring_agent)) > 0, "Did not receive any message from fish_content_monitoring_agent.")

        self.assertTrue(all([event.metadata['type'] == DataType.FISH_CONTENT.value for event in
                             get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                                  TestDataAccumulator.fish_content_monitoring_agent)]), "Message type from fish_content_monitoring_agent is not correct.")

    async def test_should_receive_crowd_data_in_timeout_limit(self):
        wait_for = 0
        while len(get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                       TestDataAccumulator.crowd_monitoring_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
            time.sleep(1)
            wait_for += 1

        self.assertTrue(len(get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                                 TestDataAccumulator.crowd_monitoring_agent)) > 0, "Did not receive any message from crowd_monitoring_agent.")

        self.assertTrue(all([event.metadata['type'] == DataType.CROWD.value for event in
                             get_messages_to_from(TestDataAccumulator.data_accumulator_agent,
                                                  TestDataAccumulator.crowd_monitoring_agent)]), "Message type from crowd_monitoring_agent is not correct.")
