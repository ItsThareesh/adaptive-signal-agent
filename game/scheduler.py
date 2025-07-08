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
        self.pending_actions = Queue()
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

        if self.scheduler_state == 'GREEN' and elapsed >= self._green_duration:
            # Check if the new pending action is differnet from current action
            if not self.pending_actions.empty():
                # If the next action is the same as current, continue with
                # green until another different action is queued
                next_action = self.pending_actions.queue[0]

                if next_action == self.current_action:
                    self.pending_actions.get()
                    self.last_switch_time = cur_time
                else:
                    self._set_yellow(cur_time)
            else:
                # No action? No need to switch. Just wait.
                pass  # Stay in GREEN until agent decides to do something

        elif self.scheduler_state == 'YELLOW' and elapsed >= self._yellow_duration:
            if self._is_intersection_clear():
                self._set_red()

                if not self.pending_actions.empty():
                    next_action = self.pending_actions.get()
                    self._apply_agent_action(next_action, cur_time)

        elif self.scheduler_state == 'WAITING_FOR_NEXT_ACTION':
            next_action = self.pending_actions.get()
            self._apply_agent_action(next_action, cur_time)
