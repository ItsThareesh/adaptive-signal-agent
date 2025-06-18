import random
from game.car import Car
from . import game_constants as game_constants


class CarSpawner:
    def __init__(self, max_cars=10):
        self.cars = []
        self.max_cars = max_cars
        self.total_spawned_cars = 0
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
        car = Car(direction)
        self.cars.append(car)

    def update_cars(self, screen):
        for car in self.cars:
            car.move()
            car.draw(screen)

            if car.is_out_of_bounds():
                self.cars.remove(car)
                self.total_spawned_cars += 1
                print(f"Removed Car {self.total_spawned_cars}")
