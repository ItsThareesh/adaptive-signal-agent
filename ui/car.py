import pygame
from . import constants
import random


class Car:
    def __init__(self, direction):
        self.direction = direction
        self.color = constants.CAR_COLOR

        self._decide_direction()

    def _decide_direction(self):
        if self.direction == 'N':
            self.x = random.choice([constants.CENTER - constants.LANE_AREA_WIDTH // 4,
                                   constants.CENTER + constants.LANE_AREA_WIDTH // 4])
            self.y = constants.HEIGHT
            self.vx = 0
            self.vy = -constants.CAR_SPEED

        elif self.direction == 'S':
            self.x = random.choice([constants.CENTER - constants.LANE_AREA_WIDTH // 4,
                                   constants.CENTER + constants.LANE_AREA_WIDTH // 4])
            self.y = 0
            self.vx = 0
            self.vy = constants.CAR_SPEED

        elif self.direction == 'W':
            self.x = 0
            self.y = random.choice([constants.CENTER - constants.LANE_AREA_WIDTH // 4,
                                   constants.CENTER + constants.LANE_AREA_WIDTH // 4])
            self.vx = constants.CAR_SPEED
            self.vy = 0

        elif self.direction == 'E':
            self.x = constants.WIDTH
            self.y = random.choice([constants.CENTER - constants.LANE_AREA_WIDTH // 4,
                                   constants.CENTER + constants.LANE_AREA_WIDTH // 4])
            self.vx = -constants.CAR_SPEED
            self.vy = 0

        else:
            raise ValueError(f"Invalid direction: {self.direction}")

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        rect = pygame.Rect(self.x - constants.CAR_SIZE//2, self.y - constants.CAR_SIZE//2, constants.CAR_SIZE, constants.CAR_SIZE)
        pygame.draw.rect(screen, self.color, rect)
