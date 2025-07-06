import random
from utils.logger import logger
from .car import Car
from . import game_constants


class CarsSpawner:
    def __init__(self, max_cars: int = 10, enable_log: bool = False):
        self.cars: list[Car] = []
        self.max_cars = max_cars
        self.cooldown_timer = 0
        self.enable_logs = enable_log

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
        new_car.ID = len(self.cars) + 1

        if self.enable_logs:
            logger.info("Spawning Car %d heading %s", new_car.ID, direction)  # Log the information

        lane_queues[new_car.direction].enqueue(new_car)
        self.cars.append(new_car)
