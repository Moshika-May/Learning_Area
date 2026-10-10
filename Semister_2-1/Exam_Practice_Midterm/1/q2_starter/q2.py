import math

import pygame

from ball_base import Ball
from config import WIDTH, HEIGHT, FPS, BACKGROUND


#TODO: implement CircularBall and HorizontalBall classes that inherit from ball_base.Ball.
class CircularBall(Ball):
   def __init__(self, radius, speed, color, orbit_radius=0, start_angle=0.0):
        self._orbit_radius = orbit_radius    # unused when horizontal
        self._angle = start_angle            # unused when horizontal
        self._orbit_center_x = WIDTH / 2     # unused when horizontal
        self._orbit_center_y = HEIGHT / 2    # unused when horizontal
        super().__init__(
            self._orbit_center_x + \
            orbit_radius * math.cos(start_angle),
            self._orbit_center_y + \
            orbit_radius * math.sin(start_angle),
            radius,
            speed,
            color
            )
         
   def move(self):
        self._angle += self._speed / self._orbit_radius
        self._angle %= 2 * math.pi
        self._center_x = self._orbit_center_x + \
        self._orbit_radius * math.cos(self._angle)
        self._center_y = self._orbit_center_y + \
        self._orbit_radius * math.sin(self._angle)

class HorizontalBall(Ball):
    def __init__(self, radius, speed, color):
        super().__init__(
            -radius,
            HEIGHT / 2,
            radius,
            speed,
            color
        )

    def move(self):
       self._center_x += self._speed
       if self._center_x - self._radius > WIDTH:
           self._center_x = -self._radius 

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Q2 — polymorphic motion")
    clock = pygame.time.Clock()

    # TODO: create a list of CircularBall and HorizontalBall instances.
    balls = [
        CircularBall(12, 4, "cyan", orbit_radius=150),
        CircularBall(8, 4, "magenta", orbit_radius=80, start_angle=math.pi),
        HorizontalBall(25, 6, "yellow"),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for ball in balls:          # no isinstance, no type test
            ball.move()

        screen.fill(BACKGROUND)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
