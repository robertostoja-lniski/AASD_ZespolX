import json

import jsonpickle
from spade.message import Message
from spade.template import Template

from src.agents.base_agent import BaseAgent
from src.spec import DataType, MessageMetadata, ONTOLOGY, Perfomatives, MSG_LANGUAGE


class DataAccumulator(BaseAgent):
    class ReceiveWaterQualityBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = msg.metadata['type']
                fishery = body['fishery']

                is_opened = body['opened']
                if not is_opened:
                    self.agent.closed_fisheries.add(fishery)

                if is_opened and fishery in self.agent.closed_fisheries:
                    self.agent.closed_fisheries.remove(fishery)

                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if fishery not in self.agent.data.keys():
                    self.agent.data[fishery] = {}

                self.agent.data[fishery][type] = jsonpickle.decode(body['data'])

    class ReceiveWeatherBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = msg.metadata['type']
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if fishery not in self.agent.data.keys():
                    self.agent.data[fishery] = {}

                self.agent.data[fishery][type] = jsonpickle.decode(body['data'])

    class ReceiveCrowdBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = msg.metadata['type']
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if fishery not in self.agent.data.keys():
                    self.agent.data[fishery] = {}

                self.agent.data[fishery][type] = int(body['data'])

    class ReceiveFishContentBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                body = json.loads(msg.body)
                data = body['data']
                type = msg.metadata['type']
                fishery = body['fishery']
                self.agent.logger.info(f"received data: {data} from {sender} for fishery: {fishery}.")
                if fishery not in self.agent.data.keys():
                    self.agent.data[fishery] = {}

                self.agent.data[fishery][type] = json.loads(body['data'])

    class HandleDataRequestBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is not None:
                sender = str(msg.sender)
                self.agent.logger.info(f"received data request from {sender}.")

                opened_fisheries_data = self.agent.data
                for closed_fishery in self.agent.closed_fisheries:
                    opened_fisheries_data.pop(closed_fishery)

                data = jsonpickle.encode(opened_fisheries_data)

                msg = Message(to=sender)
                msg.metadata = {
                    MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                    MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
                    MessageMetadata.TYPE.value: DataType.RECOMMENDATION_RESPONSE.value,
                    MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
                }
                msg.body = json.dumps({
                    "data": data
                })
                msg.metadata = {
                    MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                    MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
                    MessageMetadata.TYPE.value: DataType.DATA_RESPONSE.value,
                    MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
                }
                await self.send(msg)

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.receive_water_quality_behaviour = self.ReceiveWaterQualityBehaviour()
        self.receive_weather_behaviour = self.ReceiveWeatherBehaviour()
        self.receive_crowd_behaviour = self.ReceiveCrowdBehaviour()
        self.receive_fish_content_behaviour = self.ReceiveFishContentBehaviour()
        self.handle_data_request_behaviour = self.HandleDataRequestBehaviour()
        self.data = {}
        self.closed_fisheries = set()

    async def setup(self):
        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
            MessageMetadata.TYPE.value: DataType.WATER_QUALITY.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        self.add_behaviour(self.receive_water_quality_behaviour, template=template)

        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
            MessageMetadata.TYPE.value: DataType.WEATHER.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        self.add_behaviour(self.receive_weather_behaviour, template=template)

        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
            MessageMetadata.TYPE.value: DataType.CROWD.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        self.add_behaviour(self.receive_crowd_behaviour, template=template)

        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
            MessageMetadata.TYPE.value: DataType.FISH_CONTENT.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        self.add_behaviour(self.receive_fish_content_behaviour, template=template)

        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.REQUEST.value,
            MessageMetadata.TYPE.value: DataType.DATA_REQUEST.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        self.add_behaviour(self.handle_data_request_behaviour, template=template)
        await super().setup()
