import pygame
from . import constants

# Colours
BLACK = (0, 0, 0)
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def draw_edge_green_boxes(screen):
    BOX_SIZE = 225
    width, constants.HEIGHT = constants.WIDTH, constants.HEIGHT

    # Top Left Corner
    top_left_rect = pygame.Rect(0, 0, BOX_SIZE, BOX_SIZE)
    pygame.draw.rect(screen, GREEN, top_left_rect)

    # Bottom Left Corner
    bottom_left_rect = pygame.Rect(0, constants.HEIGHT - BOX_SIZE, BOX_SIZE, BOX_SIZE)
    pygame.draw.rect(screen, GREEN, bottom_left_rect)

    # Top Right center
    top_right_rect = pygame.Rect(constants.WIDTH - BOX_SIZE, 0, BOX_SIZE, BOX_SIZE)
    pygame.draw.rect(screen, GREEN, top_right_rect)

    # Bottom Right center
    bottom_right_rect = pygame.Rect(constants.WIDTH - BOX_SIZE, constants.HEIGHT - BOX_SIZE, BOX_SIZE, BOX_SIZE)
    pygame.draw.rect(screen, GREEN, bottom_right_rect)


def draw_lanes(screen):
    LANE_WIDTH = 15
    LANE_LENGTH = 200
    CENTER = constants.WIDTH // 2

    # Vertical lanes (North & South)
    north_lane = pygame.Rect(CENTER - LANE_WIDTH, 0, LANE_WIDTH, LANE_LENGTH)
    pygame.draw.rect(screen, GREY, north_lane)

    south_lane = pygame.Rect(CENTER - LANE_WIDTH, constants.HEIGHT - LANE_LENGTH, LANE_WIDTH, LANE_LENGTH)
    pygame.draw.rect(screen, GREY, south_lane)

    # Horizontal lanes (West & East)
    west_lane = pygame.Rect(0, CENTER - LANE_WIDTH, LANE_LENGTH, LANE_WIDTH)
    pygame.draw.rect(screen, GREY, west_lane)

    east_lane = pygame.Rect(constants.WIDTH - LANE_LENGTH, CENTER - LANE_WIDTH, LANE_LENGTH, LANE_WIDTH)
    pygame.draw.rect(screen, GREY, east_lane)


def show_fps(screen, clock):
    font = pygame.font.SysFont(None, 24)

    fps = int(clock.get_fps())
    fps_text = font.render(f'FPS: {fps}', True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))
