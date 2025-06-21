import pygame
from game.traffic_light import TrafficLight
from . import ui_constants


def draw_edge_green_boxes(screen):
    width, height = ui_constants.WIDTH, ui_constants.HEIGHT
    grass_bos_size = ui_constants.GRASS_BOX_SIZE

    # Top Left Corner
    top_left_rect = pygame.Rect(0, 0, grass_bos_size, grass_bos_size)

    # Bottom Left Corner
    bottom_left_rect = pygame.Rect(0, height - grass_bos_size,
                                   grass_bos_size, grass_bos_size)

    # Top Right center
    top_right_rect = pygame.Rect(ui_constants.WIDTH - grass_bos_size, 0,
                                 grass_bos_size, grass_bos_size)

    # Bottom Right center
    bottom_right_rect = pygame.Rect(ui_constants.WIDTH - grass_bos_size, height -
                                    grass_bos_size, grass_bos_size, grass_bos_size)

    for box in [top_left_rect, bottom_left_rect, top_right_rect, bottom_right_rect]:
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREEN'], box)


def draw_lanes(screen):
    height = ui_constants.HEIGHT
    center = ui_constants.CENTER
    lane_line_width_offset = ui_constants.LANE_LINE_WIDTH
    lane_line_length = ui_constants.LANE_LENGTH

    # Vertical lanes (North & South)
    north_lane = pygame.Rect(center - lane_line_width_offset // 2, 0, lane_line_width_offset, lane_line_length)
    south_lane = pygame.Rect(center - lane_line_width_offset // 2, height - lane_line_length,
                             lane_line_width_offset, lane_line_length)

    # Horizontal lanes (West & East)
    west_lane = pygame.Rect(0, center - lane_line_width_offset // 2, lane_line_length, lane_line_width_offset)
    east_lane = pygame.Rect(ui_constants.WIDTH - lane_line_length, center - lane_line_width_offset // 2,
                            lane_line_length, lane_line_width_offset)

    for lane in [north_lane, south_lane, west_lane, east_lane]:
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREY'], lane)


def draw_stop_lines(screen):
    color = ui_constants.UI_COLORS['WHITE']

    stop_line_len = 60
    center = ui_constants.CENTER
    half_lane_dst = ui_constants.LANE_AREA_WIDTH // 2

    # North-bound stop line
    pygame.draw.line(screen, color, (center - stop_line_len, center - half_lane_dst),
                     (center + stop_line_len, center - half_lane_dst), 2)

    # South-bound
    pygame.draw.line(screen, color, (center - stop_line_len, center + half_lane_dst),
                     (center + stop_line_len, center + half_lane_dst), 2)

    # West-bound
    pygame.draw.line(screen, color, (center - half_lane_dst, center - stop_line_len),
                     (center - half_lane_dst, center + stop_line_len), 2)

    # East-bound
    pygame.draw.line(screen, color, (center + half_lane_dst, center - stop_line_len),
                     (center + half_lane_dst, center + stop_line_len), 2)


def draw_traffic_lights(screen, traffic_lights: list[TrafficLight]):
    radius = 10
    padding = 17
    x, y = 0, 0

    center = ui_constants.CENTER
    half_lane_dst = ui_constants.LANE_AREA_WIDTH // 2

    for tl in traffic_lights:
        color = ui_constants.UI_COLORS['GREEN'] if tl.state == 'GREEN' else ui_constants.UI_COLORS['RED']

        if tl.direction == 'N':
            x = center
            y = center - half_lane_dst - padding

        elif tl.direction == 'S':
            x = center
            y = center + half_lane_dst + padding

        elif tl.direction == 'E':
            x = center + half_lane_dst + padding
            y = center

        elif tl.direction == 'W':
            x = center - half_lane_dst - padding
            y = center

        pygame.draw.circle(screen, color, (x, y), radius)


def show_fps(screen, clock):
    font = pygame.font.SysFont("Arial", 16, True)

    fps = int(clock.get_fps())
    fps_text = font.render(f'FPS: {fps}', True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))