import asyncio
import time

import aiounittest
from spade.message import Message
from spade.template import Template

from src import spec
from src.agents.water_monitoring import WaterMonitoring
from src.agents.weather_monitoring import WeatherMonitoring
from src.fishery.Fishery import Fishery
from src.spec import DataType, MessageMetadata, ONTOLOGY, Perfomatives, MSG_LANGUAGE
from test.basic_receive_message_agent import BasicReceiveMessageAgent
from test.spec import MESSAGE_TIMEOUT
from test.util import get_messages_to


class TestWaterQualityMonitoring(aiounittest.AsyncTestCase):
    water_quality_monitoring_agent = ...
    weather_monitoring_agent = ...

    @classmethod
    def setUpClass(cls):
        fishery = Fishery('sample_fishery')
        cls.water_quality_monitoring_agent = WaterMonitoring(f"{spec.water_monitoring['username']}_0", spec.password, spec.host)
        cls.water_quality_monitoring_agent.set_fishery(fishery)

        cls.weather_monitoring_agent = WeatherMonitoring(f"{spec.weather_monitoring['username']}_0", spec.password, spec.host)
        cls.weather_monitoring_agent.set_fishery(fishery)

        cls.water_quality_monitoring_agent.subscribe_to([cls.weather_monitoring_agent])

        cls.water_quality_monitoring_agent.start()
        cls.weather_monitoring_agent.start()

    @classmethod
    def tearDownClass(cls):
        cls.water_quality_monitoring_agent.stop()
        cls.weather_monitoring_agent.stop()

    async def test_should_send_message_in_timeout_even_without_weather_data(self):
        basic_receive_agent = BasicReceiveMessageAgent("basic_receive_agent", spec.password, spec.host)
        basic_receive_agent.subscribe_to([TestWaterQualityMonitoring.water_quality_monitoring_agent])
        await asyncio.wrap_future(basic_receive_agent.start())

        wait_for = 0
        while len(get_messages_to(basic_receive_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
            time.sleep(1)
            wait_for += 1

        messages = get_messages_to(basic_receive_agent)
        self.assertTrue(all([isinstance(message, Message) for message in messages]), "Did not receive messages")

    async def test_should_send_message_in_proper_format(self):
        basic_receive_agent = BasicReceiveMessageAgent("basic_receive_agent", spec.password, spec.host)
        basic_receive_agent.subscribe_to([TestWaterQualityMonitoring.water_quality_monitoring_agent])
        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
            MessageMetadata.TYPE.value: DataType.WATER_QUALITY.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        basic_receive_agent.behaviour.set_template(template)
        await asyncio.wrap_future(basic_receive_agent.start())

        wait_for = 0
        while len(get_messages_to(basic_receive_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
            time.sleep(1)
            wait_for += 1

        messages = get_messages_to(basic_receive_agent)
        self.assertTrue(all([isinstance(message, Message) for message in messages]), "Did not receive messages")

    async def test_should_receive_weather_data_in_timeout_limit(self):
        wait_for = 0
        while len(get_messages_to(TestWaterQualityMonitoring.water_quality_monitoring_agent)) == 0 and wait_for < MESSAGE_TIMEOUT:
            time.sleep(1)
            wait_for += 1

        self.assertTrue(len(get_messages_to(TestWaterQualityMonitoring.water_quality_monitoring_agent)) > 0)
        self.assertTrue(all([event.metadata['type'] == DataType.WEATHER.value for event in get_messages_to(TestWaterQualityMonitoring.water_quality_monitoring_agent)]))



