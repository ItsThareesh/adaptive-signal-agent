import time
import random
from . import game_constants
from utils.logger import logger


class TrafficLight:
    def __init__(self, direction):
        self.state = random.choice(['GREEN', 'RED'])
        self.direction = direction
        self.__red_duration = game_constants.RED_DURATION
        self.__green_duration = game_constants.GREEN_DURATION
        self.__yellow_duration = game_constants.YELLOW_DURATION
        self.last_switch_time = time.time()

        logger.info(f'Traffic Light at {self.direction} is initialized to {self.state}')

    def update(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_switch_time

        if self.state == 'RED' and elapsed_time > self.__red_duration:
            self.state = 'GREEN'
            self.last_switch_time = current_time
            logger.info(f"Changed {self.direction} Signal from RED to GREEN")  # Log Information

        elif self.state == 'YELLOW' and elapsed_time > self.__yellow_duration:
            self.state = 'RED'
            self.last_switch_time = current_time

        elif self.state == 'GREEN' and elapsed_time > self.__green_duration:
            self.state = 'YELLOW'
            self.last_switch_time = current_time
