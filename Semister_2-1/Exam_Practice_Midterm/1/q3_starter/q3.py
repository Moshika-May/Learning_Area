import math

import pygame

from config import WIDTH, HEIGHT, FPS, BACKGROUND

class Ball:
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Q3 — composition (WASD/arrows)")
    clock = pygame.time.Clock()


    # TODO: create a few Ball instances with different controllers and add them to the `balls` list.
    player = Ball(20, "white", controller=KeyboardController(WIDTH / 2, HEIGHT / 2, 5))
    enemy = Ball(14, "red", controller=ChasingController(40, 40, 3, player))
    balls = [player, enemy] 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for ball in balls:          # identical treatment, no type test
            ball.move()

        screen.fill(BACKGROUND)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
