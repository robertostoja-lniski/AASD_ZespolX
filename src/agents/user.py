import asyncio

from spade.message import Message

from src.agents.base_agent import BaseAgent
from src.spec import DataType, MessageMetadata, MSG_LANGUAGE, Perfomatives, ONTOLOGY
import threading


class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = asyncio.ensure_future(self.input_cbk(), loop=loop)
        loop.run_until_complete(asyncio.wait([task]))
        loop.close()


class User(BaseAgent):
    class GenerateRecommendationBehaviour(BaseAgent.BaseAgentBehaviour):
        kthread = None

        async def run(self):
            await super().run()
            if self.kthread is None:
                self.kthread = KeyboardThread(self.send_request)
            elif not self.kthread.is_alive():
                self.kthread._delete()
                self.kthread = KeyboardThread(self.send_request)

        async def send_request(self):
            key_input = self.agent.get_input()
            if key_input == 'f':
                self.agent.logger.info('f key has been pressed, generating recommendation')
                print('f key has been pressed, generating recommendation')
                msg = Message()
                msg.metadata = {
                    MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                    MessageMetadata.PERFORMATIVE.value: Perfomatives.REQUEST.value,
                    MessageMetadata.TYPE.value: DataType.RECOMMENDATION_REQUEST.value,
                    MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
                }
                await self.send_to_all_contacts(msg, lambda contact: self.agent.logger.info(
                    'sent recommendation request to ' + str(contact)))

    class GenerateReportBehaviour(BaseAgent.BaseAgentBehaviour):
        async def run(self):
            await super().run()
            msg = Message()
            msg.metadata = {
                MessageMetadata.ONTOLOGY.value: ONTOLOGY,
                MessageMetadata.PERFORMATIVE.value: Perfomatives.REQUEST.value,
                MessageMetadata.TYPE.value: DataType.REPORT_GENERATION_REQUEST.value,
                MessageMetadata.LANGUAGE.value: MSG_LANGUAGE
            }
            await self.send_to_all_contacts(msg, lambda contact: self.agent.logger.info(
                'sent report request to ' + str(contact)))

            await asyncio.sleep(2)
            # send message to client reporter and print report

    def __init__(self, username: str, password: str, host: str):
        super().__init__(username, password, host)
        self.generate_recommendation_behaviour = self.GenerateRecommendationBehaviour()
        self.generate_report_behaviour = self.GenerateReportBehaviour()

    async def setup(self):
        self.add_behaviour(self.generate_recommendation_behaviour)
        self.add_behaviour(self.generate_report_behaviour)

        await super().setup()

    def get_input(self):
        return input()



