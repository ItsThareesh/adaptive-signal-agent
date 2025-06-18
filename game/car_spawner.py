import random
from game.car import Car
from . import game_constants as game_constants

cars = []


def maybe_spawn_car():
    if random.random() < game_constants.SPAWN_PROBABILITY:
        direction = random.choice(['N', 'S', 'E', 'W'])
        car = Car(direction)

        if len(cars) < 10:
            cars.append(car)


def update_cars(screen):
    for car in cars[:]:
        car.move()
        car.draw(screen)

        if car.is_out_of_bounds():
            cars.remove(car)
            print("Removed Car")
