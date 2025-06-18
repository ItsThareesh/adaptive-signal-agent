import pygame
import sys
from ui.draw import draw_edge_green_boxes, draw_lanes, show_fps
from ui import ui_constants
from game.car_spawner import CarSpawner

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((ui_constants.WIDTH, ui_constants.HEIGHT))
pygame.display.set_caption("Traffic Intersection Simulation")
clock = pygame.time.Clock()


# Create Spawner Instance
spawner = CarSpawner()


def main():
    running = True

    while running:
        screen.fill(ui_constants.UI_COLORS['BLACK'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw UI elements
        draw_edge_green_boxes(screen)
        draw_lanes(screen)

        # Spawn Cars
        spawner.maybe_spawn_car()
        spawner.update_cars(screen)

        # Show FPS
        show_fps(screen, clock)

        # Update the display
        pygame.display.flip()
        clock.tick(ui_constants.FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
