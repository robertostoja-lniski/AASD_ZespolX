import argparse

import coolname
from spade import quit_spade

import src.spec as spec
from src.agents.client_reporter import *
from src.agents.crowd_monitoring import CrowdMonitoring
from src.agents.data_accumulator import DataAccumulator
from src.agents.fish_content_monitoring import FishContentMonitoring
from src.agents.fishery_recommender import FisheryRecommender
from src.agents.user import User
from src.agents.water_monitoring import WaterMonitoring
from src.agents.weather_monitoring import WeatherMonitoring
from src.fishery.Fishery import Fishery
from src.mas_logging import create_logger


def main(n_fisheries: int):
    agents = []
    logger = create_logger('main')
    logger.info(
        'How to use: \n press f - generate fishery recommendation\n press r - generate report\n input q - quit\n')
    logger.info('initializing agents')

    data_accumulator_agent = DataAccumulator(spec.data_accumulator['username'], spec.password, spec.host)
    fishery_recommender_agent = FisheryRecommender(spec.fishery_recommender['username'], spec.password, spec.host)
    client_reporter_agent = ClientReporter(spec.client_reporter['username'], spec.password, spec.host)
    user_agent = User(spec.user['username'], spec.password, spec.host)

    fishery_recommender_agent.subscribe_to([user_agent, data_accumulator_agent])
    client_reporter_agent.subscribe_to([user_agent, data_accumulator_agent])

    for fishery_index in range(n_fisheries):
        name = ' '.join(coolname.generate(2))
        fishery = Fishery(name)

        water_monitoring_agent = WaterMonitoring(f"{spec.water_monitoring['username']}_{str(fishery_index)}",
                                                 spec.password, spec.host)
        fish_content_monitoring_agent = FishContentMonitoring(
            f"{spec.fish_content_monitoring['username']}_{str(fishery_index)}", spec.password, spec.host)
        weather_monitoring_agent = WeatherMonitoring(f"{spec.weather_monitoring['username']}_{str(fishery_index)}",
                                                     spec.password, spec.host)
        crowd_monitoring_agent = CrowdMonitoring(f"{spec.crowd_monitoring['username']}_{str(fishery_index)}",
                                                 spec.password, spec.host)

        water_monitoring_agent.subscribe_to([weather_monitoring_agent])
        fish_content_monitoring_agent.subscribe_to([water_monitoring_agent])

        water_monitoring_agent.set_fishery(fishery)
        fish_content_monitoring_agent.set_fishery(fishery)
        weather_monitoring_agent.set_fishery(fishery)
        crowd_monitoring_agent.set_fishery(fishery)
        agents.extend(
            [water_monitoring_agent, fish_content_monitoring_agent, weather_monitoring_agent, crowd_monitoring_agent])
        data_accumulator_agent.subscribe_to(
            [water_monitoring_agent, fish_content_monitoring_agent, weather_monitoring_agent, crowd_monitoring_agent])

    agents.extend([data_accumulator_agent, fishery_recommender_agent, client_reporter_agent, user_agent])

    port = 10001
    for agent in agents:
        future = agent.start()
        future.result()

    for agent in agents:
        agent.web.start(hostname="127.0.0.1", port=port)
        port += 1

    while True:
        key = input()
        if key == 'q':
            logger.info('q key has been recognized, stopping program')
            quit_spade()
            break

    for agent in agents:
        agent.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--n_fisheries', help='Number of fisheries', type=int, default=2)

    args = parser.parse_args()
    main(args.n_fisheries)
