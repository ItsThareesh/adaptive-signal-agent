from .car import Car
from .traffic_light import TrafficLight
from .lane_queue import LaneQueue
from utils.logger import logger


class CarsController:
    def __init__(self, cars: list[Car], traffic_lights: list[TrafficLight]):
        self.cars = cars
        self.traffic_lights = traffic_lights
        self.lane_queues = {}

        self.initialize_lane_queue()
        self.assign_car_to_lane_queues()

    def initialize_lane_queue(self):
        for i in ['N', 'S', 'W', 'E']:
            self.lane_queues[i] = LaneQueue()

    def assign_car_to_lane_queues(self):
        for car in self.cars:
            self.lane_queues[car.direction].enqueue(car)

    def update_cars(self, screen):
        for car in self.cars:
            self._remove_out_of_bounds()
            car.move()
            car.draw(screen)

    def _remove_out_of_bounds(self):
        for car in self.cars:
            if car.is_out_of_bounds():
                logger.info(f"Removed Car {car.ID}")
                lane_queue = self.lane_queues[car.direction]

                if lane_queue.front(car.lane) == car:
                    lane_queue.dequeue(car.lane)

                self.cars.remove(car)
