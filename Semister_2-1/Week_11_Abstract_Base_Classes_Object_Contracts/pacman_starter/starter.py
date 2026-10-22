"""Week 11 Starter Code: Abstract Base Classes and Object Contracts.

STUDENT INSTRUCTIONS:
In lecture, you learned how Abstract Base Classes (ABCs) act as structural gatekeepers:
they enforce formal method contracts across subclasses, preventing runtime AttributeError
crashes by failing fast at instantiation time with a clear TypeError.

In this lab, you will enforce formal object contracts across the Pacman Arena:

  - Task 1: Convert `GameObject` into an Abstract Base Class by inheriting from `ABC`
            and decorating `update()` and `draw()` with `@abstractmethod`.
  - Task 2: Implement `IncompleteCherry` (inheriting from `GameObject`) that implements
            `update()` but deliberately omits `draw()`. Verify that Python refuses to
            instantiate it, raising a TypeError.
  - Task 3: Implement concrete `Cherry` (inheriting from `GameObject`) that fully satisfies
            the contract by implementing both `update()` (bobbing animation) and `draw()`.
  - Task 4: Integrate `Cherry` into the polymorphic arena loop with `Pacman`, `Ghost`,
            and `Pellet` instances without any type checks.

Verify your implementation with automated tests:
    python3 code/week11/starter.py --check
Or run the interactive demonstration:
    python3 code/week11/starter.py
"""

import argparse
from abc import ABC, abstractmethod
import math
import sys

try:
    import pygame
except ImportError:
    # Minimal mock for running unit checks in environments without pygame installed
    class _MockPygame:
        K_RIGHT = 1
        K_LEFT = 2
        K_DOWN = 3
        K_UP = 4
        K_d = 5
        K_a = 6
        K_s = 7
        K_w = 8

        class Rect:
            def __init__(self, x=0, y=0, width=0, height=0):
                self.x = x
                self.y = y
                self.width = width
                self.height = height

            @property
            def left(self):
                return self.x

            @property
            def right(self):
                return self.x + self.width

            @property
            def top(self):
                return self.y

            @property
            def bottom(self):
                return self.y + self.height

            @property
            def centerx(self):
                return self.x + self.width // 2

            @property
            def centery(self):
                return self.y + self.height // 2

            @property
            def center(self):
                return (self.centerx, self.centery)

            @property
            def topleft(self):
                return (self.x, self.y)

            @topleft.setter
            def topleft(self, value):
                self.x, self.y = value

            def copy(self):
                return _MockPygame.Rect(self.x, self.y, self.width, self.height)

            def colliderect(self, other):
                return not (
                    self.right <= other.x
                    or self.x >= other.right
                    or self.bottom <= other.y
                    or self.y >= other.bottom
                )

            def clamp_ip(self, bounds):
                if self.x < bounds.x:
                    self.x = bounds.x
                elif self.right > bounds.right:
                    self.x = bounds.right - self.width
                if self.y < bounds.y:
                    self.y = bounds.y
                elif self.bottom > bounds.bottom:
                    self.y = bounds.bottom - self.height

        class Surface:
            def __init__(self, size):
                self.size = size

            def fill(self, color):
                pass

            def get_rect(self, topleft=(0, 0)):
                return _MockPygame.Rect(topleft[0], topleft[1], self.size[0], self.size[1])

            def blit(self, image, rect):
                pass

    pygame = _MockPygame()


WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (20, 24, 40)
PACMAN_COLOR = (255, 238, 0)
BLINKY_COLOR = (235, 60, 60)
PELLET_COLOR = (255, 183, 77)
CHERRY_COLOR = (220, 20, 60)
STEM_COLOR = (46, 139, 87)


# =============================================================================
# TASK 1: Define GameObject as an Abstract Base Class (ABC)
# =============================================================================
# Make GameObject an Abstract Base Class.
# Establish the object contract by making update() and draw() abstract methods.
# =============================================================================

class GameObject(ABC):
    """Base class defining the mandatory contract for all game entities."""

    def __init__(self, x, y, speed, size, color):
        self.x = float(x)
        self.y = float(y)
        self.speed = float(speed)
        self.color = color
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(round(x), round(y)))
        self.active = True

    def sync_position(self):
        """Keep Pygame bounding box aligned with internal float coordinates."""
        self.rect.topleft = (round(self.x), round(self.y))

    @abstractmethod
    def update(self, bounds=None):
        """Advance entity state by one frame. Mandatory for all subclasses."""
        pass

    @abstractmethod
    def draw(self, screen):
        """Render entity to the target surface. Mandatory for all subclasses."""
        pass


# =============================================================================
# Concrete Game Entities Fulfilling the Contract
# =============================================================================

class Pacman(GameObject):
    """Player-controlled Pacman satisfying the GameObject contract."""

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            speed=5.0,
            size=(36, 36),
            color=PACMAN_COLOR,
        )
        self.facing_angle = 0.0
        self.mouth_phase = 0

    def update(self, bounds=None, controls=None):
        if controls is None:
            try:
                if hasattr(pygame, "key") and hasattr(pygame.key, "get_pressed"):
                    controls = pygame.key.get_pressed()
            except Exception:
                controls = {}
            if controls is None:
                controls = {}

        def is_pressed(key):
            if hasattr(controls, "get"):
                return controls.get(key, False)
            try:
                return bool(controls[key])
            except (IndexError, KeyError):
                return False

        dx = int(is_pressed(pygame.K_RIGHT) or is_pressed(pygame.K_d))
        dx -= int(is_pressed(pygame.K_LEFT) or is_pressed(pygame.K_a))
        dy = int(is_pressed(pygame.K_DOWN) or is_pressed(pygame.K_s))
        dy -= int(is_pressed(pygame.K_UP) or is_pressed(pygame.K_w))

        if dx or dy:
            self.facing_angle = math.atan2(dy, dx)
            self.mouth_phase += 1
        else:
            self.mouth_phase = 0

        self.x += dx * self.speed
        self.y += dy * self.speed
        self.sync_position()

        if bounds is not None:
            self.rect.clamp_ip(bounds)
            self.x, self.y = self.rect.topleft

    def draw(self, screen):
        if not self.active:
            return

        if not hasattr(pygame, "draw"):
            screen.blit(self.image, self.rect)
            return

        center = self.rect.center
        radius = self.rect.width // 2
        mouth_open = 0.25 + 0.18 * abs(math.sin(self.mouth_phase * 0.35))
        upper_angle = self.facing_angle + mouth_open
        lower_angle = self.facing_angle - mouth_open
        mouth_tip = (
            center[0] + radius * math.cos(self.facing_angle),
            center[1] + radius * math.sin(self.facing_angle),
        )
        upper_point = (
            center[0] + radius * math.cos(upper_angle),
            center[1] + radius * math.sin(upper_angle),
        )
        lower_point = (
            center[0] + radius * math.cos(lower_angle),
            center[1] + radius * math.sin(lower_angle),
        )

        pygame.draw.circle(screen, PACMAN_COLOR, center, radius)
        pygame.draw.polygon(
            screen,
            BACKGROUND_COLOR,
            [center, upper_point, mouth_tip, lower_point],
        )


class Ghost(GameObject):
    """Enemy Ghost entity satisfying the GameObject contract."""

    def __init__(self, x, y, color=BLINKY_COLOR, speed=2.5):
        super().__init__(
            x=x,
            y=y,
            speed=speed,
            size=(36, 36),
            color=color,
        )
        self.direction = 1

    def update(self, bounds=None):
        self.x += self.speed * self.direction
        self.sync_position()
        if bounds is not None:
            if self.rect.left <= bounds.left or self.rect.right >= bounds.right:
                self.direction *= -1
                self.rect.clamp_ip(bounds)
                self.x, self.y = self.rect.topleft

    def draw(self, screen):
        if not self.active:
            return

        if not hasattr(pygame, "draw"):
            screen.blit(self.image, self.rect)
            return

        body = self.rect
        center_x = body.centerx
        radius = body.width // 2

        pygame.draw.circle(screen, self.color, (center_x, body.top + radius), radius)
        pygame.draw.rect(
            screen,
            self.color,
            (body.left, body.top + radius, body.width, body.height - radius),
        )
        eye_radius = 4
        pupil_radius = 2
        left_eye = (center_x - 6, body.top + 12)
        right_eye = (center_x + 6, body.top + 12)
        pygame.draw.circle(screen, (255, 255, 255), left_eye, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), right_eye, eye_radius)
        pygame.draw.circle(screen, (0, 0, 180), (left_eye[0] + self.direction, left_eye[1]), pupil_radius)
        pygame.draw.circle(screen, (0, 0, 180), (right_eye[0] + self.direction, right_eye[1]), pupil_radius)


class Pellet(GameObject):
    """Static collectible pellet satisfying the GameObject contract."""

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            speed=0.0,
            size=(10, 10),
            color=PELLET_COLOR,
        )

    def update(self, bounds=None):
        self.sync_position()

    def draw(self, screen):
        if not self.active:
            return
        if hasattr(pygame, "draw"):
            pygame.draw.circle(screen, PELLET_COLOR, self.rect.center, 5)
        else:
            screen.blit(self.image, self.rect)


# =============================================================================
# TASK 2: Create IncompleteCherry Subclass (Demonstrating Fail-Fast Gatekeeping)
# =============================================================================
# Subclass GameObject, implement update(), but deliberately omit draw().
# Observe that Python refuses to instantiate this object with a TypeError!
# =============================================================================

class IncompleteCherry(GameObject):
    """Demonstration subclass that omits draw() to trigger TypeError."""

    def __init__(self, x, y):
        """Initialize IncompleteCherry with base GameObject state.
        
        TODO Task 2:
        - Call parent constructor with position (x, y), speed 0.0, size (28, 28), and CHERRY_COLOR.
        """
        super().__init__(x=x, y=y, speed=0.0, size=(28, 28), color=CHERRY_COLOR)

    def update(self, bounds=None):
        """Update position.
        
        TODO Task 2:
        - Synchronize rect position with float coordinates.
        """
        self.sync_position()

    # Deliberately do NOT define draw() here!


# =============================================================================
# TASK 3: Implement Concrete Cherry Fulfilling the Contract
# =============================================================================
# Subclass GameObject and fulfill the contract:
# 1. __init__(x, y) - Call parent constructor with CHERRY_COLOR and size (28, 28)
# 2. update(bounds) - Animate vertical bobbing
# 3. draw(screen)   - Render the twin cherries visual onto the screen surface
# =============================================================================

class Cherry(GameObject):
    """Bonus collectible fruit fully satisfying the GameObject contract."""

    def __init__(self, x, y):
        """Initialize Cherry entity.
        
        TODO Task 3:
        - Call parent constructor with position (x, y), speed 0.0, size (28, 28), and CHERRY_COLOR.
        - Store self.base_y = float(y) to anchor the vertical bobbing.
        - Initialize self.bob_phase = 0.0.
        """
        super().__init__(x=x, y=y, speed=0.0, size=(28, 28), color=CHERRY_COLOR)
        self.base_y = float(y)
        self.bob_phase = 0.0

    def update(self, bounds=None):
        """Bob up and down gently to attract the player.
        
        TODO Task 3:
        - Advance self.bob_phase by 0.08 each frame.
        - Update vertical position using sinusoidal bobbing formula:
            self.y = self.base_y + math.sin(self.bob_phase) * 6.0
        - Synchronize rect position with float coordinates.
        """
        self.bob_phase += 0.08
        self.y = self.base_y + math.sin(self.bob_phase) * 6.0
        self.sync_position()

    def draw(self, screen):
        """Draw twin cherries connected by green stems.
        
        TODO Task 3:
        - If not self.active, return early.
        - If pygame.draw is not available, fallback to screen.blit(self.image, self.rect).
        - Otherwise, draw twin cherries with stems using these geometry coordinates:
            center = self.rect.center
            left_bulb = (center[0] - 6, center[1] + 4)
            right_bulb = (center[0] + 6, center[1] + 6)
            stem_top = (center[0] + 2, center[1] - 10)
            1. Draw green stems from stem_top to left_bulb and right_bulb (color: STEM_COLOR, width: 2).
            2. Draw stem top leaf circle at stem_top (color: STEM_COLOR, radius: 3).
            3. Draw cherry bulbs at left_bulb and right_bulb (color: CHERRY_COLOR, radius: 6).
            4. Draw white specular highlights on each cherry (color: (255, 200, 200), radius: 2).
        """
        if not self.active:
            return
        if not hasattr(pygame, "draw"):
            screen.blit(self.image, self.rect)
            return
        center = self.rect.center
        left_bulb = (center[0] - 6, center[1] + 4)
        right_bulb = (center[0] + 6, center[1] + 6)
        stem_top = (center[0] + 2, center[1] - 10)
        for bulb in (left_bulb, right_bulb):
            pygame.draw.line(screen, STEM_COLOR, stem_top, bulb, 2)
        pygame.draw.circle(screen, STEM_COLOR, (stem_top[0] + 3, stem_top[1] - 2), 3)
        for bulb in (left_bulb, right_bulb):
            pygame.draw.circle(screen, CHERRY_COLOR, bulb, 6)
            pygame.draw.circle(screen, (255, 200, 200), (bulb[0] - 2, bulb[1] - 2), 2)


def run_checks():
    """Automated verification suite for Week 11 ABC concepts."""
    print("Running Week 11 ABC and Object Contract checks...")

    # 1. Verify GameObject is an abstract base class
    assert issubclass(GameObject, ABC), "GameObject must inherit from abc.ABC"
    assert hasattr(GameObject, "__abstractmethods__"), "GameObject must have abstract methods"
    assert "update" in GameObject.__abstractmethods__, "update() must be decorated with @abstractmethod"
    assert "draw" in GameObject.__abstractmethods__, "draw() must be decorated with @abstractmethod"
    print("  [PASS] GameObject defines ABC contract with update() and draw() abstract methods")

    # 2. Verify GameObject cannot be instantiated directly
    try:
        GameObject(0, 0, 0, (10, 10), (255, 255, 255))
    except TypeError as e:
        err_msg = str(e).lower()
        assert "abstract" in err_msg and ("draw" in err_msg or "update" in err_msg)
        print(f"  [PASS] Direct GameObject instantiation blocked: {e}")
    else:
        raise AssertionError("Instantiating GameObject directly should raise TypeError!")

    # 3. Verify incomplete subclass raises TypeError
    assert issubclass(IncompleteCherry, GameObject)
    try:
        IncompleteCherry(100, 100)
    except TypeError as e:
        err_msg = str(e).lower()
        assert "abstract" in err_msg and "draw" in err_msg
        print(f"  [PASS] IncompleteCherry instantiation blocked: {e}")
    else:
        raise AssertionError("IncompleteCherry missing draw() must raise TypeError!")

    # 4. Verify concrete classes instantiate and satisfy contract
    pacman = Pacman(100, 100)
    ghost = Ghost(200, 200)
    pellet = Pellet(50, 50)
    cherry = Cherry(300, 300)

    for entity in [pacman, ghost, pellet, cherry]:
        assert isinstance(entity, GameObject), f"{type(entity).__name__} must be an instance of GameObject"
        assert callable(getattr(entity, "update", None)), f"{type(entity).__name__} must implement update()"
        assert callable(getattr(entity, "draw", None)), f"{type(entity).__name__} must implement draw()"
    print("  [PASS] Concrete subclasses (Pacman, Ghost, Pellet, Cherry) instantiate and satisfy contract")

    # 5. Verify polymorphic game loop execution
    entities = [pacman, ghost, pellet, cherry]
    screen = pygame.Surface((WIDTH, HEIGHT))
    initial_y = cherry.y

    for entity in entities:
        entity.update()
        entity.draw(screen)

    assert cherry.y != initial_y, "Cherry update() should animate vertical bobbing"
    print("  [PASS] Polymorphic game loop executes cleanly across all entities")

    print("\nAll Week 11 verification checks passed successfully!")


def main():
    """Interactive Pygame arena demonstrating the ABC object contract."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SF211 Week 11: Abstract Base Classes — Pacman Arena")
    clock = pygame.time.Clock()

    bounds = pygame.Rect(40, 40, WIDTH - 80, HEIGHT - 80)
    pacman = Pacman(100, 150)
    ghost = Ghost(400, 150)
    cherry = Cherry(400, 300)

    pellets = [
        Pellet(100 + i * 50, 220) for i in range(13)
    ]

    # =============================================================================
    # TASK 4: Polymorphic Game Loop
    # =============================================================================
    # TODO: Include cherry in game_objects for polymorphic update and render
    # =============================================================================
    game_objects = [pacman, ghost, cherry] + pellets

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        for obj in game_objects:
            obj.update(bounds=bounds)

        if cherry.active and pacman.rect.colliderect(cherry.rect):
            cherry.active = False
            print("Pacman collected the Bonus Cherry! Contract fulfilled.")

        for pellet in pellets:
            if pellet.active and pacman.rect.colliderect(pellet.rect):
                pellet.active = False

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, (35, 45, 75), bounds, 2)

        for obj in game_objects:
            obj.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run automated test assertions")
    args = parser.parse_args()
    if args.check:
        run_checks()
    else:
        main()
