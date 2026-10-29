"""Week 12 Starter Code: Collision Detection, Events, and Observer-Style Communication.

STUDENT INSTRUCTIONS:
In lecture, you learned how tightly coupled code creates brittle game loops:
when collision detection functions directly call ScoreManager.add_points() or
SoundManager.play(), adding a new subsystem requires editing every collision function!

In this lab, you will establish a clean, decoupled event-driven architecture
in the Pacman Arena:

  - Task 1: Implement `distance_collision(entity_a, entity_b, threshold)` using
            Euclidean distance to eliminate the AABB corner overlap bug.
  - Task 2: Define custom Pygame event constants (`PELLET_EATEN`, `CHERRY_EATEN`,
            `GHOST_HIT`, `PACMAN_DEFEAT`) and implement `check_collisions()`
            to post factual events into Pygame's event queue.
            (STRICT BOUNDARY: Do NOT call score or sound managers here!)
  - Task 3: Establish the `EventObserver(ABC)` abstract interface and implement
            the concrete `ScoreManager(EventObserver)` observer.
  - Task 4: Implement the `SoundManager(EventObserver)` observer to trigger procedural
            audio feedback without crashing when audio hardware is unavailable.
  - Task 5: Implement `AchievementManager(EventObserver)` to prove the Open/Closed Principle:
            new features can be added with ZERO changes to collision detection code.
  - Task 6: Wire the observers and safe list-comprehension deferral batch cleanup
            into the interactive game loop in `main()`.

Verify your implementation with automated tests:
    python3 code/week12/starter.py --check
Or run the interactive demonstration:
    python3 code/week12/starter.py
"""

from __future__ import annotations

import argparse
from abc import ABC, abstractmethod
import array
import math
import os
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
        K_ESCAPE = 9
        QUIT = 12
        KEYDOWN = 2

        USEREVENT = 24

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
                    self.right <= other.left
                    or self.left >= other.right
                    or self.bottom <= other.top
                    or self.top >= other.bottom
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

        class _EventModule:
            def __init__(self):
                self._queue = []

            def Event(self, type_, dict_data=None, **kwargs):
                class EventObj:
                    def __init__(self, t, d):
                        self.type = t
                        self.dict = dict(d or {})
                        for k, v in self.dict.items():
                            setattr(self, k, v)

                    def __repr__(self):
                        return f"<Event({self.type}, {self.dict})>"

                payload = dict(dict_data or {})
                payload.update(kwargs)
                return EventObj(type_, payload)

            def post(self, event):
                self._queue.append(event)

            def get(self):
                events = list(self._queue)
                self._queue.clear()
                return events

            def clear(self):
                self._queue.clear()

        def __init__(self):
            self.event = self._EventModule()

    pygame = _MockPygame()


# Window & Arena Configuration
WIDTH = 800
HEIGHT = 600
FPS = 60

# Palette
BACKGROUND_COLOR = (20, 24, 40)
ARENA_BORDER_COLOR = (35, 45, 75)
PACMAN_COLOR = (255, 238, 0)
BLINKY_COLOR = (235, 60, 60)
PELLET_COLOR = (255, 183, 77)
CHERRY_COLOR = (220, 20, 60)
STEM_COLOR = (46, 139, 87)
HUD_BG_COLOR = (14, 18, 30)
TEXT_COLOR = (240, 240, 250)
ACCENT_COLOR = (22, 140, 140)


# =============================================================================
# TASK 2 (Part A): Custom Event Constants (Pygame USEREVENT Offsets)
# =============================================================================
# Define unique event IDs for game occurrences.
# In Pygame, custom events start at pygame.USEREVENT and increment by 1.
#
# TODO: Define the four custom event constants:
#   - PELLET_EATEN  = pygame.USEREVENT + 1
#   - CHERRY_EATEN  = pygame.USEREVENT + 2
#   - GHOST_HIT     = pygame.USEREVENT + 3
#   - PACMAN_DEFEAT = pygame.USEREVENT + 4
# =============================================================================
PELLET_EATEN = pygame.USEREVENT + 1
CHERRY_EATEN = pygame.USEREVENT + 2
GHOST_HIT = pygame.USEREVENT + 3
PACMAN_DEFEAT = pygame.USEREVENT + 4


# =============================================================================
# TASK 1: Euclidean Distance Collision Detection
# =============================================================================
def distance_collision(entity_a, entity_b, threshold: float) -> bool:
    """Return True if Euclidean distance between entity centers is strictly less than threshold.

    Unlike Rect.colliderect() (AABB), this radial check prevents false-positive
    'phantom collisions' at empty diagonal corners of circular sprites.

    Formula:
        dx = entity_a.rect.centerx - entity_b.rect.centerx
        dy = entity_a.rect.centery - entity_b.rect.centery
        distance = math.hypot(dx, dy)
        return distance < threshold

    TODO: Implement the Euclidean distance calculation between entity_a and entity_b.
    """
    return math.hypot(
        entity_a.rect.centerx - entity_b.rect.centerx,
        entity_a.rect.centery - entity_b.rect.centery,
    ) < threshold


# =============================================================================
# TASK 2 (Part B): Decoupled Collision Detection Function
# =============================================================================
def check_collisions(pacman, pellets, cherry=None, ghost=None) -> None:
    """Detect collisions and post factual events to the Pygame event queue.

    STRICT ARCHITECTURAL BOUNDARY:
    This function MUST NOT import, reference, or call ScoreManager,
    SoundManager, or HUD code directly. It emits FACTS as events.

    Rules:
      1. Pellets: Iterate safely using a slice copy (`pellets[:]`).
         If `pellet.active` and `distance_collision(pacman, pellet, threshold=23)`:
           - Deactivate pellet: `pellet.active = False`
           - Post `PELLET_EATEN` event with payload:
             `{"points": getattr(pellet, "points", 10), "pos": pellet.rect.center}`
      2. Cherry:
         If `cherry is not None and cherry.active` and `distance_collision(pacman, cherry, threshold=32)`:
           - Deactivate cherry: `cherry.active = False`
           - Post `CHERRY_EATEN` event with payload:
             `{"points": getattr(cherry, "points", 50), "pos": cherry.rect.center}`
      3. Ghost:
         If `ghost is not None and ghost.active` and `distance_collision(pacman, ghost, threshold=36)`:
           - Post `GHOST_HIT` event with payload:
             `{"damage": 1, "pos": pacman.rect.center}`

    TODO: Implement collision checks and event posting.
    """
    for pellet in pellets[:]:
        if pellet.active and distance_collision(pacman, pellet, threshold=23):
            pellet.active = False
            pygame.event.post(pygame.event.Event(
                PELLET_EATEN,
                {"points": getattr(pellet, "points", 10), "pos": pellet.rect.center},
            ))

    if cherry is not None and cherry.active and distance_collision(pacman, cherry, threshold=32):
        cherry.active = False
        pygame.event.post(pygame.event.Event(
            CHERRY_EATEN,
            {"points": getattr(cherry, "points", 50), "pos": cherry.rect.center},
        ))

    if ghost is not None and ghost.active and distance_collision(pacman, ghost, threshold=36):
        pygame.event.post(pygame.event.Event(
            GHOST_HIT, {"damage": 1, "pos": pacman.rect.center}
        ))


# =============================================================================
# TASK 3 (Part A): Observer Pattern Abstract Interface
# =============================================================================
class EventObserver(ABC):
    """Abstract observer interface for decoupled event handling.

    Enforces the single-method contract `handle_event(event)` so any subsystem
    can listen to game events without tight coupling.

    TODO: Define abstract method `handle_event(self, event) -> None`.
    """

    @abstractmethod
    def handle_event(self, event) -> None:
        """React to a game event."""


# =============================================================================
# TASK 3 (Part B): ScoreManager Observer
# =============================================================================
class ScoreManager(EventObserver):  # TODO Task 3 (Part B): Inherit from EventObserver
    """Observer that tracks points and collectible statistics.

    Attributes:
        score: int (total score, starts at 0)
        pellets_eaten: int (starts at 0)
        fruits_eaten: int (starts at 0)

    Event Handling:
        - On PELLET_EATEN: increment score by event.points (or 10) and pellets_eaten by 1
        - On CHERRY_EATEN: increment score by event.points (or 50) and fruits_eaten by 1

    TODO Task 3 (Part B): Inherit from EventObserver and implement `handle_event(self, event)`.
    """

    def __init__(self):
        self.score = 0
        self.pellets_eaten = 0
        self.fruits_eaten = 0

    def handle_event(self, event) -> None:
        if event.type == PELLET_EATEN:
            self.score += getattr(event, "points", 10)
            self.pellets_eaten += 1
        elif event.type == CHERRY_EATEN:
            self.score += getattr(event, "points", 50)
            self.fruits_eaten += 1


# =============================================================================
# TASK 4: SoundManager Observer
# =============================================================================
class SoundManager(EventObserver):  # TODO Task 4: Inherit from EventObserver
    """Observer that manages sound effect feedback with safe fail-soft audio handling.

    Attributes:
        enabled: bool
        sounds_played: list[str] (tracks names of played sounds for testing/HUD)

    Event Handling:
        - PELLET_EATEN -> self.play("chomp")
        - CHERRY_EATEN -> self.play("fruit")
        - GHOST_HIT    -> self.play("hazard")

    TODO Task 4: Inherit from EventObserver and implement `handle_event(self, event)`.
    (Note: `_init_audio()` and `play()` are provided below)
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.sounds_played: list[str] = []
        self._sounds = {}
        self._init_audio()

    def _init_audio(self):
        """Synthesize procedural audio tones so sound works without external WAV files."""
        if not self.enabled:
            return
        try:
            if not hasattr(pygame, "mixer") or not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

            def make_tone(freq, duration, volume=0.3):
                sample_rate = 22050
                n_samples = int(sample_rate * duration)
                amplitude = int(32767 * volume)
                raw = [
                    int(amplitude * math.sin(2.0 * math.pi * freq * i / sample_rate))
                    for i in range(n_samples)
                ]
                buf = array.array("h", raw)
                return pygame.mixer.Sound(buffer=buf)

            self._sounds["chomp"] = make_tone(587.33, 0.05, 0.25)
            self._sounds["fruit"] = make_tone(880.0, 0.12, 0.3)
            self._sounds["hazard"] = make_tone(220.0, 0.20, 0.35)
        except Exception:
            # Sound hardware unavailable (e.g. headless CI / mock)
            self._sounds = {}

    def handle_event(self, event) -> None:
        if event.type == PELLET_EATEN:
            self.play("chomp")
        elif event.type == CHERRY_EATEN:
            self.play("fruit")
        elif event.type == GHOST_HIT:
            self.play("hazard")

    def play(self, sound_name: str) -> None:
        self.sounds_played.append(sound_name)
        sound = self._sounds.get(sound_name)
        if sound is not None:
            try:
                sound.play()
            except Exception:
                pass


# =============================================================================
# HUDManager Observer (Provided)
# =============================================================================
class HUDManager(EventObserver):
    """Observer responsible for updating and drawing the on-screen Heads-Up Display."""

    def __init__(self, initial_lives: int = 3):
        self.score = 0
        self.lives = initial_lives
        self.pellets_eaten = 0
        self.message = "SF211 Pacman Arena — Week 12 Decoupled Events"
        self._invincible_cooldown = 0
        self.font = None
        self.font_small = None
        self._init_font()

    def _init_font(self):
        try:
            if hasattr(pygame, "font") and pygame.font.get_init():
                self.font = pygame.font.SysFont("Helvetica,Arial,DejaVu Sans", 20, bold=True)
                self.font_small = pygame.font.SysFont("Helvetica,Arial,DejaVu Sans", 14)
        except Exception:
            self.font = None
            self.font_small = None

    def handle_event(self, event) -> None:
        if event.type == PELLET_EATEN:
            self.score += getattr(event, "points", 10)
            self.pellets_eaten += 1
            self.message = f"Pellet eaten! +{getattr(event, 'points', 10)} pts (Total: {self.score})"
        elif event.type == CHERRY_EATEN:
            self.score += getattr(event, "points", 50)
            self.message = f"BONUS CHERRY! +{getattr(event, 'points', 50)} pts! Great job!"
        elif event.type == GHOST_HIT:
            if self._invincible_cooldown == 0:
                self.lives -= getattr(event, "damage", 1)
                self._invincible_cooldown = 60
                if self.lives <= 0:
                    self.message = "PACMAN DEFEATED! Game Over."
                    pygame.event.post(pygame.event.Event(PACMAN_DEFEAT, {"final_score": self.score}))
                else:
                    self.message = f"GHOST HIT! Lost 1 life! Remaining: {self.lives}"

    def update(self):
        if self._invincible_cooldown > 0:
            self._invincible_cooldown -= 1

    def draw(self, screen):
        if not hasattr(pygame, "draw"):
            return

        pygame.draw.rect(screen, HUD_BG_COLOR, (0, 0, WIDTH, 54))
        pygame.draw.line(screen, ACCENT_COLOR, (0, 54), (WIDTH, 54), 2)

        if self.font is not None and self.font_small is not None:
            score_surf = self.font.render(f"SCORE: {self.score}", True, PACMAN_COLOR)
            screen.blit(score_surf, (20, 14))

            msg_surf = self.font_small.render(self.message, True, TEXT_COLOR)
            screen.blit(msg_surf, (220, 18))

            lives_label = self.font.render("LIVES:", True, TEXT_COLOR)
            screen.blit(lives_label, (WIDTH - 180, 14))

        for i in range(self.lives):
            icon_x = WIDTH - 95 + i * 26
            icon_y = 25
            pygame.draw.circle(screen, PACMAN_COLOR, (icon_x, icon_y), 8)
            pygame.draw.polygon(
                screen,
                HUD_BG_COLOR,
                [(icon_x, icon_y), (icon_x + 9, icon_y - 4), (icon_x + 9, icon_y + 4)],
            )


# =============================================================================
# TASK 5: AchievementManager (Open/Closed Principle)
# =============================================================================
class AchievementManager(EventObserver):  # TODO Task 5: Inherit from EventObserver
    """Demonstrates Open/Closed Principle: added with ZERO modifications to collision code.

    Attributes:
        unlocked: set[str] (names of unlocked achievements)

    Rules:
        - PELLET_EATEN unlocks "FIRST_BITE"
        - CHERRY_EATEN unlocks "SWEET_TOOTH"
        - GHOST_HIT    unlocks "SURVIVOR"

    TODO Task 5: Inherit from EventObserver and implement `handle_event(self, event)`.
    """

    def __init__(self):
        self.unlocked: set[str] = set()

    def handle_event(self, event) -> None:
        if event.type == PELLET_EATEN:
            self.unlocked.add("FIRST_BITE")
        elif event.type == CHERRY_EATEN:
            self.unlocked.add("SWEET_TOOTH")
        elif event.type == GHOST_HIT:
            self.unlocked.add("SURVIVOR")


# =============================================================================
# Entities from Week 11 GameObject Contract (Provided)
# =============================================================================
class GameObject(ABC):
    """Abstract Base Class defining the mandatory contract for all game entities."""

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
        self.rect.topleft = (round(self.x), round(self.y))

    @abstractmethod
    def update(self, bounds=None):
        """Advance entity state by one frame."""

    @abstractmethod
    def draw(self, screen):
        """Render entity to the screen."""


class Pacman(GameObject):
    """Player-controlled Pacman entity."""

    def __init__(self, x, y):
        super().__init__(x=x, y=y, speed=4.5, size=(36, 36), color=PACMAN_COLOR)
        self.radius = 18
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
                return bool(controls.get(key, False))
            if hasattr(controls, "__getitem__"):
                try:
                    return bool(controls[key])
                except (IndexError, KeyError):
                    return False
            return False

        dx = 0.0
        dy = 0.0

        if is_pressed(pygame.K_RIGHT) or is_pressed(pygame.K_d):
            dx += self.speed
            self.facing_angle = 0.0
        if is_pressed(pygame.K_LEFT) or is_pressed(pygame.K_a):
            dx -= self.speed
            self.facing_angle = 180.0
        if is_pressed(pygame.K_DOWN) or is_pressed(pygame.K_s):
            dy += self.speed
            self.facing_angle = 90.0
        if is_pressed(pygame.K_UP) or is_pressed(pygame.K_w):
            dy -= self.speed
            self.facing_angle = 270.0

        self.x += dx
        self.y += dy
        self.sync_position()

        if bounds is not None:
            self.rect.clamp_ip(bounds)
            self.x, self.y = self.rect.topleft

        if dx != 0 or dy != 0:
            self.mouth_phase = (self.mouth_phase + 1) % 20

    def draw(self, screen):
        if not hasattr(pygame, "draw"):
            screen.blit(self.image, self.rect)
            return

        center = self.rect.center
        mouth_angle = 35.0 if self.mouth_phase < 10 else 10.0

        num_points = 24
        points = [center]
        start_rad = math.radians(self.facing_angle + mouth_angle)
        end_rad = math.radians(self.facing_angle + 360.0 - mouth_angle)
        for i in range(num_points + 1):
            theta = start_rad + (end_rad - start_rad) * (i / num_points)
            px = center[0] + self.radius * math.cos(theta)
            py = center[1] + self.radius * math.sin(theta)
            points.append((px, py))

        if len(points) >= 3:
            pygame.draw.polygon(screen, PACMAN_COLOR, points)

        eye_offset_angle = math.radians(self.facing_angle + 65.0)
        eye_x = center[0] + 8 * math.cos(eye_offset_angle)
        eye_y = center[1] + 8 * math.sin(eye_offset_angle)
        pygame.draw.circle(screen, (20, 24, 40), (eye_x, eye_y), 2)


class Ghost(GameObject):
    """Enemy Ghost entity moving along the arena."""

    def __init__(self, x, y, speed=3.0, color=BLINKY_COLOR):
        super().__init__(x=x, y=y, speed=speed, size=(36, 36), color=color)
        self.radius = 18
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
        radius = self.radius

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
        pygame.draw.circle(
            screen,
            (0, 0, 180),
            (left_eye[0] + self.direction, left_eye[1]),
            pupil_radius,
        )
        pygame.draw.circle(
            screen,
            (0, 0, 180),
            (right_eye[0] + self.direction, right_eye[1]),
            pupil_radius,
        )


class Pellet(GameObject):
    """Static collectible pellet with points value."""

    def __init__(self, x, y, points=10):
        super().__init__(x=x, y=y, speed=0.0, size=(10, 10), color=PELLET_COLOR)
        self.radius = 5
        self.points = points

    def update(self, bounds=None):
        self.sync_position()

    def draw(self, screen):
        if not self.active:
            return
        if hasattr(pygame, "draw"):
            pygame.draw.circle(screen, PELLET_COLOR, self.rect.center, self.radius)
        else:
            screen.blit(self.image, self.rect)


class Cherry(GameObject):
    """Bonus collectible fruit with animated bobbing."""

    def __init__(self, x, y, points=50):
        super().__init__(x=x, y=y, speed=0.0, size=(28, 28), color=CHERRY_COLOR)
        self.radius = 14
        self.points = points
        self.base_y = float(y)
        self.bob_phase = 0.0

    def update(self, bounds=None):
        self.bob_phase += 0.08
        self.y = self.base_y + math.sin(self.bob_phase) * 5.0
        self.sync_position()

    def draw(self, screen):
        if not self.active:
            return

        if not hasattr(pygame, "draw"):
            screen.blit(self.image, self.rect)
            return

        center = self.rect.center
        left_bulb = (center[0] - 6, center[1] + 4)
        right_bulb = (center[0] + 6, center[1] + 6)
        stem_top = (center[0] + 2, center[1] - 10)

        pygame.draw.line(screen, STEM_COLOR, stem_top, left_bulb, 2)
        pygame.draw.line(screen, STEM_COLOR, stem_top, right_bulb, 2)
        pygame.draw.circle(screen, STEM_COLOR, (stem_top[0] + 3, stem_top[1] - 2), 3)
        pygame.draw.circle(screen, CHERRY_COLOR, left_bulb, 6)
        pygame.draw.circle(screen, CHERRY_COLOR, right_bulb, 6)
        pygame.draw.circle(screen, (255, 200, 200), (left_bulb[0] - 2, left_bulb[1] - 2), 2)
        pygame.draw.circle(screen, (255, 200, 200), (right_bulb[0] - 2, right_bulb[1] - 2), 2)


# =============================================================================
# Automated Verification Suite
# =============================================================================
def run_checks():
    """Automated verification suite testing Week 12 concepts."""
    print("Running Week 12 Collision Detection, Events & Observer checks...")

    if hasattr(pygame, "init") and not isinstance(pygame, type):
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        try:
            pygame.init()
        except Exception:
            pass

    # 1. Verify Euclidean distance collision accuracy vs AABB corner overlap bug
    pacman = Pacman(82, 82)
    pellet = Pellet(117, 117)
    aabb_collides = pacman.rect.colliderect(pellet.rect)
    dist_collides = distance_collision(pacman, pellet, threshold=23)

    assert dist_collides is not None, "Task 1: distance_collision() returned None! Please implement it."
    assert aabb_collides is True, "AABB boxes should overlap at empty corner (bug baseline)"
    assert dist_collides is False, "Euclidean distance check MUST NOT trigger on phantom corner hit!"
    print("  [PASS] distance_collision() eliminates AABB phantom corner collisions")

    # 2. Verify true collision triggers when within radius sum threshold
    pellet_close = Pellet(95, 82)
    assert distance_collision(pacman, pellet_close, threshold=23) is True, (
        "Task 1: distance_collision() must return True when entities touch/overlap."
    )
    print("  [PASS] distance_collision() triggers accurately on true circular contact")

    # 3. Verify Pygame custom event constants
    assert PELLET_EATEN is not None, "Task 2: PELLET_EATEN constant is not defined!"
    assert CHERRY_EATEN is not None, "Task 2: CHERRY_EATEN constant is not defined!"
    assert GHOST_HIT is not None, "Task 2: GHOST_HIT constant is not defined!"
    assert PELLET_EATEN >= pygame.USEREVENT
    assert CHERRY_EATEN > PELLET_EATEN
    assert GHOST_HIT > CHERRY_EATEN
    print("  [PASS] Custom event constants defined cleanly as pygame.USEREVENT offsets")

    # 4. Verify EventObserver ABC contract
    assert issubclass(EventObserver, ABC), "Task 3: EventObserver must inherit from ABC!"
    assert "handle_event" in EventObserver.__abstractmethods__, (
        "Task 3: EventObserver must declare abstract method handle_event()!"
    )
    print("  [PASS] EventObserver(ABC) enforces abstract handle_event() contract")

    # 5. Verify ScoreManager observer decouples points accumulation
    score_mgr = ScoreManager()
    assert isinstance(score_mgr, EventObserver), "Task 3: ScoreManager must inherit from EventObserver!"
    assert score_mgr.score == 0

    event_pellet = pygame.event.Event(PELLET_EATEN, {"points": 10, "pos": (110, 100)})
    assert hasattr(event_pellet, "points") and event_pellet.points == 10
    score_mgr.handle_event(event_pellet)
    assert score_mgr.score == 10 and score_mgr.pellets_eaten == 1, (
        "Task 3: ScoreManager.handle_event() did not add 10 points for PELLET_EATEN!"
    )

    event_cherry = pygame.event.Event(CHERRY_EATEN, {"points": 50, "pos": (200, 200)})
    score_mgr.handle_event(event_cherry)
    assert score_mgr.score == 60 and score_mgr.fruits_eaten == 1, (
        "Task 3: ScoreManager.handle_event() did not add 50 points for CHERRY_EATEN!"
    )
    print("  [PASS] ScoreManager responds to custom events with payload attributes")

    # 6. Verify SoundManager observer plays/records without crashing in headless mode
    sound_mgr = SoundManager(enabled=True)
    assert isinstance(sound_mgr, EventObserver), "Task 4: SoundManager must inherit from EventObserver!"
    sound_mgr.handle_event(event_pellet)
    sound_mgr.handle_event(event_cherry)
    sound_mgr.handle_event(pygame.event.Event(GHOST_HIT, {"damage": 1}))
    assert "chomp" in sound_mgr.sounds_played, "Task 4: SoundManager must play 'chomp' on PELLET_EATEN"
    assert "fruit" in sound_mgr.sounds_played, "Task 4: SoundManager must play 'fruit' on CHERRY_EATEN"
    assert "hazard" in sound_mgr.sounds_played, "Task 4: SoundManager must play 'hazard' on GHOST_HIT"
    print("  [PASS] SoundManager records sound events safely without failing or crashing")

    # 7. Verify Open/Closed Principle: AchievementManager added with zero collision modifications
    achieve_mgr = AchievementManager()
    assert isinstance(achieve_mgr, EventObserver), "Task 5: AchievementManager must inherit from EventObserver!"
    achieve_mgr.handle_event(event_pellet)
    achieve_mgr.handle_event(event_cherry)
    assert "FIRST_BITE" in achieve_mgr.unlocked, "Task 5: AchievementManager must unlock 'FIRST_BITE' on PELLET_EATEN"
    assert "SWEET_TOOTH" in achieve_mgr.unlocked, "Task 5: AchievementManager must unlock 'SWEET_TOOTH' on CHERRY_EATEN"
    print("  [PASS] AchievementManager satisfies Open/Closed Principle (zero collision changes)")

    # 8. Verify check_collisions() emits events and deactivates entities without touching observers
    pacman_test = Pacman(100, 100)
    pellet_test = Pellet(105, 100)
    pellet_far = Pellet(300, 300)
    pellets_test = [pellet_test, pellet_far]

    pygame.event.clear()
    check_collisions(pacman_test, pellets_test)

    assert pellet_test.active is False, "Task 2: Collided pellet must be marked active=False"
    assert pellet_far.active is True, "Task 2: Uncollided pellet must remain active=True"

    queued_events = pygame.event.get()
    pellet_events = [e for e in queued_events if e.type == PELLET_EATEN]
    assert len(pellet_events) == 1, "Task 2: Exactly one PELLET_EATEN event must be posted"
    assert pellet_events[0].points == 10
    print("  [PASS] check_collisions() emits facts to event queue and marks entities inactive")

    # 9. Verify safe list iteration and deferral batch cleanup pattern
    pellets_cleanup = [Pellet(100 + i * 2, 100) for i in range(5)]
    pellets_cleanup[0].active = False
    pellets_cleanup[1].active = False
    pellets_cleanup[2].active = False
    remaining = [p for p in pellets_cleanup if p.active]
    assert len(remaining) == 2, "Batch cleanup should safely filter all inactive items without skipping"
    print("  [PASS] List iteration and deferral batch cleanup preserves collection integrity")

    print("\nAll Week 12 verification checks passed successfully!")


# =============================================================================
# TASK 6: Interactive Game Loop Wiring
# =============================================================================
def main():
    """Interactive Pygame arena with collision detection, custom events, and observers."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SF211 Week 12: Collision Detection & Decoupled Observers (Starter)")
    clock = pygame.time.Clock()

    bounds = pygame.Rect(30, 70, WIDTH - 60, HEIGHT - 90)

    # Entities
    pacman = Pacman(x=120, y=300)
    blinky = Ghost(x=WIDTH - 160, y=300, speed=2.8, color=BLINKY_COLOR)
    cherry = Cherry(x=WIDTH // 2 - 14, y=HEIGHT // 2 - 40, points=50)

    # Pellets distributed along two tracks
    pellets: list[Pellet] = []
    for x in range(70, WIDTH - 70, 36):
        pellets.append(Pellet(x=x, y=200, points=10))
        pellets.append(Pellet(x=x, y=420, points=10))

    # Observers
    score_mgr = ScoreManager()
    sound_mgr = SoundManager(enabled=True)
    hud_mgr = HUDManager(initial_lives=3)
    achieve_mgr = AchievementManager()

    # TODO Task 6 (Part A): Put all observers into a single list
    observers: list[EventObserver] = [
        score_mgr, sound_mgr, hud_mgr, achieve_mgr,
    ]

    running = True
    while running:
        # 1. Input & Event Polling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            # TODO Task 6 (Part B): Dispatch custom events to all observers!
            for obs in observers:
                obs.handle_event(event)

            if event.type == PACMAN_DEFEAT:
                pass

        # 2. Update entities
        pacman.update(bounds=bounds)
        blinky.update(bounds=bounds)
        cherry.update(bounds=bounds)
        for p in pellets:
            p.update(bounds=bounds)

        # 3. Collision Detection -> Emits factual events
        check_collisions(pacman=pacman, pellets=pellets, cherry=cherry, ghost=blinky)

        # 4. Safe collection cleanup via list comprehension deferral
        # TODO Task 6 (Part C): Filter pellets using list comprehension to remove inactive ones
        pellets = [p for p in pellets if p.active]

        # 5. Update HUD state
        hud_mgr.update()

        # 6. Render
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, ARENA_BORDER_COLOR, bounds, width=2, border_radius=8)

        for p in pellets:
            p.draw(screen)
        cherry.draw(screen)
        blinky.draw(screen)
        pacman.draw(screen)

        hud_mgr.draw(screen)

        # Render achievement badges in bottom corner
        if hasattr(pygame, "font") and pygame.font.get_init() and hud_mgr.font_small:
            badge_text = "Badges: " + (", ".join(sorted(achieve_mgr.unlocked)) if achieve_mgr.unlocked else "None")
            badge_surf = hud_mgr.font_small.render(badge_text, True, (160, 180, 210))
            screen.blit(badge_surf, (30, HEIGHT - 26))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Week 12 Starter Code: Collision Detection & Observers")
    parser.add_argument("--check", action="store_true", help="Run automated test suite and exit")
    args = parser.parse_args()

    if args.check:
        run_checks()
    else:
        try:
            main()
        except Exception as e:
            if "video system not initialized" in str(e).lower() or "no available video device" in str(e).lower():
                print(f"Interactive mode requires a graphical display: {e}")
                print("Running --check suite instead:")
                run_checks()
            else:
                raise
