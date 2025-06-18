import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("traffic_sim")

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def get_logger(self):
        return self.logger


logger = Logger().get_logger()
