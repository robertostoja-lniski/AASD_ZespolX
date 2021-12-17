from spade.agent import Agent

from src.mas_logging import create_logger


class BaseAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = create_logger(self.__class__.__name__)
        self.logger.info('initialization')
