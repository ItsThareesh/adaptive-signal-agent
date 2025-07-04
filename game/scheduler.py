import time
from typing import List
from .game_constants import YELLOW_DURATION, GREEN_DURATION
from ui.ui_constants import CENTER, LANE_WIDTH
from .car import Car
from .traffic_light import TrafficLight


class TrafficLightScheduler:
    def __init__(self, traffic_lights: list[TrafficLight]):
        self.traffic_lights = traffic_lights

        # Light Cooldowns
        self._yellow_duration = YELLOW_DURATION
        self._green_duration = GREEN_DURATION

        # Internal State
        self.current_action = None
        self.pending_action = None
        self.scheduler_state = 'WAITING_FOR_NEXT_ACTION'
        self.last_switch_time = time.time()

    def _is_intersection_clear(self, cars: List[Car]):
        center = CENTER
        lane_width = LANE_WIDTH // 2
        margin = 10

        for car in cars:
            if center - lane_width - margin < car.x < center + lane_width + margin and \
                    center - lane_width - margin < car.y < center + lane_width + margin:
                return False

        return True

    def _apply_agent_action(self, action: int):
        green_dirs = ['N', 'S'] if action == 0 else ['E', 'W']

        for tl in self.traffic_lights:
            tl.state = 'GREEN' if tl.direction in green_dirs else 'RED'

        self.current_action = action
        self.scheduler_state = 'GREEN'
        self.last_switch_time = time.time()

    def update(self, cars: List[Car]):
        now = time.time()
        elapsed = now - self.last_switch_time

        if self.scheduler_state == 'GREEN':
            if elapsed >= self._green_duration:
                if self.pending_action is not None and self.pending_action != self.current_action:
                    self._set_yellow()

            elif self.pending_action == self.current_action:
                self.pending_action = None

        elif self.scheduler_state == 'YELLOW':
            if self._is_intersection_clear(cars):
                if elapsed >= self._yellow_duration:
                    self._set_red()

        elif self.scheduler_state == 'WAITING_FOR_NEXT_ACTION':
            if self.pending_action is not None:
                self._apply_agent_action(self.pending_action)
                self.pending_action = None

    def _set_yellow(self):
        for tl in self.traffic_lights:
            if tl.state == 'GREEN':
                tl.state = 'YELLOW'

        self.scheduler_state = 'YELLOW'
        self.last_switch_time = time.time()

    def _set_red(self):
        for tl in self.traffic_lights:
            tl.state = 'RED'

        self.scheduler_state = 'WAITING_FOR_NEXT_ACTION'
