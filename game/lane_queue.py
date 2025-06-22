from .car import Car


class LaneQueue:
    def __init__(self):
        self.queue: list[list[Car]] = [[], []]  # list of car references in order

    def enqueue(self, car: Car):
        self.queue[car.lane].append(car)

    def dequeue(self, lane: int):
        return self.queue[lane].pop(0) if self.queue else None

    def peek(self, lane: int):
        return self.queue[lane][0] if self.queue else None

    def get_front_car(self, car: Car):
        idx = self.queue[car.lane].index(car)

        if idx > 0:
            return self.queue[car.lane][idx - 1]

        return None
