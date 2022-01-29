import datetime
import json
import os
from collections import deque

import jsonpickle
from spade.message import Message
from spade.template import Template

from src.agents.base_agent import BaseAgent
from src.io_utils import write_json
from src.spec import DataType, Perfomatives, ONTOLOGY, MessageMetadata, MSG_LANGUAGE
from src.mas_logging import create_logger

class ClientReporter(BaseAgent):
    class HandleReportGenerationBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        @staticmethod
        def _generate_data_request():
            out_msg = Message()
            out_msg.metadata = {
                MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                MessageMetadata.PERFORMATIVE.value: Perfomatives.REQUEST.value,
                MessageMetadata.TYPE.value: DataType.DATA_REQUEST.value,
                MessageMetadata.LANGUAGE.value: MSG_LANGUAGE,
            }
            return out_msg

        async def run(self):
            await super().run()
            in_msg = await self.receive(timeout=10)
            if in_msg is None:
                return

            self.agent.logger.info(
                "Received report generation request from " + str(in_msg.sender)
            )
            self.agent.requests_to_handle.append(in_msg.sender)

            if not self.agent.data_request_sent:
                out_msg = self._generate_data_request()

                await self.send_to_all_contacts(
                    out_msg,
                    lambda contact: self.agent.logger.info(
                        "sent data request to " + str(contact)
                    ),
                )
                self.agent.data_request_sent = True

    class HandleDataResponseBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        def _generate_client_report(self, fisheries):
            return [self._generate_single_fishery_report(name, data) for name, data in fisheries.items()]

        def _generate_single_fishery_report(self, name, data):
            return {
                'name': name,
                'weather': {
                    'cloudiness': data['Weather'].cloudiness,
                    'precipitation_rate': data['Weather'].precipitation_rate,
                    'pressure': data['Weather'].pressure,
                    'temperature': data['Weather'].temperature,
                    'wind_speed': data['Weather'].wind_speed,
                },
                'water_quality': {
                    'contamination_level': data['Water quality'].contamination_level,
                    'oxygen_level': data['Water quality'].oxygen_level,
                    'temperature': data['Water quality'].temperature,
                },
                'fish': {
                    'fish_content': data['Fish content']['fish_content'],
                    'fish_content_rating': data['Fish content']['fish_content_rating'],
                },
                'crowd': data["Crowd"]
            }

        @staticmethod
        def _get_str_time():
            return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        async def run(self):
            await super().run()
            msg = await self.receive(timeout=10)
            if msg is None:
                self.agent.data_request_sent = False
                return

            fisheries_data = jsonpickle.decode(json.loads(msg.body)['data'])

            try:
                data = self._generate_client_report(fisheries_data)
            except KeyError:
                # if not enough data is provided, report will not be generate
                return

            for requester in self.agent.requests_to_handle:
                dir_path = os.path.join('reports', str(requester))
                path = os.path.join(dir_path, f'client_report_{self._get_str_time()}.txt')
                write_json(data, path)

            self.agent.requests_to_handle.clear()
            self.agent.data_request_sent = False

    async def setup(self):
        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.REQUEST.value,
            MessageMetadata.TYPE.value: DataType.REPORT_GENERATION_REQUEST.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE,
        }
        self.add_behaviour(self.report_generation_behaviour, template=template)
        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
            MessageMetadata.TYPE.value: DataType.DATA_RESPONSE.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        self.add_behaviour(self.data_response_behaviour, template=template)
        await super().setup()

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.report_generation_behaviour = self.HandleReportGenerationBehaviour()
        self.data_response_behaviour = self.HandleDataResponseBehaviour()
        self.requests_to_handle = deque()
        self.data_request_sent = False
