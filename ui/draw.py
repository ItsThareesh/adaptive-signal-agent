import pygame
from . import ui_constants


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
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREEN'], box)


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
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREY'], lane)


def show_fps(screen, clock):
    font = pygame.font.SysFont(None, 24)

    fps = int(clock.get_fps())
    fps_text = font.render(f'FPS: {fps}', True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))


def draw_stop_lines(screen):
    half_lane = ui_constants.LANE_AREA_WIDTH // 2
    stop_line_len = 60
    color = ui_constants.UI_COLORS['WHITE']

    # North-bound stop line
    pygame.draw.line(screen, color, (ui_constants.CENTER - stop_line_len, ui_constants.CENTER - half_lane),
                     (ui_constants.CENTER + stop_line_len, ui_constants.CENTER - half_lane), 2)

    # South-bound
    pygame.draw.line(screen, color, (ui_constants.CENTER - stop_line_len, ui_constants.CENTER + half_lane),
                     (ui_constants.CENTER + stop_line_len, ui_constants.CENTER + half_lane), 2)

    # West-bound
    pygame.draw.line(screen, color, (ui_constants.CENTER - half_lane, ui_constants.CENTER - stop_line_len),
                     (ui_constants.CENTER - half_lane, ui_constants.CENTER + stop_line_len), 2)

    # East-bound
    pygame.draw.line(screen, color, (ui_constants.CENTER + half_lane, ui_constants.CENTER - stop_line_len),
                     (ui_constants.CENTER + half_lane, ui_constants.CENTER + stop_line_len), 2)
