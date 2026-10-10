import math
import random

import pygame

from ball_base import Ball
from config import WIDTH, HEIGHT, FPS, BACKGROUND, random_color

# TODO: implement BouncingBall class that inherits from ball_base.Ball.

class BouncingBall(Ball):
    def __init__(self, center_x, center_y, radius, speed):
        super().__init__(center_x, center_y, radius, speed, random_color())
        angle = random.uniform(0, 2 * math.pi)
        self._dx = speed * math.cos(angle)
        self._dy = speed * math.sin(angle)

    def move(self):
        self._center_x += self._dx
        self._center_y += self._dy
        hit = False
        if self._center_x - self._radius <= 0:
            self._center_x = self._radius;          self._dx = abs(self._dx);   hit = True
        elif self._center_x + self._radius >= WIDTH:
            self._center_x = WIDTH - self._radius;  self._dx = -abs(self._dx);  hit = True
        if self._center_y - self._radius <= 0:
            self._center_y = self._radius;          self._dy = abs(self._dy);   hit = True
        elif self._center_y + self._radius >= HEIGHT:
            self._center_y = HEIGHT - self._radius; self._dy = -abs(self._dy);  hit = True
        if hit:
            self._color = random_color()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Q1 — BouncingBall (inheritance)")
    clock = pygame.time.Clock()

    # TODO: create a list of BouncingBall instances, instead of the global `balls` list in the starter code.
    balls = []
    for _ in range(3):
        ball = BouncingBall(random.randint(100, 700),
                    random.randint(100, 500), 18, 5)
        balls.append(ball)


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
