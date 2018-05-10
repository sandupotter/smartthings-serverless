import logging
import sys


def create_logger(module_name: object, level: object = 'INFO', stdout: object = False) -> logging.Logger:
    logger = logging.getLogger(module_name)
    if level == 'INFO':
        logger.setLevel(logging.INFO)
    if level == 'DEBUG':
        logger.setLevel(logging.DEBUG)

    if stdout:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
