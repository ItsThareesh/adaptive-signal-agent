from .car import Car


class LaneQueue:
    def __init__(self):
        self.queue: list[Car] = []  # list of car references in order

    def enqueue(self, car: Car):
        self.queue.append(car)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

    def peek(self):
        return self.queue[0] if self.queue else None

    def get_front_car(self, car: Car):
        idx = self.queue.index(car)

        if idx > 0:
            return self.queue[idx - 1]

        return None
