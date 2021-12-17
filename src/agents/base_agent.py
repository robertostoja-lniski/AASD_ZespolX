import os

from spade.agent import Agent
import logging

class BaseAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.exists("../logs/"):
            os.makedirs("../logs/")

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('../logs/' + self.__class__.__name__ + '.log')
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # Create formatters and add it to handlers
        c_format = logging.Formatter(log_format)
        f_format = logging.Formatter(log_format)
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        self.logger.addHandler(c_handler)
        self.logger.addHandler(f_handler)
        self.logger.info('initialization')