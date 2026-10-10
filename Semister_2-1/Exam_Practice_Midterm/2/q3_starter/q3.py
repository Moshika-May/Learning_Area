"""
Question 3 Starter: Monolithic MovingObject (30 points)

This starter code has the same monolithic structure as Question 2.
Instead of using inheritance to specialize MovingObject, Question 3 applies
COMPOSITION OVER INHERITANCE (the Strategy / Component pattern).

Your task:
Refactor the responsibilities of rendering and movement into pluggable components:

1. Renderer Components:
   - Base class: `Renderer` with stub `draw(self, screen, x, y, color)`.
   - `CircleRenderer(radius=20)`: encapsulates `_radius` with a read-only @property.
     Overrides `draw(self, screen, x, y, color)` to draw a filled circle centered at (x, y).
   - `BoxRenderer(width=40, height=40)`: encapsulates `_width` and `_height` with read-only @properties.
     Overrides `draw(self, screen, x, y, color)` to draw a filled rectangle at (x, y).

2. Controller Components:
   - Base class: `Controller` with stub `update_position(self, x, y, speed, target=None) -> tuple[float, float]`.
   - `FallingController(radius=20)`: encapsulates `_radius` with a read-only @property.
     Overrides `update_position(...)` to calculate downward motion and respawn at top with a new random x
     when reaching the bottom. Returns updated `(x, y)`.
   - `ChaserController(width=40, height=40)`: encapsulates `_width` and `_height` with read-only @properties.
     Overrides `update_position(...)` to chase `target` and clamp position within the window. Returns updated `(x, y)`.

3. Delegating `MovingObject` Entity:
   - Constructor: `MovingObject(x, y, speed, color, renderer, controller)`.
   - Encapsulates `_x`, `_y`, `_speed`, `_color`, `_renderer`, `_controller` with read-only @properties.
   - `update(self, target=None)`: delegates calculation to its controller:
         `self._x, self._y = self._controller.update_position(self._x, self._y, self._speed, target)`
   - `draw(self, screen)`: delegates rendering to its renderer:
         `self._renderer.draw(screen, self._x, self._y, self._color)`
"""

import sys
import random
import pygame

# Constants & Configurations
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

COLOR_BG = (30, 30, 40)
COLOR_BALL = (230, 50, 50)
COLOR_BOX = (50, 120, 240)


class MovingObject:
    """Monolithic entity with code smell before component refactoring."""

    def __init__(self, x, y, speed, color, kind, radius=20, width=40, height=40):
        self._x = float(x)
        self._y = float(y)
        self._speed = float(speed)
        self._color = color
        self._kind = kind
        self._radius = float(radius)
        self._width = float(width)
        self._height = float(height)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def speed(self):
        return self._speed

    @property
    def color(self):
        return self._color

    def update(self, target=None):
        if self._kind == "falling_ball":
            self._y += self._speed
            if self._y >= SCREEN_HEIGHT:
                self._y = -self._radius
                self._x = float(random.randint(int(self._radius), int(SCREEN_WIDTH - self._radius)))
        elif self._kind == "chaser_box":
            if target is not None:
                tx = target.x if hasattr(target, "x") else target[0]
                ty = target.y if hasattr(target, "y") else target[1]
                cx = self._x + self._width / 2.0
                cy = self._y + self._height / 2.0
                if tx > cx:
                    self._x += min(self._speed, tx - cx)
                elif tx < cx:
                    self._x -= min(self._speed, cx - tx)
                if ty > cy:
                    self._y += min(self._speed, ty - cy)
                elif ty < cy:
                    self._y -= min(self._speed, cy - ty)
            self._x = max(0.0, min(self._x, float(SCREEN_WIDTH - self._width)))
            self._y = max(0.0, min(self._y, float(SCREEN_HEIGHT - self._height)))

    def draw(self, screen):
        if self._kind == "falling_ball":
            pygame.draw.circle(screen, self._color, (int(self._x), int(self._y)), int(self._radius))
        elif self._kind == "chaser_box":
            pygame.draw.rect(
                screen, self._color,
                (int(self._x), int(self._y), int(self._width), int(self._height))
            )


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Q3 Starter: Monolithic Object for Component Refactoring")
    clock = pygame.time.Clock()

    ball = MovingObject(
        x=random.randint(40, SCREEN_WIDTH - 40),
        y=0.0,
        speed=4.0,
        color=COLOR_BALL,
        kind="falling_ball",
        radius=20
    )
    box = MovingObject(
        x=280.0,
        y=520.0,
        speed=3.0,
        color=COLOR_BOX,
        kind="chaser_box",
        width=40,
        height=40
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball.update()
        box.update(target=ball)

        screen.fill(COLOR_BG)
        ball.draw(screen)
        box.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
