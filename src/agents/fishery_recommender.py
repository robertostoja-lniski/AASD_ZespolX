import datetime
import json
import os
from typing import Optional, Tuple

import jsonpickle
from aioxmpp import JID
from spade.message import Message
from spade.template import Template
from src.agents.fish_content_monitoring import FishContentMonitoring
from src.agents.base_agent import BaseAgent
from src.generators.WaterQualityGenerator import MAX_WATER_TEMPERATURE
from src.generators.WeatherGenerator import MIN_TEMPERATURE, MAX_TEMPERATURE, MIN_PRESSURE, MAX_PRESSURE, \
    MAX_PRECIPITATION, MAX_WIND_SPEED, MAX_CLOUDINESS
from src.spec import DataType, Perfomatives, ONTOLOGY, MessageMetadata, MSG_LANGUAGE


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
                    msg.metadata = {
                        MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                        MessageMetadata.PERFORMATIVE.value: Perfomatives.REQUEST.value,
                        MessageMetadata.TYPE.value: DataType.DATA_REQUEST.value,
                        MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
                    }
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
                data = jsonpickle.decode(json.loads(msg.body)['data'])
                recommendation = self.agent.get_recommendation(data)
                for requester in self.agent.recommendation_requests_queue:
                    self.agent.save_recommendation_for_user(requester, recommendation, data)
                self.agent.recommendation_requests_queue = set([])
            self.agent.data_request_sent = False

    def __init__(self, username: str, password: str, host: str, verbose: bool):
        super().__init__(username, password, host, verbose)
        self.recommendation_request_behaviour = self.HandleRecommendationRequestBehaviour()
        self.data_response_behaviour = self.HandleDataResponseBehaviour()
        self.report_generation_behaviour = self.HandleReportGenerationBehaviour()
        self.recommendation_requests_queue = set([])
        self.data_request_sent = False

    # Ignore requests for report generattion
    class HandleReportGenerationBehaviour(BaseAgent.BaseAgentBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self):
            await super().run()
            return

    async def setup(self):
        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.REQUEST.value,
            MessageMetadata.TYPE.value: DataType.RECOMMENDATION_REQUEST.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        self.add_behaviour(self.recommendation_request_behaviour, template=template)
        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.INFORM.value,
            MessageMetadata.TYPE.value: DataType.DATA_RESPONSE.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
        }
        self.add_behaviour(self.data_response_behaviour, template=template)
        template = Template()
        template.metadata = {
            MessageMetadata.ONTOLOGY.value: ONTOLOGY,
            MessageMetadata.PERFORMATIVE.value: Perfomatives.REQUEST.value,
            MessageMetadata.TYPE.value: DataType.REPORT_GENERATION_REQUEST.value,
            MessageMetadata.LANGUAGE.value: MSG_LANGUAGE,
        }
        self.add_behaviour(self.report_generation_behaviour, template=template)
        await super().setup()

    def get_recommendation(self, data):
        self.logger.info("Creating recommendation...")
        print("Creating recommendation...")

        highest_crowd = 0
        for fishery in data.keys():
            if DataType.CROWD.value in data[fishery]:
                crowd = data[fishery][DataType.CROWD.value]
                highest_crowd = crowd if crowd > highest_crowd else highest_crowd

        fishery_scores = {}
        for fishery in data.keys():
            if data[fishery]:
                if DataType.FISH_CONTENT.value in data[fishery].keys():
                    fish_content_score = data[fishery][DataType.FISH_CONTENT.value]['fish_content_rating']
                else:
                    fish_content_score = 0
                if DataType.WATER_QUALITY.value in data[fishery].keys():
                    water_contamination_score = (100 - data[fishery][DataType.WATER_QUALITY.value].contamination_level) / 100
                    water_oxygen_level_score = (100 - data[fishery][DataType.WATER_QUALITY.value].oxygen_level) / 100
                    water_temperature = data[fishery][DataType.WATER_QUALITY.value].temperature
                    water_temperature_score = 0 if water_temperature < 4 else (water_temperature - 4) / (
                                15 - 4) if water_temperature < 15 \
                        else (MAX_WATER_TEMPERATURE - water_temperature) / (MAX_WATER_TEMPERATURE - 15)

                    water_quality_score = (water_temperature_score + water_contamination_score + water_oxygen_level_score) / 3
                else:
                    water_quality_score = 0

                if DataType.WEATHER.value in data[fishery].keys():
                    weather_data = data[fishery][DataType.WEATHER.value]
                    temperature_score = (weather_data.temperature - MIN_TEMPERATURE) / (
                                20 - MIN_TEMPERATURE) if weather_data.temperature <= 20 \
                        else (MAX_TEMPERATURE - weather_data.temperature) / (MAX_TEMPERATURE - 20)
                    pressure_score = (weather_data.pressure - MIN_PRESSURE) / (
                                1000. - MIN_PRESSURE) if weather_data.pressure <= 1000. \
                        else (MAX_PRESSURE - weather_data.pressure) / (MAX_PRESSURE - 1000.)
                    precipitation_score = (MAX_PRECIPITATION - weather_data.precipitation_rate) / MAX_PRECIPITATION
                    wind_speed_score = (MAX_WIND_SPEED - weather_data.wind_speed) / MAX_WIND_SPEED
                    cloudiness_score = (MAX_CLOUDINESS - weather_data.cloudiness) / MAX_CLOUDINESS

                    weather_score = 0.3 * temperature_score + 0.3 * precipitation_score + 0.2 * wind_speed_score + 0.1 * pressure_score + 0.1 * cloudiness_score
                else:
                    weather_score = 0

                if DataType.CROWD.value in data[fishery].keys():
                    crowd_score = 0 if highest_crowd == 0 else data[fishery][DataType.CROWD.value] / highest_crowd
                else:
                    crowd_score = 0

                overall_score = weather_score + water_quality_score + fish_content_score + crowd_score
                fishery_scores[fishery] = overall_score
            else:
                self.logger.info(f"No data for fishery {fishery.name}.")

        best_fishery = None
        for fishery in fishery_scores.keys():
            if best_fishery is None or fishery_scores[fishery] > fishery_scores[best_fishery]:
                best_fishery = fishery

        return (best_fishery, fishery_scores[best_fishery]) if best_fishery else None

    def save_recommendation_for_user(self, user: JID, recommendation: Optional[Tuple[str, dict]], data):
        if recommendation:
            self.logger.info("Saving recommendation for user " + str(user))
            print("Saving recommendation for user " + str(user))
            fishery = recommendation[0]
            score = recommendation[1]
            fishery_data = data[fishery]
            txt = f"""Best fishery: {fishery}
Overall score: {"{:.1f}".format(score)} out of max 4
Crowd at the fishery: {f"{fishery_data[DataType.CROWD.value]} persons" if DataType.CROWD.value in fishery_data.keys() else 'No data'}
Fish content: {fishery_data[DataType.FISH_CONTENT.value]['fish_content'] if DataType.FISH_CONTENT.value in fishery_data.keys() else 'No data'}
Fish content rating: {FishContentMonitoring.FishContentRating(fishery_data[DataType.FISH_CONTENT.value]['fish_content_rating']).name  if DataType.FISH_CONTENT.value in fishery_data.keys() else 'No data'}
Water contamination level: {f"{'{:.1f}'.format(fishery_data[DataType.WATER_QUALITY.value].contamination_level * 100)}%" if DataType.WATER_QUALITY.value in fishery_data.keys() else 'No data'}
Water oxygen level: {f"{'{:.1f}'.format(fishery_data[DataType.WATER_QUALITY.value].oxygen_level * 100)}%" if DataType.WATER_QUALITY.value in fishery_data.keys() else 'No data'}
Water temperature: {f"{'{:.1f}'.format(fishery_data[DataType.WATER_QUALITY.value].temperature)}°C" if DataType.WATER_QUALITY.value in fishery_data.keys() else 'No data'}
Air temperature: {f"{'{:.1f}'.format(fishery_data[DataType.WEATHER.value].temperature)}°C" if DataType.WEATHER.value in fishery_data.keys() else 'No data'}
Precipitation: {f"{'{:.1f}'.format(fishery_data[DataType.WEATHER.value].precipitation_rate)}mm/h" if DataType.WEATHER.value in fishery_data.keys() else 'No data'}
Air pressure: {f"{'{:.1f}'.format(fishery_data[DataType.WEATHER.value].pressure)}hPa" if DataType.WEATHER.value in fishery_data.keys() else 'No data'}
Wind speed: {f"{'{:.1f}'.format(fishery_data[DataType.WEATHER.value].wind_speed)}km/h" if DataType.WEATHER.value in fishery_data.keys() else 'No data'}
Clouds: {f"{int(fishery_data[DataType.WEATHER.value].cloudiness)}%" if DataType.WEATHER.value in fishery_data.keys() else 'No data'}"""
        else:
            txt = "No available fisheries at the moment. " \
                  "Unfortunately all of them are closed due to bad water quality."
        reports_dir = os.path.join('recommendations', str(user))
        os.makedirs(reports_dir, exist_ok=True)
        recommendation_path = os.path.join(reports_dir,
                                   f"recommendation_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt")
        report_file = recommendation_path
        f = open(report_file, 'x', encoding='utf8')
        f.write(txt)
        f.close()
        print(f'Saved recommendation at path {recommendation_path}')
        pass
