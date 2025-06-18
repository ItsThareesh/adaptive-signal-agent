import pygame
import sys
from ui.draw import draw_edge_green_boxes, draw_lanes, show_fps
from ui import constants

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Single Intersection Traffic UI")
clock = pygame.time.Clock()
FPS = 30
font = pygame.font.SysFont(None, 24)


def main():
    running = True
    while running:
        screen.fill(constants.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw UI elements
        draw_edge_green_boxes(screen)
        draw_lanes(screen)
        show_fps(screen, clock)

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
