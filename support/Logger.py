import logging


class Logger:
    def __init__(self):
        logger = logging.getLogger(__name__)

        logging.basicConfig()
        logger.setLevel(logging.DEBUG)

        self.logger = logger

    def info(self, message):
        self.logger.info(message)
