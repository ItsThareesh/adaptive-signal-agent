from utils.logger import logger
from .car import Car
from .traffic_light import TrafficLight
from .lane_queue import LaneQueue


class CarsController:
    def __init__(self, cars: list[Car], traffic_lights: list[TrafficLight], **kwargs):
        self.cars = cars
        self.traffic_lights = traffic_lights
        self.lane_queues = {}
        self.verbose = kwargs.get("verbose", False)

        if self.verbose:
            logger.info("[CarsController] Verbose mode ON")

        self._initialize_lane_queue()

    def _initialize_lane_queue(self):
        for dir in ["N", "S", "W", "E"]:
            self.lane_queues[dir] = LaneQueue()

    def update_cars_positions(self, screen, render_game: bool = False) -> int:
        self._remove_out_of_bounds()
        cars_waiting = {'N': 0, 'S': 0, 'W': 0, 'E': 0}
        cars_passed = 0

        for car in self.cars:
            should_stop = False

            for tl in self.traffic_lights:
                # If Car's and Traffic Light Direction isn't the same, then go to next iteration
                if tl.direction != car.direction:
                    continue

                if tl.state in ["RED", "YELLOW"] and car.is_before_tl(tl):
                    cars_waiting[tl.direction] += 1

                    if car.is_near_tl(tl):
                        should_stop = True
                        break

                # Should stop if a car is too close to the car in front of it in the respective lane
                front_car = self.lane_queues[car.direction].get_front_car(car)
                if front_car and self._too_close_to_other(car, front_car):
                    should_stop = True
                    break

            if not should_stop:
                car.move()

            if car.has_crossed_middle():
                cars_passed += 1

            if render_game:
                car.draw(screen)

        return (cars_waiting, cars_passed)

    @staticmethod
    def _too_close_to_other(car: Car, front_car: Car, min_gap=35):
        if car.direction in ["N", "S"]:
            return abs(car.y - front_car.y) < min_gap

        return abs(car.x - front_car.x) < min_gap

    def _remove_out_of_bounds(self):
        for car in self.cars[:]:  # Iterate over a copy to avoid skipping elements
            if car.is_out_of_bounds():
                if self.verbose:
                    logger.info("Removed Car %s", car.ID)

                # Since I'm running this method on every frame, it's safe to
                # think that the first car in any lane left the window frame
                lane_queue = self.lane_queues[car.direction]
                lane_queue.dequeue(car.lane)

                self.cars.remove(car)
