import asyncio
from unittest import mock
from unittest.mock import patch

import aiounittest

from src import spec
from src.agents.crowd_monitoring import CrowdMonitoring
from src.agents.data_accumulator import DataAccumulator
from src.agents.fish_content_monitoring import FishContentMonitoring
from src.agents.fishery_recommender import FisheryRecommender
from src.agents.user import User
from src.agents.water_monitoring import WaterMonitoring
from src.agents.weather_monitoring import WeatherMonitoring
from src.fishery.Fishery import Fishery


class TestFisheryRecommenderMonitoring(aiounittest.AsyncTestCase):
    data_accumulator_agent = ...
    water_monitoring_agent = ...
    fish_content_monitoring_agent = ...
    weather_monitoring_agent = ...
    crowd_monitoring_agent = ...
    user_agent = ...
    fishery_recommender = ...

    @classmethod
    def setUpClass(cls):
        cls.fishery = Fishery('sample_fishery')
        cls.data_accumulator_agent = DataAccumulator(f"{spec.data_accumulator['username']}", spec.password, spec.host)

        cls.water_monitoring_agent = WaterMonitoring(f"{spec.water_monitoring['username']}_0",
                                                     spec.password, spec.host)
        cls.water_monitoring_agent.set_fishery(cls.fishery)

        cls.fish_content_monitoring_agent = FishContentMonitoring(f"{spec.fish_content_monitoring['username']}_0",
                                                                  spec.password, spec.host)
        cls.fish_content_monitoring_agent.set_fishery(cls.fishery)

        cls.weather_monitoring_agent = WeatherMonitoring(f"{spec.weather_monitoring['username']}_0",
                                                         spec.password, spec.host)
        cls.weather_monitoring_agent.set_fishery(cls.fishery)
        cls.water_monitoring_agent.subscribe_to([cls.weather_monitoring_agent])

        cls.crowd_monitoring_agent = CrowdMonitoring(f"{spec.crowd_monitoring['username']}_0", spec.password, spec.host)
        cls.crowd_monitoring_agent.set_fishery(cls.fishery)

        cls.fish_content_monitoring_agent.subscribe_to([cls.water_monitoring_agent])

        cls.user_agent = User(spec.user['username'], spec.password, spec.host)

        cls.fishery_recommender = FisheryRecommender(f"{spec.fishery_recommender['username']}", spec.password, spec.host)
        cls.fishery_recommender.subscribe_to([cls.user_agent, cls.data_accumulator_agent])

        cls.data_accumulator_agent.subscribe_to(
            [cls.water_monitoring_agent, cls.fish_content_monitoring_agent, cls.weather_monitoring_agent,
             cls.crowd_monitoring_agent, cls.fishery_recommender])

        for agent in [cls.water_monitoring_agent,
                      cls.fish_content_monitoring_agent,
                      cls.weather_monitoring_agent,
                      cls.crowd_monitoring_agent,
                      cls.data_accumulator_agent]:
            agent.start()

    @classmethod
    def tearDownClass(cls):
        cls.data_accumulator_agent.stop()
        cls.water_monitoring_agent.stop()
        cls.fish_content_monitoring_agent.stop()
        cls.weather_monitoring_agent.stop()
        cls.crowd_monitoring_agent.stop()
        cls.fishery_recommender.stop()
        cls.user_agent.stop()

    class CustomMock(object):
        calls = 0
        def get_input(self):
            self.calls += 1
            if self.calls == 1:
                return 'f'
            else:
                return input()

    # a lot of mocks and hacks here - testing async agents ain't easy :/
    @patch("src.agents.user.User.get_input")
    async def test_should_generate_recommendation_after_user_request(self, mocked_method):
        mocked_method.side_effect = self.CustomMock().get_input

        with mock.patch.object(TestFisheryRecommenderMonitoring.fishery_recommender, 'save_recommendation_for_user',
                               wraps=TestFisheryRecommenderMonitoring.fishery_recommender.save_recommendation_for_user) as mocked_save_recommendation:
            await asyncio.wrap_future(TestFisheryRecommenderMonitoring.fishery_recommender.start())
            await asyncio.wrap_future(TestFisheryRecommenderMonitoring.user_agent.start())

            b = [behavior for behavior in TestFisheryRecommenderMonitoring.fishery_recommender.behaviours
                 if type(behavior) == FisheryRecommender.HandleDataResponseBehaviour][0]

            async def mock_run(self):
                await self.run()
                # CyclicBehavior doesn't end, so we need to force it
                self.kill()

            b.run = mock_run

            [behavior for behavior in TestFisheryRecommenderMonitoring.fishery_recommender.behaviours
             if type(behavior) == FisheryRecommender.HandleDataResponseBehaviour][0].join()

            mocked_save_recommendation.assert_called()

        TestFisheryRecommenderMonitoring.fishery_recommender.stop()

