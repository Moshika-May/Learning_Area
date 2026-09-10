"""Week 6 Starter Code: Specialized Ghost Behaviors through Method Overriding.

STUDENT INSTRUCTIONS:
In lecture, you learned how to use Method Overriding and Dynamic Dispatch to create
distinct subclass behaviors under a shared method interface without brittle if/elif
chains.

In this lab, you will extend the Pacman Arena with three distinct Ghost AI behaviors:

  - Task 1: Understand the `GameObject` and `Ghost` base classes.
  - Task 2: Implement `PatrolGhost` (Pinky) overriding update() with corridor bouncing
            and super().update() synchronization.
  - Task 3: Implement `ChaseGhost` (Blinky) overriding update() with direct target pursuit
            and distance calculation.
  - Task 4: Implement `StationaryGhost` (Clyde/Guard) overriding update() with timer-based
            alert/attack cooldowns.
  - Task 5: Implement `update_ghosts()` to dispatch polymorphic updates across mixed
            ghost types with ZERO isinstance() type checks.

Verify your implementation with automated tests:
    python3 code/week06/starter.py --check
Or run the interactive demonstration:
    python3 code/week06/starter.py
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
BLINKY_COLOR = (235, 60, 60)      # Red - ChaseGhost
PINKY_COLOR = (255, 160, 210)     # Pink - PatrolGhost
CLYDE_COLOR = (255, 175, 65)      # Orange - Stationary/Guard Ghost
PELLET_COLOR = (255, 183, 77)


# =============================================================================
# BASE CLASSES: GameObject and Ghost
# =============================================================================

class GameObject:
    """Base class for shared position, bounding box, active state, and drawing."""

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

    def update(self, target=None, bounds=None):
        """Default base update: maintain position synchronization."""
        self.sync_position()

    def draw(self, screen):
        """Draw the entity on screen if active."""
        if self.active:
            screen.blit(self.image, self.rect)


class Pacman(GameObject):
    """Player-controlled Pacman entity."""

    def __init__(self, x, y):
        super().__init__(x=x, y=y, speed=5.0, size=(36, 36), color=PACMAN_COLOR)
        self.facing_angle = 0.0
        self.mouth_phase = 0
        self.score = 0

    def update(self, target=None, bounds=None, controls=None):
        if controls is None:
            if hasattr(pygame, "key") and hasattr(pygame.key, "get_pressed"):
                controls = pygame.key.get_pressed()
            else:
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


class Ghost(GameObject):
    """Base Ghost enemy class providing shared ghost rendering and state."""

    def __init__(self, x, y, color=BLINKY_COLOR, speed=2.5):
        super().__init__(x=x, y=y, speed=speed, size=(36, 36), color=color)
        self.eye_direction = (1, 0)

    def update(self, target=None, bounds=None):
        """Parent update: synchronize Pygame rect with internal coordinates."""
        super().update(target, bounds)

    def draw(self, screen):
        """Draw the ghost body with rounded head, wavy skirt, and directional eyes."""
        if not self.active:
            return
        if not hasattr(pygame, "draw"):
            super().draw(screen)
            return

        body = self.rect
        radius = body.width // 2
        center_x = body.centerx
        head_center = (center_x, body.y + radius)

        pygame.draw.circle(screen, self.color, head_center, radius)
        pygame.draw.rect(
            screen,
            self.color,
            (body.x, body.y + radius, body.width, body.height - radius),
        )

        wave_radius = body.width // 6
        wave_y = body.bottom - wave_radius
        for index in range(3):
            wave_x = body.x + wave_radius + index * wave_radius * 2
            pygame.draw.circle(screen, BACKGROUND_COLOR, (wave_x, wave_y), wave_radius)

        eye_y = body.y + body.height // 3
        eye_offset = 7
        pupil_dx = 2 if self.eye_direction[0] >= 0 else -2
        pupil_dy = 2 if self.eye_direction[1] > 0 else (-2 if self.eye_direction[1] < 0 else 0)

        for eye_x in (center_x - eye_offset, center_x + eye_offset):
            pygame.draw.circle(screen, "white", (eye_x, eye_y), 5)
            pygame.draw.circle(screen, (30, 60, 160), (eye_x + pupil_dx, eye_y + pupil_dy), 2)


# =============================================================================
# TASK 2: PatrolGhost Subclass
# =============================================================================

class PatrolGhost(Ghost):
    """Specialized Ghost (Pinky) that patrols back and forth between corridor bounds."""

    def __init__(self, x, y, patrol_left, patrol_right, color=PINKY_COLOR, speed=3.0):
        """Initialize PatrolGhost with corridor boundaries."""
        super().__init__(x=x, y=y, color=color, speed=speed)
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

    def update(self, target=None, bounds=None):
        """Override: move horizontally and reverse direction at patrol bounds."""
        self.x += self.speed

        if self.x <= self.patrol_left:
            self.x = self.patrol_left
            self.speed = abs(self.speed)
        elif self.x + self.rect.width >= self.patrol_right:
            self.x = self.patrol_right - self.rect.width
            self.speed = -abs(self.speed)

        self.eye_direction = (1 if self.speed >= 0 else -1, 0)

        super().update(target, bounds)


# =============================================================================
# TASK 3: ChaseGhost Subclass
# =============================================================================

class ChaseGhost(Ghost):
    """Specialized Ghost (Blinky) that actively tracks and pursues Pac-Man."""

    def __init__(self, x, y, color=BLINKY_COLOR, speed=2.2):
        """Initialize ChaseGhost."""
        super().__init__(x=x, y=y, color=color, speed=speed)

    def update(self, target=None, bounds=None):
        """Override: calculate vector to Pacman and close distance in 2D space."""
        if target is not None:
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance > 0:
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)
                self.eye_direction = (
                    1 if dx >= 0 else -1,
                    1 if dy > 0 else (-1 if dy < 0 else 0),
                )

        super().update(target, bounds)


# =============================================================================
# TASK 4: StationaryGhost Subclass
# =============================================================================

class StationaryGhost(Ghost):
    """Specialized Ghost (Clyde/Guard) that stays in place and pulses periodic alerts."""

    def __init__(self, x, y, color=CLYDE_COLOR, attack_cooldown=60):
        """Initialize StationaryGhost with cooldown timer."""
        super().__init__(x=x, y=y, color=color, speed=0.0)
        self.attack_timer = 0
        self.attack_cooldown = attack_cooldown
        self.attacks = 0

    def update(self, target=None, bounds=None):
        """Override: no movement; increment timer and trigger periodic alert/attack."""
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            self.attacks += 1

        if target is not None:
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            self.eye_direction = (
                1 if dx >= 0 else -1,
                1 if dy > 0 else (-1 if dy < 0 else 0),
            )

        super().update(target, bounds)


# =============================================================================
# TASK 5: Polymorphic Dispatch Functions
# =============================================================================

class Pellet(GameObject):
    """Stationary score pellet collected by Pacman."""

    def __init__(self, x, y, points=10):
        super().__init__(x=x, y=y, speed=0.0, size=(14, 14), color=PELLET_COLOR)
        self.points = points

    def collect(self):
        self.active = False
        return self.points

    def draw(self, screen):
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


def update_ghosts(ghosts, target, bounds=None):
    """Polymorphic update loop: invokes specialized update() without type checks."""
    for ghost in ghosts:
        ghost.update(target, bounds)


def draw_objects(screen, objects):
    """Polymorphic render loop: draws entities through their public draw() method."""
    for entity in objects:
        entity.draw(screen)


# =============================================================================
# VERIFICATION AND DEMONSTRATION
# =============================================================================

def run_checks():
    """Run deterministic unit checks verifying ghost method overriding."""
    # 1. Inheritance relationships
    assert issubclass(Ghost, GameObject), "Ghost must inherit from GameObject"
    assert issubclass(PatrolGhost, Ghost), "PatrolGhost must inherit from Ghost"
    assert issubclass(ChaseGhost, Ghost), "ChaseGhost must inherit from Ghost"
    assert issubclass(StationaryGhost, Ghost), "StationaryGhost must inherit from Ghost"
    assert issubclass(Pacman, GameObject), "Pacman must inherit from GameObject"

    # 2. Method overriding verification
    assert PatrolGhost.update is not Ghost.update, "PatrolGhost must override update()"
    assert ChaseGhost.update is not Ghost.update, "ChaseGhost must override update()"
    assert StationaryGhost.update is not Ghost.update, "StationaryGhost must override update()"
    assert Pacman.update is not GameObject.update, "Pacman must override update()"

    # 3. Instance setup
    pacman = Pacman(400, 300)
    patrol = PatrolGhost(100, 150, patrol_left=80, patrol_right=250)
    chase = ChaseGhost(700, 300)
    guard = StationaryGhost(400, 500, attack_cooldown=60)
    ghosts = [patrol, chase, guard]

    # 4. Behavioral Specialization: Chase distance closes
    initial_dist = math.hypot(
        pacman.rect.centerx - chase.rect.centerx,
        pacman.rect.centery - chase.rect.centery,
    )
    for _ in range(60):
        update_ghosts(ghosts, pacman)

    new_dist = math.hypot(
        pacman.rect.centerx - chase.rect.centerx,
        pacman.rect.centery - chase.rect.centery,
    )
    assert new_dist < initial_dist, "ChaseGhost should move closer to Pacman"

    # 5. Behavioral Specialization: Patrol bounds respected
    assert patrol.rect.left >= 80 and patrol.rect.right <= 250, "PatrolGhost must remain in bounds"

    # 6. Behavioral Specialization: Stationary does not move, counts attack ticks
    assert guard.rect.topleft == (400, 500), "StationaryGhost should remain in fixed place"
    assert guard.attacks == 1, "StationaryGhost should have triggered 1 attack cycle after 60 ticks"

    # 7. Polymorphic rendering test
    surface = pygame.Surface((WIDTH, HEIGHT))
    draw_objects(surface, [pacman, patrol, chase, guard])

    print("✓ All Week 6 Ghost behavioral specialization checks passed successfully!")


def main():
    try:
        import pygame
    except ImportError:
        print("Error: pygame is required to run the interactive demo.")
        print("Run with --check to execute verification tests without GUI.")
        sys.exit(1)

    pygame.init()
    pygame.display.set_caption("Week 6 Exercise: Specialized Ghost Behaviors")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bounds = screen.get_rect()
    clock = pygame.time.Clock()

    pacman = Pacman(400, 450)
    blinky = ChaseGhost(700, 100, color=BLINKY_COLOR, speed=2.2)
    pinky = PatrolGhost(100, 200, patrol_left=80, patrol_right=450, color=PINKY_COLOR, speed=3.0)
    clyde = StationaryGhost(600, 400, color=CLYDE_COLOR, attack_cooldown=90)
    ghosts = [blinky, pinky, clyde]

    pellets = [
        Pellet(200, 300, points=10),
        Pellet(350, 200, points=10),
        Pellet(500, 300, points=10),
        Pellet(600, 200, points=10),
        Pellet(400, 150, points=25),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pacman.update(bounds=bounds)
        update_ghosts(ghosts, target=pacman, bounds=bounds)

        for pellet in pellets:
            if pellet.active and pacman.rect.colliderect(pellet.rect):
                pacman.score += pellet.collect()

        screen.fill(BACKGROUND_COLOR)
        draw_objects(screen, pellets)
        draw_objects(screen, ghosts)
        pacman.draw(screen)

        dist_to_blinky = int(math.hypot(
            pacman.rect.centerx - blinky.rect.centerx,
            pacman.rect.centery - blinky.rect.centery,
        ))
        pygame.display.set_caption(
            f"Week 6 Pacman & Ghosts | Score: {pacman.score} | "
            f"Blinky (Chase) Dist: {dist_to_blinky}px | Clyde (Guard) Pulses: {clyde.attacks}"
        )
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="run exercise verification checks without opening a window",
    )
    args = parser.parse_args()
    if args.check:
        run_checks()
    else:
        main()
