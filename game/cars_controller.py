from ui import ui_constants
from .car import Car
from .traffic_light import TrafficLight
from .lane_queue import LaneQueue
from utils.logger import logger


class CarsController:
    def __init__(self, cars: list[Car], traffic_lights: list[TrafficLight]):
        self.cars = cars
        self.traffic_lights = traffic_lights
        self.lane_queues = {}

        self._initialize_lane_queue()

    def _initialize_lane_queue(self):
        for dirctn in ['N', 'S', 'W', 'E']:
            self.lane_queues[dirctn] = LaneQueue()

    def update_cars_positions(self, screen, train=False) -> int:
        self._remove_out_of_bounds()
        cars_passed = 0

        for car in self.cars:
            should_stop = False

            for tl in self.traffic_lights:
                if tl.direction != car.direction:
                    continue

                # print(f"Car {car.ID} before TL: {car.is_before_tl(tl)}")
                # print(f"Car {car.ID} will cross stop line: {car.will_cross_stop_line(tl)}")
                # print(f"Car {car.ID} is near TL: {car.is_near_tl(tl)}")

                if car.is_before_tl(tl):
                    if car.will_cross_stop_line(tl) and car.is_near_tl(tl):
                        should_stop = True
                        break
                    else:
                        front_car = self.lane_queues[car.direction].get_front_car(car)

                        # Should stop if a car is too close to the car in front of it in the respective lane
                        if front_car and self._too_close_to_other(car, front_car):
                            should_stop = True
                            break

            if not should_stop:
                car.move()

            if car.has_crossed_intersection():
                cars_passed += 1

            if not train:
                car.draw(screen)

        return cars_passed

    def is_intersection_clear(self):
        center = ui_constants.CENTER
        margin = 75

        for car in self.cars:
            if center - margin < car.x < center + margin and center - margin < car.y < center + margin:
                return False

        return True

    @staticmethod
    def _too_close_to_other(car: Car, front_car: Car, min_gap=35):
        if car.direction in ['N', 'S']:
            return abs(car.y - front_car.y) < min_gap
        else:
            return abs(car.x - front_car.x) < min_gap

    def _remove_out_of_bounds(self):
        for car in self.cars[:]:  # Iterate over a copy to avoid skipping elements
            if car.is_out_of_bounds():
                logger.info(f"Removed Car {car.ID}")
                lane_queue = self.lane_queues[car.direction]

                # Since I'm running this method on every frame, it's safe to
                # think that the first car in any lane left the window frame
                if lane_queue.peek(car.lane) == car:
                    lane_queue.dequeue(car.lane)

                self.cars.remove(car)
