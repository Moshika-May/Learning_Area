"""
Q4 STARTER — skeleton only. Fill in the TODOs.

Constraint: the update and draw loops must contain NO isinstance() call and
NO branching on object type.
"""

import math
import random

import pygame

from ball_base import Ball
from config import WIDTH, HEIGHT, FPS, BACKGROUND, random_color



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



class ControlledBall:
    """Owns appearance and drawing only. Movement is delegated."""

    def __init__(self, radius, color, controller):
        self._radius = radius
        self._color = color
        self._controller = controller
        # The controller is the single source of truth for position.
        self._center_x = controller.x
        self._center_y = controller.y

    @property
    def center_x(self):
        return self._center_x

    @property
    def center_y(self):
        return self._center_y

    @property
    def radius(self):
        return self._radius

    @property
    def color(self):
        return self._color

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, new_controller):
        """Swapping behaviour at RUN TIME — impossible with subclassing."""
        self._controller = new_controller

    def draw(self, screen):
        pygame.draw.circle(screen, self._color,
                           (int(self._center_x), int(self._center_y)),
                           self._radius)

    def move(self):
        self._controller.move()                # 1. delegate
        self._center_x = self._controller.x    # 2. sync
        self._center_y = self._controller.y

class Controller:
    def __init__(self, x, y, speed):
        self._x = x
        self._y = y
        self._speed = speed

    @property
    def x(self):
        return (self._x)

    @property
    def y(self):
       return (self._y)

    @property
    def speed(self):
       return (self._speed)

    def move(self):
       ...

class KeyboardController(Controller):
    def move(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx += -1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy += -1

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        length = math.hypot(dx, dy)
        if length != 0:
            self._x += self._speed * dx / length
            self._y += self._speed * dy / length

        if self._x <= 0:
            self._x = 0        
        elif self._x >= WIDTH:
            self._x = WIDTH 
        if self._y <= 0:
            self._y = 0
        elif self._y >= HEIGHT:
            self._y = HEIGHT 

class ChasingController(Controller):
    def __init__(self, x, y, speed, target):
        super().__init__(x, y, speed)
        self._target = target

    def move(self):
        if math.hypot(self._target.center_x - self._x,
                      self._target.center_y - self._y) <= self._speed:
            self._x = self._target.center_x
            self._y = self._target.center_y
            return
        dx = 0
        dy = 0
        if self._target.center_x > self._x:
            dx += 1
        elif self._target.center_x < self._x:
            dx += -1
        if self._target.center_y > self._y:
            dy += 1
        elif self._target.center_y < self._y:
            dy += -1
        length = math.hypot(dx, dy)
        if (length != 0):
            self._x += self._speed * dx / length
            self._y += self._speed * dy / length

        if self._x <= 0:
            self._x = 0        
        elif self._x >= WIDTH:
            self._x = WIDTH 
        if self._y <= 0:
            self._y = 0
        elif self._y >= HEIGHT:
            self._y = HEIGHT


def build_scene():
    """Return a single list containing every object in the scene.

    TODO: 3 x BouncingBall (Q1)
    TODO: 1 x CircularBall + 1 x HorizontalBall (Q2)
    TODO: 1 x keyboard-controlled ball + 1 x ball chasing it (Q3)

    Hint: Q1/Q2 balls inherit from Ball; Q3 balls COMPOSE a Controller.
    Part (b) asks you to reconcile the two designs first.
    """
    balls = [BouncingBall(random.randint(100, 700), random.randint(100, 500), 18, 5)
             for _ in range(3)]
    balls.append(CircularBall(12, 4, "cyan", orbit_radius=150))
    balls.append(HorizontalBall(25, 6, "yellow"))
    player = ControlledBall(20, "white", controller=KeyboardController(WIDTH / 2, HEIGHT / 2, 5))
    balls.append(player)
    balls.append(ControlledBall(14, "red", ChasingController(40, 40, 3, player)))
    return balls


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Q4")
    clock = pygame.time.Clock()

    balls = build_scene()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND)   
        for ball in balls:
            ball.move()
        for ball in balls:
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
