from utils.logger import logger


class TrafficLight:
    def __init__(self, direction):
        self.state = 'RED'
        self.direction = direction

        logger.info(f"[{self.direction}] INITIALIZED TO {self.state}")
