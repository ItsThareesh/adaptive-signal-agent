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
        for i in ['N', 'S', 'W', 'E']:
            self.lane_queues[i] = LaneQueue()

    def update_cars(self, screen):
        self._remove_out_of_bounds()

        for car in self.cars:
            for tl in self.traffic_lights:
                if self._should_car_stop(tl, car):
                    if self.lane_queues[car.direction].peek(car.lane) == car and self._is_close_to_light(tl, car):
                        break
                    else:
                        if self._is_close_to_light(tl, car):
                            break
                        else:
                            front_car = self.lane_queues[car.direction].get_front_car(car)

                            if front_car and self._too_close_to_other(car, front_car):
                                break
                            else:
                                car.move()
                else:
                    car.move()

            car.draw(screen)

    @staticmethod
    def _too_close_to_other(car: Car, front_car: Car, min_gap=35):
        if car.direction in ['N', 'S']:
            return abs(car.y - front_car.y) < min_gap
        else:
            return abs(car.x - front_car.x) < min_gap

    @staticmethod
    def _is_close_to_light(tl: TrafficLight, car: Car):
        stop_margin = 25

        if tl.direction == 'N':
            stop_line_y = ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 2

            if stop_line_y - stop_margin <= car.y:
                return True

        elif tl.direction == 'S':
            stop_line_y = ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 2

            if stop_line_y + stop_margin <= car.y:
                return True

        elif tl.direction == 'W':
            stop_line_x = ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 2

            if stop_line_x + stop_margin <= car.x :
                return True

        elif tl.direction == 'E':
            stop_line_x = ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 2

            if stop_line_x - stop_margin <= car.x:
                return True

        return False

    @staticmethod
    def _should_car_stop(tl, car: Car) -> bool:
        if tl.direction != car.direction:
            return False

        stop_margin = 25

        if tl.state == 'RED':
            if tl.direction == 'N':
                stop_line_y = ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 2

                if car.y <= stop_line_y - stop_margin:
                    return True

            elif tl.direction == 'S':
                stop_line_y = ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 2

                if car.y >= stop_line_y + stop_margin:
                    return True

            elif tl.direction == 'W':
                stop_line_x = ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 2

                if car.x <= stop_line_x + stop_margin:
                    return True

            elif tl.direction == 'E':
                stop_line_x = ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 2

                if car.x >= stop_line_x - stop_margin:
                    return True

        return False

    def _remove_out_of_bounds(self):
        for car in self.cars:
            if car.is_out_of_bounds():
                logger.info(f"Removed Car {car.ID}")
                lane_queue = self.lane_queues[car.direction]

                if lane_queue.peek(car.lane) == car:
                    lane_queue.dequeue(car.lane)

                self.cars.remove(car)
