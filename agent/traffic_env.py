import sys
import pygame
from game.cars_controller import CarsController
from game.cars_spawner import CarsSpawner
from game.traffic_light import TrafficLight
from game.scheduler import TrafficLightScheduler
from ui import ui_constants
from ui.draw import DrawUIElements
from utils.logger import logger


class TrafficEnv:
    def __init__(self, max_cars: int = 15):
        pygame.init()
        self.screen = pygame.display.set_mode((ui_constants.WIDTH, ui_constants.HEIGHT))
        pygame.display.set_caption("Traffic Intersection Simulation")
        self.clock = pygame.time.Clock()

        # Internal State
        self.max_cars = max_cars
        self.last_reward = 0
        self.last_action = None
        self.repeat_count = 0
        self.cars_waiting = {"N": 0, "S": 0, "W": 0, "E": 0}

        # Create Instances
        self.traffic_lights = [TrafficLight(d) for d in ["N", "S", "W", "E"]]
        self.scheduler = TrafficLightScheduler(self.traffic_lights)
        self.spawner = CarsSpawner(max_cars=self.max_cars)
        self.controller = CarsController(self.spawner.cars, self.traffic_lights)
        self.renderer = DrawUIElements(self.screen)

        logger.info("Started App!")

    def update(self, render_game: bool = False, **kwargs):
        current_epoch = kwargs.get("epoch")
        render_epoch = kwargs.get("render_epoch", False)
        current_decision = kwargs.get("decision")
        render_decision = kwargs.get("render_decision", False)

        # ALL UI ELEMENTS
        if render_game:
            self.screen.fill(ui_constants.UI_COLORS["BLACK"])

            # Render UI Elements
            self.renderer.draw_edge_green_boxes()
            self.renderer.draw_lanes()
            self.renderer.draw_stop_lines()
            self.renderer.draw_traffic_lights(self.traffic_lights)
            self.renderer.show_cars(len(self.spawner.cars))
            self.renderer.show_fps(self.clock)

            if render_epoch and current_epoch is not None:
                self.renderer.show_epoch(current_epoch)

            if render_decision and current_decision is not None:
                self.renderer.show_decision(current_decision)

        # CORE LOGIC
        self.cars_waiting, self.last_reward = self.controller.update_cars_positions(
            self.screen, render_game
        )
        self.spawner.maybe_spawn_car(self.controller.lane_queues)
        self.scheduler.update(self.spawner.cars)

        pygame.display.flip()
        self.clock.tick(ui_constants.FPS)

    def get_state(self) -> tuple:
        def bucket(x):
            return min(x, 5)

        state = tuple(bucket(self.cars_waiting[dir]) for dir in ["N", "S", "W", "E"])

        return (*state, self.scheduler.current_action)

    def compute_reward(self, action):
        # Determine which lanes are served and unserved
        action_dirs = {0: ["N", "S"], 1: ["W", "E"]}

        served_q = sum(
            self.controller.lane_queues[d].get_total_cars() for d in action_dirs[action]
        )
        unserved_q = sum(
            self.controller.lane_queues[d].get_total_cars()
            for d in action_dirs[action ^ 1]
        )
        imbalance_penalty = abs(served_q - unserved_q)

        reward = 1.25 * self.last_reward - 0.3 * unserved_q - 0.2 * imbalance_penalty

        if self.repeat_count >= 3:
            reward -= self.repeat_count * 0.2

        return reward

    def set_light_state(self, action: int):
        if self.last_action is not None and self.last_action == action:
            self.repeat_count += 1
        else:
            self.repeat_count = 1
            self.last_action = action

        self.scheduler.pending_action = action

    def _reset_simulation(self):
        # Internal State
        self.last_reward = 0

        # Create Instances
        self.traffic_lights = [TrafficLight(d) for d in ["N", "S", "W", "E"]]
        self.scheduler = TrafficLightScheduler(self.traffic_lights)
        self.spawner = CarsSpawner(max_cars=self.max_cars)
        self.controller = CarsController(self.spawner.cars, self.traffic_lights)

    def reset(self):
        self._reset_simulation()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
