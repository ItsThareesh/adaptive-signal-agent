import pygame
import logging
import random
from ui import ui_constants
from . import game_constants


class Car:
    def __init__(self, direction):
        self.ID = 0
        self.direction = direction
        self.color = random.choice(list(ui_constants.CAR_COLORS.values()))
        self.stopped = False

        self._decide_direction()

    def _decide_direction(self):
        if self.direction == 'S':
            self.x = random.choice([ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 4,
                                   ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 4])
            self.y = ui_constants.HEIGHT
            self.vx = 0
            self.vy = -game_constants.CAR_SPEED

        elif self.direction == 'N':
            self.x = random.choice([ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 4,
                                   ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 4])
            self.y = 0
            self.vx = 0
            self.vy = game_constants.CAR_SPEED

        elif self.direction == 'W':
            self.x = 0
            self.y = random.choice([ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 4,
                                   ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 4])
            self.vx = game_constants.CAR_SPEED
            self.vy = 0

        elif self.direction == 'E':
            self.x = ui_constants.WIDTH
            self.y = random.choice([ui_constants.CENTER - ui_constants.LANE_AREA_WIDTH // 4,
                                   ui_constants.CENTER + ui_constants.LANE_AREA_WIDTH // 4])
            self.vx = -game_constants.CAR_SPEED
            self.vy = 0

        else:
            self.logger.fatal(f"Invalid direction: {self.direction}")
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
        rect = pygame.Rect(self.x - game_constants.CAR_SIZE//2, self.y - game_constants.CAR_SIZE//2,
                           game_constants.CAR_SIZE, game_constants.CAR_SIZE)

        pygame.draw.rect(screen, self.color, rect)
