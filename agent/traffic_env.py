import pygame
import sys
from game.cars_controller import CarsController
from game.cars_spawner import CarsSpawner
from game.traffic_light import TrafficLight
from ui import ui_constants
from ui.draw import draw_edge_green_boxes, draw_lanes, draw_stop_lines, draw_traffic_lights, show_fps, show_cars
from utils.logger import logger


class TrafficEnv:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ui_constants.WIDTH, ui_constants.HEIGHT))
        pygame.display.set_caption("Traffic Intersection Simulation")
        self.clock = pygame.time.Clock()

        logger.info("Started App!")

        # Create Instances
        self.traffic_lights = [TrafficLight(d) for d in ['N', 'S', 'W', 'E']]
        self.spawner = CarsSpawner(max_cars=15)
        self.controller = CarsController(self.spawner.cars, self.traffic_lights)

        # Internal State
        self.last_reward = 0
        self.pending_green_dirs = []

    def update(self, train: bool = False):
        # ALL UI ELEMENTS
        if not train:
            self.screen.fill(ui_constants.UI_COLORS['BLACK'])

            # Render UI Elements
            draw_edge_green_boxes(self.screen)
            draw_lanes(self.screen)
            draw_stop_lines(self.screen)
            draw_traffic_lights(self.screen, self.traffic_lights)
            show_cars(self.screen, self.spawner.get_total_cars())
            show_fps(self.screen, self.clock)

        # CORE LOGIC
        if self.pending_green_dirs:
            logger.info("Updating RED lights to GREEN")

            for tl in self.traffic_lights:
                if tl.direction in self.pending_green_dirs:
                    tl.target_state = 'GREEN'

            # Reset after triggering
            self.pending_green_dirs = []

        for tl in self.traffic_lights:
            tl.update_tl()

        self.last_reward = self.controller.update_cars_positions(self.screen, train)
        self.spawner.maybe_spawn_car(self.controller.lane_queues)

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
        green_dirs = ['N', 'S'] if action == 0 else ['E', 'W']
        self.pending_green_dirs = green_dirs

        logger.info(f"Setting GREEN for: {green_dirs}")

        for tl in self.traffic_lights:
            if tl.direction not in green_dirs:
                tl.target_state = 'RED'

    def _reset_simulation(self):
        self.traffic_lights = [TrafficLight(d) for d in ['N', 'S', 'W', 'E']]
        self.spawner = CarsSpawner(max_cars=15)
        self.controller = CarsController(self.spawner.cars, self.traffic_lights)

        self.last_reward = 0
        self.clear_frames = 0
        self.required_clear_frames = 45
        self.pending_green_dirs = []

    def reset(self):
        self._reset_simulation()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
