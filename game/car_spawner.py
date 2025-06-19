import random
from .car import Car
from .traffic_light import TrafficLight
from . import game_constants as game_constants, car
from utils.logger import logger


class CarSpawner:
    def __init__(self, max_cars=10):
        self.cars: list[Car] = []
        self.total_cars = 0
        self.max_cars = max_cars
        self.cooldown_timer = 0

    def maybe_spawn_car(self, lane_queues: dict):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            return

        if random.random() < game_constants.SPAWN_PROBABILITY and len(self.cars) < self.max_cars:
            self.spawn_car(lane_queues)
            self.cooldown_timer = game_constants.COOLDOWN_TIMER

    def spawn_car(self, lane_queues: dict):
        direction = random.choice(['N'])

        # Create the Car instance
        new_car = Car(direction)
        self.total_cars += 1
        new_car.ID = self.total_cars

        logger.info(f"Spawning Car {new_car.ID} heading {direction}")  # Log the information

        lane_queues[new_car.direction].enqueue(new_car)
        self.cars.append(new_car)

    # def is_car_ahead(self, car: Car, lane_threshold: int = 10, distance_threshold: int = 40):
    #     for other in self.cars:
    #         if car == other:
    #             continue
    #         if car.direction != other.direction:
    #             continue

    #         if car.direction in ['N', 'S']:
    #             same_lane = abs(car.x - other.x) < lane_threshold
    #         else:
    #             same_lane = abs(car.y - other.y) < lane_threshold

    #         if not same_lane:
    #             continue

    #         if car.direction == 'N':
    #             if other.y < car.y and abs(car.y - other.y) < distance_threshold:
    #                 return True
    #         elif car.direction == 'S':
    #             if other.y > car.y and abs(car.y - other.y) < distance_threshold:
    #                 return True
    #         elif car.direction == 'W':
    #             if other.x < car.x and abs(car.x - other.x) < distance_threshold:
    #                 return True
    #         elif car.direction == 'E':
    #             if other.x > car.x and abs(car.x - other.x) < distance_threshold:
    #                 return True

    #     return False
