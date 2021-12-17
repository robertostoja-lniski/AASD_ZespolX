import os

import logging

def create_logger(name):
    if not os.path.exists("../logs/"):
        os.makedirs("../logs/")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('../logs/' + name + '.log')
    all_handler = logging.FileHandler('../logs/all.log')
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)
    all_handler.setLevel(logging.DEBUG)
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # Create formatters and add it to handlers
    c_format = logging.Formatter(log_format)
    f_format = logging.Formatter(log_format)
    all_format = logging.Formatter(log_format)
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    all_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger.addHandler(all_handler)
    return logger
