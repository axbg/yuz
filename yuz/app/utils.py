import logging

from pathlib import Path
from datetime import datetime

class Logger:
    logging.basicConfig(filename = 'yuz.log', level=logging.INFO)
    logger = logging.getLogger("yuz-logger")

    @staticmethod
    def info(message):
        Logger.logger.info("{} - {}".format(datetime.now(), message))

    @staticmethod
    def warn(message):
        Logger.logger.warn("{} - {}".format(datetime.now(), message))

    @staticmethod
    def error(message):
        Logger.logger.error("{} - {}".format(datetime.now(), message))