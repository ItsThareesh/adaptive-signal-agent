import pygame
import sys
from ui.draw import draw_edge_green_boxes, draw_lanes, show_fps, draw_stop_lines
from ui import ui_constants
from game.traffic_light import TrafficLight
from game.car_spawner import CarSpawner
from utils.logger import logger

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((ui_constants.WIDTH, ui_constants.HEIGHT))
pygame.display.set_caption("Traffic Intersection Simulation")
clock = pygame.time.Clock()

# Create Instances
spawner = CarSpawner(max_cars=5)
traffic_lights = [TrafficLight(d) for d in ['N', 'S', 'W', 'E']]


def main():
    running = True
    logger.info("Started App!")

    while running:
        screen.fill(ui_constants.UI_COLORS['BLACK'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw UI elements
        draw_edge_green_boxes(screen)
        draw_lanes(screen)
        draw_stop_lines(screen)

        # # Spawn Cars
        # for tl in traffic_lights:
        #     tl.update()

        spawner.maybe_spawn_car()
        spawner.update_cars(screen, traffic_lights)

        # Show FPS
        show_fps(screen, clock)

        # Update the display
        pygame.display.flip()
        clock.tick(ui_constants.FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
