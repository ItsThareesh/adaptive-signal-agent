import pygame
from game.traffic_light import TrafficLight
from . import ui_constants


def draw_edge_green_boxes(screen):
    width, height = ui_constants.WIDTH, ui_constants.HEIGHT
    grass_bos_size = ui_constants.GRASS_BOX_SIZE

    # Top Left Corner
    top_left_rect = pygame.Rect(0, 0, grass_bos_size, grass_bos_size)

    # Bottom Left Corner
    bottom_left_rect = pygame.Rect(0, height - grass_bos_size, grass_bos_size, grass_bos_size)

    # Top Right center
    top_right_rect = pygame.Rect(width - grass_bos_size, 0, grass_bos_size, grass_bos_size)

    # Bottom Right center
    bottom_right_rect = pygame.Rect(width - grass_bos_size, height - grass_bos_size, grass_bos_size, grass_bos_size)

    for box in [top_left_rect, bottom_left_rect, top_right_rect, bottom_right_rect]:
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREEN'], box)


def draw_lanes(screen):
    height = ui_constants.HEIGHT
    width = ui_constants.WIDTH

    lane_width_offset = ui_constants.LANE_WIDTH // 4
    line_width = ui_constants.LINE_WIDTH
    line_length = ui_constants.LINE_LENGTH
    grass_bos_size = ui_constants.GRASS_BOX_SIZE

    def get_divider_length(iteration: int):
        if iteration == 2:
            return line_width * 2
        else:
            return line_width

    # North Lanes
    for i in range(1, 4):
        left = grass_bos_size + i * lane_width_offset - line_width // 2

        north_lane_line = pygame.Rect(left, 0, get_divider_length(i), line_length)
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREY'], north_lane_line)

    # South Lanes
    for i in range(1, 4):
        left = grass_bos_size + i * lane_width_offset - line_width // 2

        south_lane_line = pygame.Rect(left, height - line_length, get_divider_length(i), line_length)
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREY'], south_lane_line)

    # West Lanes
    for i in range(1, 4):
        top = grass_bos_size + i * lane_width_offset - line_width // 2

        west_lane_line = pygame.Rect(0, top, line_length, get_divider_length(i))
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREY'], west_lane_line)

    # East Lanes
    for i in range(1, 4):
        top = grass_bos_size + i * lane_width_offset - line_width // 2

        east_lane_line = pygame.Rect(width - line_length, top, line_length, get_divider_length(i))
        pygame.draw.rect(screen, ui_constants.UI_COLORS['GREY'], east_lane_line)


def draw_stop_lines(screen):
    color = ui_constants.UI_COLORS['WHITE']

    stop_line_len = 60
    center = ui_constants.CENTER
    half_lane_dst = ui_constants.LANE_WIDTH // 2

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
    x, y = 0, 0

    center = ui_constants.CENTER
    half_lane_dst = ui_constants.LANE_WIDTH // 2
    color = ui_constants.UI_COLORS['RED']

    for tl in traffic_lights:
        if tl.state == 'RED':
            color = ui_constants.UI_COLORS['RED']
        elif tl.state == 'YELLOW':
            color = ui_constants.UI_COLORS['YELLOW']
        elif tl.state == 'GREEN':
            color = ui_constants.UI_COLORS['GREEN']

        if tl.direction == 'N':
            x = center
            y = center - half_lane_dst

        elif tl.direction == 'S':
            x = center
            y = center + half_lane_dst

        elif tl.direction == 'E':
            x = center + half_lane_dst
            y = center

        elif tl.direction == 'W':
            x = center - half_lane_dst
            y = center

        pygame.draw.circle(screen, color, (x, y), radius)


def show_fps(screen, clock):
    font = pygame.font.SysFont("Arial", 16, True)

    fps = int(clock.get_fps())
    fps_text = font.render(f'FPS: {fps}', True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))


def show_cars(screen, total_cars: int):
    font = pygame.font.SysFont("Arial", 16, True)

    cars_text = font.render(f'Total Cars: {total_cars}', True, (0, 0, 0))
    screen.blit(cars_text, (screen.get_width() - 110, 10))


def show_epoch(screen, clock, epoch: int):
    font = pygame.font.SysFont("Arial", 16, True)

    epoch_text = font.render(f'Epoch: {epoch}', True, (0, 0, 0))
    text_rect = epoch_text.get_rect()
    text_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)

    screen.blit(epoch_text, text_rect)
