import time
import random
from . import game_constants
from utils.logger import logger


class TrafficLight:
    def __init__(self, direction):
        self.state = random.choice(['GREEN', 'RED', 'TURN_LEFT', 'TURN_RIGHT'])
        self.direction = direction
        self.red_duration = game_constants.RED_DURATION
        self.green_duration = game_constants.GREEN_DURATION
        self.last_switch_time = time.time()

        logger.info(f'Traffic Light at {self.direction} is initialized to {self.state}')

    def update(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_switch_time

        if self.state == 'RED' and elapsed_time > self.red_duration:
            self.state = 'GREEN'
            logger.info(f"Changed {self.direction} Signal from RED to GREEN")  # Log Information
            self.last_switch_time = time.time()

        elif self.state == 'GREEN' and elapsed_time > self.green_duration:
            self.state = 'RED'
            logger.info(f"Changed Signal at {self.direction} from GREEN to RED")  # Log Information
            self.last_switch_time = time.time()
