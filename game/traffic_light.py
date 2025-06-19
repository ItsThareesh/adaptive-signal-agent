import time
from . import game_constants
from .car import Car
from ui import ui_constants
from utils.logger import logger


class TrafficLight:
    def __init__(self, direction):
        self.state = 'GREEN'
        self.direction = direction
        self.red_duration = game_constants.RED_DURATION
        self.green_duration = game_constants.GREEN_DURATION
        self.last_switch_time = time.time()

    def update(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_switch_time

        if self.state == 'RED' and elapsed_time > self.red_duration:
            self.state = 'GREEN'
            logger.info(f"Switched Signal at {self.direction} from RED to GREEN")  # Log Information
            self.last_switch_time = time.time()

        elif self.state == 'GREEN' and elapsed_time > self.green_duration:
            self.state = 'RED'
            logger.info(f"Switched Signal at {self.direction} from GREEN to RED")  # Log Information
            self.last_switch_time = time.time()

    def should_car_stop(self, car: Car) -> bool:
        if self.direction != car.direction:
            return False

        stop_margin = 50

        if self.state == 'RED':
            if self.direction == 'N':
                stop_line_y = ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 2

                if car.y <= stop_line_y - stop_margin:
                    return True

            elif self.direction == 'S':
                stop_line_y = ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 2

                if car.y >= stop_line_y + stop_margin:
                    return True

            elif self.direction == 'W':
                stop_line_x = ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 2

                if car.x <= stop_line_x + stop_margin:
                    return True

            elif self.direction == 'E':
                stop_line_x = ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 2

                if car.x >= stop_line_x - stop_margin:
                    return True

        else:
            return False
