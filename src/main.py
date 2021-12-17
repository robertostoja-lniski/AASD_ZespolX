import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from src.agents.client_reporter import *
from src.agents.crowd_monitoring import CrowdMonitoring
from src.agents.data_accumulator import DataAccumulator
from src.agents.fish_content_monitoring import FishContentMonitoring
from src.agents.fishery_recommender import FisheryRecommender
from src.agents.water_monitoring import WaterMonitoring
from src.agents.weather_monitoring import WeatherMonitoring


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

    water_monitoring = WaterMonitoring('water_monitoring', '1qaz@WSX')
    fish_content_monitoring = FishContentMonitoring('fish_content_monitoring', '1qaz@WSX')
    weather_monitoring = WeatherMonitoring('weather_monitoring', '1qaz@WSX')
    crowd_monitoring = CrowdMonitoring('crowd_monitoring', '1qaz@WSX')
    data_accumulator = DataAccumulator('data_accumulator', '1qaz@WSX')
    fishery_reccomender = FisheryRecommender('fishery_reccomender', '1qaz@WSX')
    client_reporter = ClientReporter('client_reporter', '1qaz@WSX')

