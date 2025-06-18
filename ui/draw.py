import pygame
from . import ui_constants

# Colours
BLACK = (0, 0, 0)
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def draw_edge_green_boxes(screen):
    width, ui_constants.HEIGHT = ui_constants.WIDTH, ui_constants.HEIGHT

    # Top Left Corner
    top_left_rect = pygame.Rect(0, 0, ui_constants.GRASS_BOX_SIZE, ui_constants.GRASS_BOX_SIZE)

    # Bottom Left Corner
    bottom_left_rect = pygame.Rect(0, ui_constants.HEIGHT - ui_constants.GRASS_BOX_SIZE,
                                   ui_constants.GRASS_BOX_SIZE, ui_constants.GRASS_BOX_SIZE)

    # Top Right center
    top_right_rect = pygame.Rect(ui_constants.WIDTH - ui_constants.GRASS_BOX_SIZE, 0,
                                 ui_constants.GRASS_BOX_SIZE, ui_constants.GRASS_BOX_SIZE)

    # Bottom Right center
    bottom_right_rect = pygame.Rect(ui_constants.WIDTH - ui_constants.GRASS_BOX_SIZE, ui_constants.HEIGHT -
                                    ui_constants.GRASS_BOX_SIZE, ui_constants.GRASS_BOX_SIZE, ui_constants.GRASS_BOX_SIZE)

    for box in [top_left_rect, bottom_left_rect, top_right_rect, bottom_right_rect]:
        pygame.draw.rect(screen, GREY, box)


def draw_lanes(screen):
    # Vertical lanes (North & South)
    north_lane = pygame.Rect(ui_constants.CENTER - ui_constants.LANE_WIDTH, 0, ui_constants.LANE_WIDTH, ui_constants.LANE_LENGTH)
    south_lane = pygame.Rect(ui_constants.CENTER - ui_constants.LANE_WIDTH, ui_constants.HEIGHT - ui_constants.LANE_LENGTH,
                             ui_constants.LANE_WIDTH, ui_constants.LANE_LENGTH)

    # Horizontal lanes (West & East)
    west_lane = pygame.Rect(0, ui_constants.CENTER - ui_constants.LANE_WIDTH, ui_constants.LANE_LENGTH, ui_constants.LANE_WIDTH)
    east_lane = pygame.Rect(ui_constants.WIDTH - ui_constants.LANE_LENGTH, ui_constants.CENTER - ui_constants.LANE_WIDTH,
                            ui_constants.LANE_LENGTH, ui_constants.LANE_WIDTH)

    for lane in [north_lane, south_lane, west_lane, east_lane]:
        pygame.draw.rect(screen, GREY, lane)


def show_fps(screen, clock):
    font = pygame.font.SysFont(None, 24)

    fps = int(clock.get_fps())
    fps_text = font.render(f'FPS: {fps}', True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))
