import pygame
import sys
from ui.draw import draw_edge_green_boxes, draw_lanes, show_fps
from ui import ui_constants
from game.car_spawner import maybe_spawn_car, update_cars

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((ui_constants.WIDTH, ui_constants.HEIGHT))
pygame.display.set_caption("Single Intersection Traffic UI")
clock = pygame.time.Clock()


def main():
    running = True

    while running:
        screen.fill(ui_constants.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw UI elements
        draw_edge_green_boxes(screen)
        draw_lanes(screen)
        maybe_spawn_car()
        update_cars(screen)
        show_fps(screen, clock)

        # Update the display
        pygame.display.flip()
        clock.tick(ui_constants.FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
