import pygame
import sys
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
        self.last_reward = 0
        self.max_cars = max_cars

        # Create Instances
        self.traffic_lights = [TrafficLight(d) for d in ['N', 'S', 'W', 'E']]
        self.scheduler = TrafficLightScheduler(self.traffic_lights)
        self.spawner = CarsSpawner(max_cars=self.max_cars)
        self.controller = CarsController(self.spawner.cars, self.traffic_lights)
        self.renderer = DrawUIElements(self.screen)

        logger.info("Started App!")

    def update(self, train: bool = False, **kwargs):
        current_epoch = kwargs.get("epoch")
        render_epoch = kwargs.get("render_epoch", False)

        # ALL UI ELEMENTS
        if not train:
            self.screen.fill(ui_constants.UI_COLORS['BLACK'])

            # Render UI Elements
            self.renderer.draw_edge_green_boxes()
            self.renderer.draw_lanes()
            self.renderer.draw_stop_lines()
            self.renderer.draw_traffic_lights(self.traffic_lights)
            self.renderer.show_cars(len(self.spawner.cars))
            self.renderer.show_fps(self.clock)

            if render_epoch and current_epoch is not None:
                self.renderer.show_epoch(current_epoch)

        # CORE LOGIC
        self.last_reward = self.controller.update_cars_positions(self.screen, train)
        self.spawner.maybe_spawn_car(self.controller.lane_queues)
        self.scheduler.update(self.spawner.cars)

        if not train:
            pygame.display.flip()
            self.clock.tick(ui_constants.FPS)

    def get_state(self) -> tuple:
        n_s_bucket = self.controller.lane_queues['N'].get_total_cars() + self.controller.lane_queues['S'].get_total_cars()
        w_e_bucket = self.controller.lane_queues['W'].get_total_cars() + self.controller.lane_queues['E'].get_total_cars()

        def bucket(x):
            if x == 0:
                return 0
            elif x <= 2:
                return 1
            elif x <= 5:
                return 3
            else:
                return 5

        return bucket(n_s_bucket), bucket(w_e_bucket)

    def compute_reward(self, action):
        # Get total cars in both directions
        if action == 0:
            penalty = self.controller.lane_queues['E'].get_total_cars() + \
                self.controller.lane_queues['W'].get_total_cars()
        else:
            penalty = self.controller.lane_queues['N'].get_total_cars() + \
                self.controller.lane_queues['S'].get_total_cars()

        # Weighted reward
        reward = 2 * self.last_reward - (0.5 * penalty)
        return reward

    def set_light_state(self, action: int):
        self.scheduler.pending_action = action

    def _reset_simulation(self):
        # Internal State
        self.last_reward = 0

        # Create Instances
        self.traffic_lights = [TrafficLight(d) for d in ['N', 'S', 'W', 'E']]
        self.scheduler = TrafficLightScheduler(self.traffic_lights)
        self.spawner = CarsSpawner(max_cars=self.max_cars)
        self.controller = CarsController(self.spawner.cars, self.traffic_lights)

    def reset(self):
        self._reset_simulation()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
