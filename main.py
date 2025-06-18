import pygame
import sys
from ui.draw import draw_edge_green_boxes, draw_lanes, show_fps
from ui import constants
from ui.car import Car

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Single Intersection Traffic UI")
clock = pygame.time.Clock()


def main():
    running = True
    cars = [Car('N'), Car('S'), Car('W'), Car('E')]

    while running:
        screen.fill(constants.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw UI elements
        draw_edge_green_boxes(screen)
        draw_lanes(screen)
        show_fps(screen, clock)

        for car in cars:
            car.move()
            car.draw(screen)

            if (car.x < -constants.CAR_SIZE or car.x > constants.WIDTH or car.y < -constants.CAR_SIZE or car.y > constants.HEIGHT):
                cars.remove(car)

        # Update the display
        pygame.display.flip()
        clock.tick(constants.FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
