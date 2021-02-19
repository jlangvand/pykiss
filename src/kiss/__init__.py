"""
Main init file
"""

import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
CONSOLE_FORMAT = '%(levelname)8s %(filename)14s:%(lineno)-4s %(message)s'
stream_handler = logging.StreamHandler(sys.stdout)
stream_formatter = logging.Formatter(CONSOLE_FORMAT)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)
