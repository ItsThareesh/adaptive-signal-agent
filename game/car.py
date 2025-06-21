import pygame

import ui.ui_constants
from utils.logger import logger
import random
from ui import ui_constants
from . import game_constants


class Car:
    def __init__(self, direction: str):
        self.ID = 0
        self.direction = direction
        self.color = random.choice(list(ui_constants.CAR_COLORS.values()))
        self.spawned = True

        self._decide_direction()

    def _decide_direction(self):
        height = ui_constants.HEIGHT
        width = ui_constants.WIDTH
        center = ui_constants.CENTER

        lane_width_offset = ui_constants.LANE_WIDTH // 8
        line_width = ui_constants.LINE_WIDTH
        line_length = ui_constants.LINE_LENGTH
        grass_bos_size = ui_constants.GRASS_BOX_SIZE

        if self.direction == 'N':
            self.x = random.choice([grass_bos_size + lane_width_offset, center - lane_width_offset])
            self.y = 0

            self.vx = 0
            self.vy = game_constants.CAR_SPEED

        elif self.direction == 'S':
            self.x = random.choice([center + lane_width_offset, width - grass_bos_size - lane_width_offset])
            self.y = ui_constants.HEIGHT

            self.vx = 0
            self.vy = -game_constants.CAR_SPEED

        elif self.direction == 'W':
            self.x = 0
            self.y = random.choice([center + lane_width_offset, height - grass_bos_size - lane_width_offset])

            self.vx = game_constants.CAR_SPEED
            self.vy = 0

        elif self.direction == 'E':
            self.x = ui_constants.WIDTH
            self.y = random.choice([grass_bos_size + lane_width_offset, center - lane_width_offset])

            self.vx = -game_constants.CAR_SPEED
            self.vy = 0

        else:
            logger.fatal(f"Invalid direction: {self.direction}")
            raise

    def is_out_of_bounds(self):
        left_bound = 0 - game_constants.CAR_SIZE
        right_bound = ui_constants.WIDTH + game_constants.CAR_SIZE
        top_bound = 0 - game_constants.CAR_SIZE
        bottom_bound = ui_constants.HEIGHT + game_constants.CAR_SIZE

        if self.x < left_bound or self.x > right_bound or self.y < top_bound or self.y > bottom_bound:
            return True
        else:
            return False

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        car_offset = game_constants.CAR_SIZE // 2

        rect = pygame.Rect(self.x - car_offset, self.y - car_offset, game_constants.CAR_SIZE, game_constants.CAR_SIZE)
        pygame.draw.rect(screen, self.color, rect)
