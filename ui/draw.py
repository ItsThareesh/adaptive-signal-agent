import pygame
from . import constants

# Colours
BLACK = (0, 0, 0)
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def draw_edge_green_boxes(screen):
    width, constants.HEIGHT = constants.WIDTH, constants.HEIGHT

    # Top Left Corner
    top_left_rect = pygame.Rect(0, 0, constants.GRASS_BOX_SIZE, constants.GRASS_BOX_SIZE)
    pygame.draw.rect(screen, GREEN, top_left_rect)

    # Bottom Left Corner
    bottom_left_rect = pygame.Rect(0, constants.HEIGHT - constants.GRASS_BOX_SIZE,
                                   constants.GRASS_BOX_SIZE, constants.GRASS_BOX_SIZE)
    pygame.draw.rect(screen, GREEN, bottom_left_rect)

    # Top Right center
    top_right_rect = pygame.Rect(constants.WIDTH - constants.GRASS_BOX_SIZE, 0,
                                 constants.GRASS_BOX_SIZE, constants.GRASS_BOX_SIZE)
    pygame.draw.rect(screen, GREEN, top_right_rect)

    # Bottom Right center
    bottom_right_rect = pygame.Rect(constants.WIDTH - constants.GRASS_BOX_SIZE, constants.HEIGHT -
                                    constants.GRASS_BOX_SIZE, constants.GRASS_BOX_SIZE, constants.GRASS_BOX_SIZE)
    pygame.draw.rect(screen, GREEN, bottom_right_rect)


def draw_lanes(screen):
    # Vertical lanes (North & South)
    north_lane = pygame.Rect(constants.CENTER - constants.LANE_WIDTH, 0, constants.LANE_WIDTH, constants.LANE_LENGTH)
    south_lane = pygame.Rect(constants.CENTER - constants.LANE_WIDTH, constants.HEIGHT - constants.LANE_LENGTH,
                             constants.LANE_WIDTH, constants.LANE_LENGTH)

    # Horizontal lanes (West & East)
    west_lane = pygame.Rect(0, constants.CENTER - constants.LANE_WIDTH, constants.LANE_LENGTH, constants.LANE_WIDTH)
    east_lane = pygame.Rect(constants.WIDTH - constants.LANE_LENGTH, constants.CENTER - constants.LANE_WIDTH,
                            constants.LANE_LENGTH, constants.LANE_WIDTH)

    for lane in [north_lane, south_lane, west_lane, east_lane]:
        pygame.draw.rect(screen, GREY, lane)


def show_fps(screen, clock):
    font = pygame.font.SysFont(None, 24)

    fps = int(clock.get_fps())
    fps_text = font.render(f'FPS: {fps}', True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))
