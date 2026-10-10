"""
Question 2 Starter: Monolithic MovingObject Class (30 points)

This file contains a working Pygame program where:
- A ball falls from the top at a random horizontal position at fixed speed.
  Once it reaches the bottom, it falls from the top again with a new random x position.
- A box chases the ball in 2D space, but is clamped so it never leaves the window.

Code Smell / Anti-Pattern:
Both objects are implemented inside a single monolithic `MovingObject` class using an
internal `_kind` string ('falling_ball' vs 'chaser_box') and conditional if/elif branching
in update() and draw().

Your task:
Refactor this monolithic design into an inheritance hierarchy with polymorphism:
1. Base Class `MovingObject`:
   - Constructor: `MovingObject(x, y, speed, color)`
   - Encapsulates `_x`, `_y`, `_speed`, `_color` with read-only @property getters.
   - Provides a helper method `get_center(self) -> tuple[float, float]`.
   - Defines stub methods `update(self, target=None)` and `draw(self, screen)` using `pass`.
2. Subclass `FallingBall`:
   - Inherits from `MovingObject`.
   - Constructor: `FallingBall(x, y, speed, color, radius=20)`. Invokes `super().__init__(...)`.
   - Encapsulates `_radius` with a read-only @property.
   - Overrides `get_center(self)` returning `(self._x, self._y)`.
   - Overrides `update(self, target=None)` to fall downward and respawn at top with a new random x.
   - Overrides `draw(self, screen)` to render the circle.
3. Subclass `ChaserBox`:
   - Inherits from `MovingObject`.
   - Constructor: `ChaserBox(x, y, speed, color, width=40, height=40)`. Invokes `super().__init__(...)`.
   - Encapsulates `_width` and `_height` with read-only @properties.
   - Overrides `get_center(self)` returning `(self._x + self._width / 2.0, self._y + self._height / 2.0)`.
   - Overrides `update(self, target=None)` to chase `target` and stay strictly inside window bounds.
   - Overrides `draw(self, screen)` to render the rectangle.
4. Eliminate the `kind` parameter/attribute entirely and eliminate all type-based if/elif checks.
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
    """Monolithic entity with code smell (type branching / kind flag)."""

    def __init__(self, x, y, speed, color, kind, radius=20, width=40, height=40):
        self._x = float(x)
        self._y = float(y)
        self._speed = float(speed)
        self._color = color
        self._kind = kind  # "falling_ball" or "chaser_box"
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

    @property
    def kind(self):
        return self._kind

    @property
    def radius(self):
        return self._radius

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get_center(self):
        if self._kind == "falling_ball":
            return self._x, self._y
        elif self._kind == "chaser_box":
            return self._x + self._width / 2.0, self._y + self._height / 2.0
        return self._x, self._y

    def update(self, target=None):
        if self._kind == "falling_ball":
            # Fall downward at fixed speed
            self._y += self._speed
            # When reaching bottom, respawn at top with a new random x
            if self._y >= SCREEN_HEIGHT:
                self._y = -self._radius
                self._x = float(random.randint(int(self._radius), int(SCREEN_WIDTH - self._radius)))

        elif self._kind == "chaser_box":
            # Chase target if provided
            if target is not None:
                if hasattr(target, "get_center"):
                    tx, ty = target.get_center()
                elif hasattr(target, "x") and hasattr(target, "y"):
                    tx, ty = target.x, target.y
                else:
                    tx, ty = target[0], target[1]

                cx, cy = self.get_center()
                if tx > cx:
                    self._x += min(self._speed, tx - cx)
                elif tx < cx:
                    self._x -= min(self._speed, cx - tx)
                if ty > cy:
                    self._y += min(self._speed, ty - cy)
                elif ty < cy:
                    self._y -= min(self._speed, cy - ty)

            # Never leave the window (clamp bounds)
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
    pygame.display.set_caption("Q2 Starter: Monolithic MovingObject")
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
