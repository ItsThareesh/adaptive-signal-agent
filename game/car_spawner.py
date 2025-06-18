import random
from .car import Car
from .traffic_light import TrafficLight
from . import game_constants as game_constants
from utils.logger import logger


class CarSpawner:
    def __init__(self, max_cars=10):
        self.cars = []
        self.total_cars = 0
        self.max_cars = max_cars
        self.cooldown_timer = 0

    def maybe_spawn_car(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            return

        if random.random() < game_constants.SPAWN_PROBABILITY and len(self.cars) < self.max_cars:
            self.spawn_car()
            self.cooldown_timer = game_constants.COOLDOWN_TIMER

    def spawn_car(self):
        direction = random.choice(['N', 'S', 'E', 'W'])

        # Create the Car instance
        car = Car(direction)
        self.total_cars += 1
        car.ID = self.total_cars

        logger.info(f"Spawning Car {car.ID} heading {direction}")  # Log the information

        self.cars.append(car)

    def update_cars(self, screen, traffic_lights: list[TrafficLight]):
        for car in self.cars:
            relevant_light = next((tl for tl in traffic_lights if tl.direction == car.direction), None)

            should_stop = relevant_light.should_car_stop(car) if relevant_light else False

            if should_stop:
                if car.stopped == False:
                    logger.info(f"Car {car.ID} stopped at Traffic Light")
                    car.stopped = True

            else:
                car.move()
                if car.stopped:
                    logger.info(f"Car {car.ID} resumed from {car.direction}")

                car.stopped = False

            car.draw(screen)

            if car.is_out_of_bounds():
                self.cars.remove(car)
                logger.info(f"Removed Car {car.ID}")  # Log the information
