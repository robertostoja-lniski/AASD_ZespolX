import os

import logging


def add_stream_logger(logger, log_format: str):
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter(log_format)
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)


def add_file_logger(logger, log_format: str, name: str):
    f_handler = logging.FileHandler(name)
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter(log_format)
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)


def create_logger(name: str, verbose: bool):
    if not os.path.exists("../logs/"):
        os.makedirs("../logs/")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    if verbose:
        add_stream_logger(logger, log_format)

    add_file_logger(logger, log_format, '../logs/' + name + '.log')
    add_file_logger(logger, log_format, '../logs/all.log')

    return logger
