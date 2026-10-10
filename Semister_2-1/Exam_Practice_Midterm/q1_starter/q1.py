import math
import random

import pygame

from ball_base import Ball
from config import WIDTH, HEIGHT, FPS, BACKGROUND, random_color

# TODO: implement BouncingBall class that inherits from ball_base.Ball.

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Q1 — BouncingBall (inheritance)")
    clock = pygame.time.Clock()

    # TODO: create a list of BouncingBall instances, instead of the global `balls` list in the starter code.
    balls = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for ball in balls:
            ball.move()

        screen.fill(BACKGROUND)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()