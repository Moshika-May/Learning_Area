""""Week 5 Starter Code: Pacman GameObject Hierarchy.

STUDENT INSTRUCTIONS:
In lecture, you learned how to use Object-Oriented Inheritance to eliminate code
duplication and express genuine "is-a" relationships between game entities.

In this lab, you will build a clean, polymorphic class hierarchy for a Pacman Arena:

  - Task 1: Implement the `GameObject` base class for shared position, image, rect,
            active state, position syncing, and default rendering.
  - Task 2: Implement the `Pacman` subclass inheriting from `GameObject` with
            super() initialization, keyboard-driven update(), and mouth animation.
  - Task 3: Implement the `Ghost` subclass inheriting from `GameObject` with
            super() initialization, corridor patrol bounce update(), and animated eyes.
  - Task 4: Implement the `Pellet` subclass inheriting from `GameObject` with
            super() initialization, collect() method, and unchanged update() inheritance.
  - Task 5: Implement `update_objects()` and `draw_objects()` polymorphic dispatch loops
            with ZERO isinstance() type checks.

Verify your implementation with automated tests:
    python3 main.py --check
Or run the interactive demonstration:
    python3 main.py
"""

import argparse
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
            def topleft(self):
                return (self.x, self.y)

            @topleft.setter
            def topleft(self, value):
                self.x, self.y = value

            @property
            def right(self):
                return self.x + self.width

            @property
            def bottom(self):
                return self.y + self.height

            @property
            def bottomright(self):
                return (self.right, self.bottom)

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


# Window and Simulation Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (20, 24, 40)
PACMAN_COLOR = (255, 238, 0)
GHOST_COLOR = (230, 40, 40)
PELLET_COLOR = (255, 183, 77)


def _is_pressed(controls, key):
    """Read a key state safely from a pygame key sequence or a plain dict."""
    try:
        return bool(controls[key])
    except (KeyError, IndexError, TypeError):
        return False


# =============================================================================
# TASK 1: Base Class GameObject
# =============================================================================

class GameObject:
    """Base class for state and behavior shared by all visible maze entities."""

    def __init__(self, x, y, speed, size, color):
        """Initialize the shared state for any visible game object."""
        self.x = float(x)
        self.y = float(y)
        self.speed = float(speed)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(round(x), round(y)))
        self.active = True

    def update(self, bounds=None, controls=None):
        """Default behavior: stationary entity (subclasses override for movement)."""
        pass

    def sync_position(self):
        """Keep Pygame bounding box aligned with internal float coordinates."""
        self.rect.topleft = (round(self.x), round(self.y))

    def draw(self, screen):
        """Draw the entity on screen if active."""
        if self.active:
            screen.blit(self.image, self.rect)


# =============================================================================
# TASK 2: Subclass Pacman
# =============================================================================

class Pacman(GameObject):
    """Player-controlled Pacman entity that overrides update() with keyboard input."""

    def __init__(self, x, y):
        """Initialize Pacman by calling the parent constructor and setting player state."""
        super().__init__(x=x, y=y, speed=5.0, size=(36, 36), color=PACMAN_COLOR)
        self.lives = 3
        self.score = 0
        self.facing_angle = 0.0
        self.mouth_phase = 0

    def update(self, bounds=None, controls=None):
        """Handle keyboard controls, update direction/animation, move, and clamp position."""
        if controls is None:
            return

        dx = 0
        dy = 0
        if _is_pressed(controls, pygame.K_RIGHT) or _is_pressed(controls, pygame.K_d):
            dx += 1
        if _is_pressed(controls, pygame.K_LEFT) or _is_pressed(controls, pygame.K_a):
            dx -= 1
        if _is_pressed(controls, pygame.K_DOWN) or _is_pressed(controls, pygame.K_s):
            dy += 1
        if _is_pressed(controls, pygame.K_UP) or _is_pressed(controls, pygame.K_w):
            dy -= 1

        if dx != 0 or dy != 0:
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
        """Draw Pacman as an animated, direction-facing chomping circle."""
        if not self.active:
            return

        if not hasattr(pygame, "draw"):
            super().draw(screen)
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


# =============================================================================
# TASK 3: Subclass Ghost
# =============================================================================

class Ghost(GameObject):
    """Autonomous Ghost entity that patrols back-and-forth between corridors."""

    def __init__(self, x, y, patrol_left, patrol_right):
        """Initialize Ghost with base state and corridor patrol bounds."""
        super().__init__(x=x, y=y, speed=3.0, size=(36, 36), color=GHOST_COLOR)
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

    def update(self, bounds=None, controls=None):
        """Patrol horizontally and bounce between patrol_left and patrol_right."""
        self.x += self.speed

        if self.x <= self.patrol_left:
            self.x = self.patrol_left
            self.speed = abs(self.speed)
        elif self.x + self.rect.width >= self.patrol_right:
            self.x = self.patrol_right - self.rect.width
            self.speed = -abs(self.speed)

        self.sync_position()

    def draw(self, screen):
        """Draw the ghost as a rounded body with eyes facing patrol direction."""
        if not self.active:
            return

        if not hasattr(pygame, "draw"):
            super().draw(screen)
            return

        body = self.rect
        radius = body.width // 2
        center_x = body.centerx
        head_center = (center_x, body.y + radius)

        pygame.draw.circle(screen, GHOST_COLOR, head_center, radius)
        pygame.draw.rect(
            screen,
            GHOST_COLOR,
            (body.x, body.y + radius, body.width, body.height - radius),
        )

        wave_radius = body.width // 6
        wave_y = body.bottom - wave_radius
        for index in range(3):
            wave_x = body.x + wave_radius + index * wave_radius * 2
            pygame.draw.circle(
                screen,
                BACKGROUND_COLOR,
                (wave_x, wave_y),
                wave_radius,
            )

        eye_y = body.y + body.height // 3
        eye_offset = 7
        pupil_offset = 2 if self.speed >= 0 else -2
        for eye_x in (center_x - eye_offset, center_x + eye_offset):
            pygame.draw.circle(screen, "white", (eye_x, eye_y), 5)
            pygame.draw.circle(
                screen,
                (30, 60, 160),
                (eye_x + pupil_offset, eye_y),
                2,
            )


# =============================================================================
# TASK 4: Subclass Pellet
# =============================================================================

class Pellet(GameObject):
    """Stationary score pellet collected by Pacman (inherits update() unchanged)."""

    def __init__(self, x, y, points=10):
        """Initialize Pellet with stationary speed and point value.

        Note: DO NOT override `update()`. Pellet inherits `GameObject.update()` unchanged!
        """
        super().__init__(x=x, y=y, speed=0.0, size=(14, 14), color=PELLET_COLOR)
        self.points = points

    def collect(self):
        """Deactivate the pellet and return its score value."""
        self.active = False
        return self.points

    def draw(self, screen):
        """Draw a pellet as a small glowing dot."""
        if not self.active:
            return

        if not hasattr(pygame, "draw"):
            super().draw(screen)
            return

        center = self.rect.center
        outer_radius = self.rect.width // 2
        inner_radius = max(2, outer_radius - 3)
        pygame.draw.circle(screen, (255, 224, 130), center, outer_radius)
        pygame.draw.circle(screen, PELLET_COLOR, center, inner_radius)


# =============================================================================
# TASK 5: Polymorphic Dispatch Functions
# =============================================================================

def update_objects(objects, bounds=None, controls=None):
    """Update mixed subclasses through dynamic dispatch without type checking."""
    for entity in objects:
        entity.update(bounds, controls)


def draw_objects(screen, objects):
    """Draw all entities through their inherited public draw() method."""
    for entity in objects:
        entity.draw(screen)


# =============================================================================
# AUTOMATED VERIFICATION SUITE
# =============================================================================

def run_checks():
    """Run deterministic tests verifying the Pacman inheritance hierarchy."""
    print("Running Week 5 automated verification suite...")

    # 1. Inheritance relationships
    assert issubclass(Pacman, GameObject), "Pacman must inherit from GameObject"
    assert issubclass(Ghost, GameObject), "Ghost must inherit from GameObject"
    assert issubclass(Pellet, GameObject), "Pellet must inherit from GameObject"
    print("  [PASS] Subclass inheritance hierarchy")

    # 2. Method overriding verification
    assert Pacman.update is not GameObject.update, "Pacman must override update()"
    assert Ghost.update is not GameObject.update, "Ghost must override update()"
    assert Pellet.update is GameObject.update, "Pellet should inherit GameObject.update() unchanged"
    assert Pellet.draw is not GameObject.draw, "Pellet should override draw() for a round pellet"
    print("  [PASS] Method overriding & inheritance contract")

    # 3. Instance creation and state initialization
    bounds = pygame.Rect(0, 0, WIDTH, HEIGHT)
    pacman = Pacman(100, 100)
    ghost = Ghost(200, 200, patrol_left=180, patrol_right=300)
    pellet = Pellet(400, 300, points=25)

    assert pacman.rect.topleft == (100, 100), "Pacman rect should match initial position"
    assert ghost.rect.topleft == (200, 200), "Ghost rect should match initial position"
    assert pellet.collect() == 25, "Pellet.collect() should return point value"
    assert not pellet.active, "Pellet should be inactive after collection"
    print("  [PASS] Instance creation & super() state initialization")

    # 4. Polymorphic update dispatch
    pellet.active = True
    before_pellet = pellet.rect.topleft
    controls = {pygame.K_RIGHT: True, pygame.K_DOWN: True}
    update_objects([pacman, ghost, pellet], bounds, controls)
    assert pacman.rect.topleft == (105, 105), "Pacman should move with speed 5.0"
    assert ghost.rect.x == 203, "Ghost should move with speed 3.0"
    assert pellet.rect.topleft == before_pellet, "Pellet should remain stationary during update"
    print("  [PASS] Polymorphic update dispatch loop")

    # 5. Boundary clamping
    pacman.x = WIDTH
    pacman.y = HEIGHT
    pacman.update(bounds, {})
    assert pacman.rect.bottomright == bounds.bottomright, "Pacman should be clamped within bounds"
    print("  [PASS] Pacman arena boundary clamping")

    # 6. Ghost patrol bounce
    ghost.x = ghost.patrol_right
    ghost.update(bounds)
    assert ghost.speed < 0, "Ghost speed should reverse upon reaching patrol_right"
    assert ghost.rect.right == ghost.patrol_right, "Ghost position should align with patrol_right"
    print("  [PASS] Ghost patrol bounce mechanics")

    # 7. Polymorphic rendering
    surface = pygame.Surface((WIDTH, HEIGHT))
    draw_objects(surface, [pacman, ghost, pellet])
    print("  [PASS] Polymorphic rendering loop")

    print("\nSUCCESS: All Week 5 Pacman GameObject hierarchy checks passed successfully!")


# =============================================================================
# INTERACTIVE DEMONSTRATION ARENA
# =============================================================================

def main():
    try:
        import pygame
    except ImportError:
        print("Error: pygame is required to run the interactive demo.")
        print("Run with --check to execute verification tests without GUI.")
        sys.exit(1)

    pygame.init()
    pygame.display.set_caption("Week 5 Exercise: Pacman GameObject Hierarchy")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bounds = screen.get_rect()
    clock = pygame.time.Clock()

    pacman = Pacman(100, 450)
    ghost = Ghost(250, 280, patrol_left=180, patrol_right=650)
    pellet = Pellet(600, 470, points=10)
    objects = [pacman, ghost, pellet]
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        controls = pygame.key.get_pressed()
        update_objects(objects, bounds, controls)

        if pacman.rect.colliderect(pellet.rect) and pellet.active:
            score += pellet.collect()
            pellet.x = 100 + (score * 37) % 650
            pellet.y = 140 + (score * 23) % 400
            pellet.active = True
            pellet.sync_position()

        screen.fill(BACKGROUND_COLOR)
        draw_objects(screen, objects)
        pygame.display.set_caption(
            f"Week 5 Exercise (Pacman Arena) — Score: {score}"
            " | Arrow Keys/WASD: Move Pacman | Red: Ghost | Gold: Pellet"
        )
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="run the exercise verification checks without opening a window",
    )
    arguments = parser.parse_args()

    if arguments.check:
        run_checks()
    else:
        main()