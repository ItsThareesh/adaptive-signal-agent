import random
from .car import Car
from . import game_constants as game_constants
from utils.logger import logger


class CarsSpawner:
    def __init__(self, max_cars:int = 10, enable_log:bool = False):
        self.cars: list[Car] = []
        self.max_cars = max_cars
        self.cooldown_timer = 0
        self.enable_logs = enable_log

    def get_total_cars(self):
        """ Helper method for drawing the total cars count on the screen """
        return len(self.cars)

    def maybe_spawn_car(self, lane_queues: dict):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            return

        if random.random() < game_constants.SPAWN_PROBABILITY and len(self.cars) < self.max_cars:
            self.spawn_car(lane_queues)
            self.cooldown_timer = game_constants.COOLDOWN_TIMER

    def spawn_car(self, lane_queues: dict):
        direction = random.choice(['N', 'S', 'W', 'E'])

        # Create the Car instance
        new_car = Car(direction)
        new_car.ID = self.get_total_cars() + 1

        if self.enable_logs:
            logger.info(f"Spawning Car {new_car.ID} heading {direction}")  # Log the information

        lane_queues[new_car.direction].enqueue(new_car)
        self.cars.append(new_car)
