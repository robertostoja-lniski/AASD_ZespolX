from spade import quit_spade
import keyboard
from src.agents.client_reporter import *
from src.agents.crowd_monitoring import CrowdMonitoring
from src.agents.data_accumulator import DataAccumulator
from src.agents.fish_content_monitoring import FishContentMonitoring
from src.agents.fishery_recommender import FisheryRecommender
from src.agents.user import User
from src.agents.water_monitoring import WaterMonitoring
from src.agents.weather_monitoring import WeatherMonitoring
from src.mas_logging import create_logger

if __name__ == "__main__":
    agents = []
    logger = create_logger('main')
    logger.info('How to use: \n press f - generate fishery reccomendation\n press r - generate report\n input q - quit\n')
    logger.info('initializing agents')
    agents.append(WaterMonitoring(spec.water_monitoring, spec.password))
    agents.append(FishContentMonitoring(spec.fish_content_monitoring, spec.password))
    agents.append(WeatherMonitoring(spec.weather_monitoring, spec.password))
    agents.append(CrowdMonitoring(spec.crowd_monitoring, spec.password))
    agents.append(DataAccumulator(spec.data_accumulator, spec.password))
    agents.append(FisheryRecommender(spec.fishery_recommender, spec.password))
    agents.append(ClientReporter(spec.client_reporter, spec.password))
    agents.append(User(spec.user, spec.password))

    port = 10001
    for agent in agents:
        future = agent.start()
        agent.web.start(hostname="127.0.0.1", port=port)
        port += 1

    while True:
        key = input()
        if key == 'q':
            logger.info('q key has been recognized, stopping program')
            quit_spade()
        break
