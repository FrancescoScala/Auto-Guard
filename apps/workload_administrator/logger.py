""" logger setup """

import sys
import logging
from config import NAME

def setup_logger() -> logging.Logger:
    """
    set up and return the logger
    """
    logger: logging.Logger = logging.getLogger(NAME)
    stdout: logging.StreamHandler = logging.StreamHandler(stream=sys.stdout)
    formatter: logging.Formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
    stdout.setFormatter(formatter)
    stdout.setLevel(logging.INFO)
    logger.addHandler(stdout)
    logger.setLevel(logging.INFO)
    return logger
