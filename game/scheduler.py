from queue import Queue
import time
from typing import List
from ui.ui_constants import CENTER, LANE_WIDTH
from .game_constants import YELLOW_DURATION, GREEN_DURATION
from .car import Car
from .traffic_light import TrafficLight


class TrafficLightScheduler:
    def __init__(self, traffic_lights: list[TrafficLight], cars: List[Car]):
        self.traffic_lights = traffic_lights
        self.cars = cars

        # Light Cooldowns
        self._yellow_duration = YELLOW_DURATION
        self._green_duration = GREEN_DURATION

        # Internal State
        self.current_action = None
        self.pending_action = None
        self.scheduler_state = 'WAITING_FOR_NEXT_ACTION'
        self.last_switch_time = time.time()

    def _is_intersection_clear(self):
        center = CENTER
        lane_width = LANE_WIDTH // 2
        margin = 10

        for car in self.cars:
            if center - lane_width - margin < car.x < center + lane_width + margin and \
                    center - lane_width - margin < car.y < center + lane_width + margin:
                return False

        return True

    def _apply_agent_action(self, action: int, cur_time):
        """Applies the agent's action by setting the appropriate traffic lights to GREEN."""
        green_dirs = ['N', 'S'] if action == 0 else ['E', 'W']

        for tl in self.traffic_lights:
            tl.state = 'GREEN' if tl.direction in green_dirs else 'RED'

        self.current_action = action
        self.scheduler_state = 'GREEN'
        self.last_switch_time = cur_time

    def _set_yellow(self, cur_time):
        for tl in self.traffic_lights:
            if tl.state == 'GREEN':
                tl.state = 'YELLOW'

        self.scheduler_state = 'YELLOW'
        self.last_switch_time = cur_time

    def _set_red(self):
        for tl in self.traffic_lights:
            tl.state = 'RED'

        self.scheduler_state = 'WAITING_FOR_NEXT_ACTION'

    def _get_time(self):
        return time.time()

    def update(self):
        cur_time = self._get_time()
        elapsed = cur_time - self.last_switch_time

        if self.scheduler_state == 'GREEN':
            if elapsed >= self._green_duration:
                if self.pending_action is not None and self.pending_action != self.current_action:
                    self._set_yellow(cur_time)

                elif self.pending_action == self.current_action:
                    self.pending_action = None

        elif self.scheduler_state == 'YELLOW':
            if self._is_intersection_clear() and elapsed >= self._yellow_duration:
                self._set_red()

                if self.pending_action is not None:
                    self._apply_agent_action(self.pending_action, cur_time)
                    self.pending_action = None

        elif self.scheduler_state == 'WAITING_FOR_NEXT_ACTION':
            if self.pending_action is not None:
                self._apply_agent_action(self.pending_action, cur_time)
                self.pending_action = None
