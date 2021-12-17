import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import keyboard

from src.agents.client_reporter import *
from src.agents.crowd_monitoring import CrowdMonitoring
from src.agents.data_accumulator import DataAccumulator
from src.agents.fish_content_monitoring import FishContentMonitoring
from src.agents.fishery_recommender import FisheryRecommender
from src.agents.water_monitoring import WaterMonitoring
from src.agents.weather_monitoring import WeatherMonitoring
from src.mas_logging import create_logger


class SenderAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="receiver@localhost")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)

class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=20) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)



if __name__ == "__main__":
    agents = []
    logger = create_logger('main')
    logger.info('How to use: \n f - generate fishery reccomendation\n r - generate report\n q - quit\n')
    logger.info('initializing agents')
    agents.append(WaterMonitoring('water_monitoring@localhost', '1qaz@WSX'))
    agents.append(FishContentMonitoring('fish_content_monitoring@localhost', '1qaz@WSX'))
    agents.append(WeatherMonitoring('weather_monitoring@localhost', '1qaz@WSX'))
    agents.append(CrowdMonitoring('crowd_monitoring@localhost', '1qaz@WSX'))
    agents.append(DataAccumulator('data_accumulator@localhost', '1qaz@WSX'))
    agents.append(FisheryRecommender('fishery_recommender@localhost', '1qaz@WSX'))
    agents.append(ClientReporter('client_reporter@localhost', '1qaz@WSX'))
    for agent in agents:
        future = agent.start()

    while True:
        if keyboard.is_pressed('q'):
            logger.info('q key has been pressed, stopping program')
            for agent in agents:
                future = agent.stop()
            break
        elif keyboard.is_pressed('f'):
            logger.info('f key has been pressed, generating recommendation')
            time.sleep(1)
            # send message to fishery recommender and print recommendation
            pass
        elif keyboard.is_pressed('r'):
            logger.info('r key has been pressed, generating report')
            time.sleep(1)
            # send message to client reporter and print report
            pass
        else:
            pass


