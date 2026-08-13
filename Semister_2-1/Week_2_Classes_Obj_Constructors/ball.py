import pygame
import random

class Ball:
    def __init__(self, x: int, y: int, radius: int, dx: int, dy: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)

ball = Ball(300, 400, 15, 10, 3)
ball.update()

print(ball.x, ball.y, ball.radius, ball.dx, ball.dy)
