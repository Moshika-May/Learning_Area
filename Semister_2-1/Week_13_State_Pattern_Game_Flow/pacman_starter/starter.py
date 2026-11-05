"""Week 13 Starter Code: State Pattern and Game Flow.

STUDENT INSTRUCTIONS:
In previous weeks, your game ran inside a single continuous loop. But a real game
requires distinct screens: Title/Menu, Gameplay, Pause, and GameOver.

Using boolean flags (is_menu, is_paused, is_gameover) produces tangled, brittle
"flag soup" where adding a new screen requires modifying every single conditional.

In this lab, you will apply the Gang of Four (GoF) State Pattern and a State Stack
to structure the Pacman Arena:

  - Task 1: Complete the `GameState(ABC)` abstract interface contract.
  - Task 2: Implement the `Game` context stack management (`change_state`, `push_state`, `pop_state`).
  - Task 3: Implement `TitleMenuState` to start the game on [SPACE] and quit on [Q].
  - Task 4: Wire `PlayState` to push `PauseState` on [P], and transition to `GameOverState` when lives hit 0.
  - Task 5: Implement `PauseState` to pop off the stack on [P] or [ESC] and resume gameplay.
  - Task 6: Implement `FrightenedState` countdown timer for Ghost AI.

Verify your implementation with automated tests:
    python3 code/week13/starter.py --check
Or run the interactive demonstration:
    python3 code/week13/starter.py
"""

from __future__ import annotations

import argparse
from abc import ABC, abstractmethod
import math
import sys
from typing import Optional

try:
    import pygame
except ImportError:
    # Minimal mock for running headless unit checks without pygame installed
    class _MockRect:
        def __init__(self, x=0, y=0, w=0, h=0):
            self.x = x
            self.y = y
            self.width = w
            self.height = h

        @property
        def center(self):
            return (self.x + self.width // 2, self.y + self.height // 2)

        def colliderect(self, other):
            return not (
                self.x + self.width < other.x
                or other.x + other.width < self.x
                or self.y + self.height < other.y
                or other.y + other.height < self.y
            )

    class _MockSurface:
        def __init__(self, size=(800, 600), flags=0):
            self.size = size

        def fill(self, color):
            pass

        def blit(self, source, dest):
            pass

        def set_alpha(self, alpha):
            pass

        def get_width(self):
            return self.size[0]

        def get_height(self):
            return self.size[1]

    class _MockFont:
        def render(self, text, antialias, color):
            return _MockSurface()

        def size(self, text):
            return (len(str(text)) * 10, 20)

    class _MockPygame:
        K_RIGHT = 1073741903
        K_LEFT = 1073741904
        K_DOWN = 1073741905
        K_UP = 1073741906
        K_SPACE = 32
        K_p = 112
        K_r = 114
        K_m = 109
        K_q = 113
        K_ESCAPE = 27
        QUIT = 256
        KEYDOWN = 768
        SRCALPHA = 0x00010000

        Rect = _MockRect
        Surface = _MockSurface

        class font:
            @staticmethod
            def SysFont(name, size, bold=False):
                return _MockFont()

            @staticmethod
            def init():
                pass

        class draw:
            @staticmethod
            def rect(surface, color, rect, width=0, border_radius=0):
                pass

            @staticmethod
            def circle(surface, color, center, radius, width=0):
                pass

            @staticmethod
            def line(surface, color, start, end, width=1):
                pass

        class event:
            _queue = []

            @classmethod
            def get(cls):
                q = list(cls._queue)
                cls._queue.clear()
                return q

            @classmethod
            def post(cls, evt):
                cls._queue.append(evt)

            class Event:
                def __init__(self, evt_type, **kwargs):
                    self.type = evt_type
                    self.__dict__.update(kwargs)

        class display:
            @staticmethod
            def set_mode(size):
                return _MockSurface(size)

            @staticmethod
            def set_caption(caption):
                pass

            @staticmethod
            def flip():
                pass

        class time:
            class Clock:
                def tick(self, fps=60):
                    return 16

        @staticmethod
        def init():
            pass

        @staticmethod
        def quit():
            pass

    pygame = _MockPygame()


# =============================================================================
# Constants & Colors (SF211 Course Palette)
# =============================================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

COLOR_NAVY = (23, 50, 77)
COLOR_TEAL = (22, 140, 140)
COLOR_GOLD = (227, 165, 43)
COLOR_CORAL = (217, 93, 79)
COLOR_CREAM = (247, 244, 237)
COLOR_INK = (38, 50, 56)
COLOR_BLUE_GHOST = (64, 128, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)


# =============================================================================
# Task 1: Abstract GameState Contract
# =============================================================================
# TODO (Task 1): Inherit from ABC to enforce an abstract contract.
class GameState(ABC):  # Change to: class GameState(ABC):
    """Abstract base class defining the lifecycle contract for game states."""

    def __init__(self, game: Game) -> None:
        self.game = game

    def enter(self) -> None:
        """Called immediately when this state becomes active on the stack."""
        pass

    def exit(self) -> None:
        """Called immediately when this state is popped or replaced."""
        pass

    # TODO (Task 1): Decorate with @abstractmethod
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Process an input event specific to this state."""
        pass

    # TODO (Task 1): Decorate with @abstractmethod
    @abstractmethod
    def update(self, dt: float) -> None:
        """Advance game logic and animations for this state."""
        pass

    # TODO (Task 1): Decorate with @abstractmethod
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Render this state's visuals onto the display surface."""
        pass


# =============================================================================
# Task 2: Game Context & State Stack
# =============================================================================
class Game:
    """The State Machine Context managing the screen stack and game loop."""

    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT) -> None:
        self.width = width
        self.height = height
        self.running = False
        self.state_stack: list[GameState] = []

    @property
    def current_state(self) -> Optional[GameState]:
        """Return the active state at the top of the stack, or None if empty."""
        if self.state_stack:
            return self.state_stack[-1]
        return None

    def change_state(self, new_state: GameState) -> None:
        """Replace the current state completely.

        TODO (Task 2a):
          1. If self.state_stack is not empty, pop the current state and call its exit().
          2. Append new_state to self.state_stack.
          3. Call new_state.enter().
        """
        # TODO Task 2a: Replace pass with your implementation
        if self.state_stack:
            self.state_stack.pop().exit()
        self.state_stack.append(new_state)
        new_state.enter()

    def push_state(self, new_state: GameState) -> None:
        """Push a state on top of the stack without removing lower states.

        TODO (Task 2b):
          1. Append new_state to self.state_stack.
          2. Call new_state.enter().
        """
        # TODO Task 2b: Replace pass with your implementation
        self.state_stack.append(new_state)
        new_state.enter()

    def pop_state(self) -> Optional[GameState]:
        """Pop the active state from the stack, calling exit().

        TODO (Task 2c):
          1. If self.state_stack is empty, return None.
          2. Pop top state, call its exit(), and return the popped state.
        """
        # TODO Task 2c: Replace pass with your implementation
        if not self.state_stack:
            return None
        state = self.state_stack.pop()
        state.exit()
        return state

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if self.current_state:
                self.current_state.handle_event(event)

    def update(self, dt: float) -> None:
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        if not self.state_stack:
            screen.fill(COLOR_NAVY)
            font = pygame.font.SysFont("sans-serif", 24)
            msg = font.render("Complete Task 1 & 2 in starter.py to activate GameState Stack!", True, COLOR_GOLD)
            screen.blit(msg, (screen.get_width() // 2 - msg.get_width() // 2, screen.get_height() // 2 - 10))
            return
        for state in self.state_stack:
            state.draw(screen)

    def quit(self) -> None:
        self.running = False


# =============================================================================
# Ghost AI State Pattern
# =============================================================================
class GhostState(ABC):
    @abstractmethod
    def update(self, ghost: Ghost, dt: float) -> None:
        pass

    @abstractmethod
    def get_color(self) -> tuple[int, int, int]:
        pass


class ChaseState(GhostState):
    def update(self, ghost: Ghost, dt: float) -> None:
        if ghost.target:
            dx = ghost.target.x - ghost.x
            dy = ghost.target.y - ghost.y
            dist = math.hypot(dx, dy)
            if dist > 1:
                ghost.x += (dx / dist) * ghost.speed * dt
                ghost.y += (dy / dist) * ghost.speed * dt

    def get_color(self) -> tuple[int, int, int]:
        return COLOR_CORAL


class ScatterState(GhostState):
    def update(self, ghost: Ghost, dt: float) -> None:
        dx = ghost.home_x - ghost.x
        dy = ghost.home_y - ghost.y
        dist = math.hypot(dx, dy)
        if dist > 1:
            ghost.x += (dx / dist) * ghost.speed * dt
            ghost.y += (dy / dist) * ghost.speed * dt

    def get_color(self) -> tuple[int, int, int]:
        return COLOR_TEAL


class FrightenedState(GhostState):
    """Ghost wanders slowly in blue color until timer expires."""

    def __init__(self, duration: float = 7.0) -> None:
        self.timer = duration

    def update(self, ghost: Ghost, dt: float) -> None:
        """TODO (Task 6):
        1. Decrease self.timer by dt.
        2. Steer ghost away from target at half speed (ghost.speed * 0.5):
           If ghost.target is present:
               dx = ghost.x - ghost.target.x
               dy = ghost.y - ghost.target.y
               dist = math.hypot(dx, dy)
               if dist > 1:
                   ghost.x += (dx / dist) * (ghost.speed * 0.5) * dt
                   ghost.y += (dy / dist) * (ghost.speed * 0.5) * dt
        3. If self.timer <= 0, revert ghost to ChaseState:
           ghost.change_state(ChaseState())
        """
        self.timer -= dt
        if ghost.target:
            dx = ghost.x - ghost.target.x
            dy = ghost.y - ghost.target.y
            dist = math.hypot(dx, dy)
            if dist > 1:
                ghost.x += (dx / dist) * (ghost.speed * 0.5) * dt
                ghost.y += (dy / dist) * (ghost.speed * 0.5) * dt
        if self.timer <= 0:
            ghost.change_state(ChaseState())

    def get_color(self) -> tuple[int, int, int]:
        return COLOR_BLUE_GHOST


class EatenState(GhostState):
    def update(self, ghost: Ghost, dt: float) -> None:
        dx = ghost.home_x - ghost.x
        dy = ghost.home_y - ghost.y
        dist = math.hypot(dx, dy)
        if dist > 2:
            ghost.x += (dx / dist) * (ghost.speed * 2.0) * dt
            ghost.y += (dy / dist) * (ghost.speed * 2.0) * dt
        else:
            ghost.change_state(ChaseState())

    def get_color(self) -> tuple[int, int, int]:
        return COLOR_WHITE


class Ghost:
    def __init__(self, x: float, y: float, home_x: float, home_y: float) -> None:
        self.x = x
        self.y = y
        self.home_x = home_x
        self.home_y = home_y
        self.speed = 100.0
        self.radius = 14
        self.target: Optional[PacmanEntity] = None
        self.state: GhostState = ChaseState()

    def change_state(self, new_state: GhostState) -> None:
        self.state = new_state

    def update(self, dt: float) -> None:
        self.state.update(self, dt)

    def draw(self, screen: pygame.Surface) -> None:
        center = (int(self.x), int(self.y))
        pygame.draw.circle(screen, self.state.get_color(), center, self.radius)
        eye_offset = 4
        pygame.draw.circle(screen, COLOR_WHITE, (center[0] - eye_offset, center[1] - 3), 3)
        pygame.draw.circle(screen, COLOR_WHITE, (center[0] + eye_offset, center[1] - 3), 3)


# =============================================================================
# Entities
# =============================================================================
class PacmanEntity:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 150.0
        self.radius = 14

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, getattr(pygame, "K_d", None)):
                self.vx, self.vy = self.speed, 0
            elif event.key in (pygame.K_LEFT, getattr(pygame, "K_a", None)):
                self.vx, self.vy = -self.speed, 0
            elif event.key in (pygame.K_UP, getattr(pygame, "K_w", None)):
                self.vx, self.vy = 0, -self.speed
            elif event.key in (pygame.K_DOWN, getattr(pygame, "K_s", None)):
                self.vx, self.vy = 0, self.speed

    def update(self, dt: float, bounds: pygame.Rect) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = max(bounds.x + self.radius, min(bounds.x + bounds.width - self.radius, self.x))
        self.y = max(bounds.y + self.radius, min(bounds.y + bounds.height - self.radius, self.y))

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, COLOR_GOLD, (int(self.x), int(self.y)), self.radius)


class PelletEntity:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.radius = 4
        self.active = True

    def draw(self, screen: pygame.Surface) -> None:
        if self.active:
            pygame.draw.circle(screen, COLOR_CREAM, (int(self.x), int(self.y)), self.radius)


# =============================================================================
# Concrete States
# =============================================================================
class TitleMenuState(GameState):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.blink_timer = 0.0
        self.show_prompt = True

    def handle_event(self, event: pygame.event.Event) -> None:
        """TODO (Task 3):
        When player presses [SPACE], change state to PlayState(self.game).
        When player presses [Q], quit via self.game.quit().
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state(PlayState(self.game))
            elif event.key == pygame.K_q:
                self.game.quit()

    def update(self, dt: float) -> None:
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_timer = 0.0
            self.show_prompt = not self.show_prompt

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COLOR_NAVY)
        font_large = pygame.font.SysFont("sans-serif", 52, bold=True)
        font_med = pygame.font.SysFont("sans-serif", 24)
        title_surf = font_large.render("PACMAN ARENA", True, COLOR_GOLD)
        screen.blit(title_surf, (screen.get_width() // 2 - 170, 160))
        if self.show_prompt:
            prompt_surf = font_med.render("PRESS [SPACE] TO START GAME", True, COLOR_TEAL)
            screen.blit(prompt_surf, (screen.get_width() // 2 - 160, 350))


class PlayState(GameState):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.arena_bounds = pygame.Rect(50, 70, game.width - 100, game.height - 120)
        self.pacman = PacmanEntity(game.width // 2, game.height // 2 + 100)
        self.ghost = Ghost(game.width // 2, 140, game.width // 2, 140)
        self.ghost.target = self.pacman
        self.pellets: list[PelletEntity] = []
        self.score = 0
        self.lives = 3
        self._init_pellets()

    def _init_pellets(self) -> None:
        for r in range(4):
            for c in range(10):
                px = self.arena_bounds.x + 40 + c * 65
                py = self.arena_bounds.y + 40 + r * 70
                self.pellets.append(PelletEntity(px, py))

    def handle_event(self, event: pygame.event.Event) -> None:
        """TODO (Task 4a):
        1. When player presses [P], push PauseState(self.game) onto the stack!
        2. When player presses [ESC], change state to TitleMenuState(self.game).
        3. Forward all other events to self.pacman.handle_input(event).
        """
        # TODO Task 4a: Check for [P] and [ESC], then forward other events to pacman
        # (Be sure to keep self.pacman.handle_input(event) for player steering)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.game.push_state(PauseState(self.game))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state(TitleMenuState(self.game))
        else:
            self.pacman.handle_input(event)

    def update(self, dt: float) -> None:
        self.pacman.update(dt, self.arena_bounds)
        self.ghost.update(dt)

        # Collect pellets
        for pellet in self.pellets:
            if pellet.active:
                if math.hypot(self.pacman.x - pellet.x, self.pacman.y - pellet.y) < 18:
                    pellet.active = False
                    self.score += 10
        self.pellets = [p for p in self.pellets if p.active]

        # Check Ghost collision
        if math.hypot(self.pacman.x - self.ghost.x, self.pacman.y - self.ghost.y) < 28:
            if isinstance(self.ghost.state, FrightenedState):
                self.score += 200
                self.ghost.change_state(EatenState())
            else:
                self.lives -= 1
                if self.lives <= 0:
                    self.game.change_state(GameOverState(self.game, self.score))
                else:
                    self.pacman.x = self.game.width // 2
                    self.pacman.y = self.game.height // 2 + 100
                    self.ghost.x = self.game.width // 2
                    self.ghost.y = 140

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COLOR_NAVY)
        pygame.draw.rect(screen, COLOR_TEAL, self.arena_bounds, 3, border_radius=8)
        for pellet in self.pellets:
            pellet.draw(screen)
        self.ghost.draw(screen)
        self.pacman.draw(screen)

        font = pygame.font.SysFont("sans-serif", 20, bold=True)
        score_surf = font.render(f"SCORE: {self.score}", True, COLOR_GOLD)
        lives_surf = font.render(f"LIVES: {self.lives}", True, COLOR_CORAL)
        screen.blit(score_surf, (self.arena_bounds.x, 25))
        screen.blit(lives_surf, (self.arena_bounds.x + self.arena_bounds.width - 100, 25))


class PauseState(GameState):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.overlay_surf = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
        self.overlay_surf.fill((15, 25, 35, 180))

    def handle_event(self, event: pygame.event.Event) -> None:
        """TODO (Task 5):
        When player presses [P] or [ESC], pop this PauseState off the stack:
            self.game.pop_state()
        """
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.game.pop_state()

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.overlay_surf, (0, 0))
        font_large = pygame.font.SysFont("sans-serif", 48, bold=True)
        pause_surf = font_large.render("PAUSED", True, COLOR_GOLD)
        screen.blit(pause_surf, (screen.get_width() // 2 - 90, screen.get_height() // 2 - 50))


class GameOverState(GameState):
    def __init__(self, game: Game, final_score: int) -> None:
        super().__init__(game)
        self.final_score = final_score

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.change_state(PlayState(self.game))
            elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                self.game.change_state(TitleMenuState(self.game))

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COLOR_NAVY)
        font_large = pygame.font.SysFont("sans-serif", 52, bold=True)
        go_surf = font_large.render("GAME OVER", True, COLOR_CORAL)
        screen.blit(go_surf, (screen.get_width() // 2 - 145, 180))


# =============================================================================
# Automated Checks
# =============================================================================
def run_checks() -> None:
    print("Running Week 13 Starter verification tests...")

    # Test 1: ABC Enforcement
    try:
        dummy = GameState(None)  # type: ignore
        raise AssertionError("Task 1 Failed: GameState must inherit from ABC and enforce abstract methods (@abstractmethod)!")
    except TypeError:
        print("  [PASS] Test 1: GameState ABC contract properly enforced")

    # Test 2: State Stack push/pop and enter/exit tracking
    class TrackerState(GameState):
        def __init__(self, game: Game, name: str) -> None:
            super().__init__(game)
            self.name = name
            self.entered = False
            self.exited = False

        def enter(self) -> None:
            self.entered = True

        def exit(self) -> None:
            self.exited = True

        def handle_event(self, event: pygame.event.Event) -> None:
            pass

        def update(self, dt: float) -> None:
            pass

        def draw(self, screen: pygame.Surface) -> None:
            pass

    test_game = Game()
    s1 = TrackerState(test_game, "S1")
    s2 = TrackerState(test_game, "S2")

    test_game.push_state(s1)
    assert s1.entered and not s1.exited, "Task 2b Failed: s1.enter() not triggered on push_state()"
    assert test_game.current_state == s1, "Task 2b Failed: s1 not active state on top of stack"

    test_game.push_state(s2)
    assert s2.entered and not s2.exited, "Task 2b Failed: s2.enter() not triggered on push_state()"
    assert not s1.exited, "Task 2b Failed: s1.exit() should NOT trigger when s2 is pushed on top"
    assert len(test_game.state_stack) == 2, "Task 2b Failed: state_stack length should be 2"

    popped = test_game.pop_state()
    assert popped == s2, "Task 2c Failed: pop_state() did not return the popped top state"
    assert s2.exited, "Task 2c Failed: popped state exit() was not called"
    assert test_game.current_state == s1, "Task 2c Failed: s1 should resume as active state after pop"

    s3 = TrackerState(test_game, "S3")
    test_game.change_state(s3)
    assert s1.exited, "Task 2a Failed: s1.exit() should trigger when replaced via change_state()"
    assert s3.entered, "Task 2a Failed: s3.enter() should trigger when activated via change_state()"
    assert len(test_game.state_stack) == 1, "Task 2a Failed: Stack size should be 1 after change_state()"
    print("  [PASS] Test 2: State Stack lifecycle (push/pop/change enter/exit) verified")

    # Test 3: TitleMenuState transitions to PlayState on SPACE
    game = Game()
    menu = TitleMenuState(game)
    game.change_state(menu)
    assert isinstance(game.current_state, TitleMenuState), "Initial state must be TitleMenuState"

    space_evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    game.current_state.handle_event(space_evt)
    assert isinstance(game.current_state, PlayState), "Task 3 Failed: Pressing [SPACE] in TitleMenuState did not transition to PlayState"
    print("  [PASS] Test 3: TitleMenuState -> PlayState transition verified")

    # Test 4: PlayState pushes PauseState on 'P' key and preserves PlayState state
    play = game.current_state
    assert isinstance(play, PlayState)
    play.score = 250
    play.lives = 2

    p_evt = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)
    game.current_state.handle_event(p_evt)
    assert isinstance(game.current_state, PauseState), "Task 4a Failed: Pressing [P] in PlayState did not push PauseState"
    assert len(game.state_stack) == 2, "Task 4a Failed: State stack did not preserve PlayState under PauseState"

    # Resuming via PauseState
    game.current_state.handle_event(p_evt)
    assert isinstance(game.current_state, PlayState), "Task 5 Failed: Pressing [P] in PauseState did not pop back to PlayState"
    assert game.current_state.score == 250 and game.current_state.lives == 2, "Task 5 Failed: PlayState lost data when resuming!"
    print("  [PASS] Test 4: PauseState push/pop preserves PlayState data intact")

    # Test 5: GameOverState transition on 0 lives
    game.current_state.lives = 1
    game.current_state.pacman.x = game.current_state.ghost.x
    game.current_state.pacman.y = game.current_state.ghost.y
    game.current_state.update(0.016)
    assert isinstance(game.current_state, GameOverState), "Task 4b Failed: Fatal collision with 0 lives did not trigger GameOverState"
    print("  [PASS] Test 5: PlayState -> GameOverState transition on defeat verified")

    # Test 6: Ghost AI State Pattern transfer
    ghost = Ghost(0, 0, 100, 100)
    assert isinstance(ghost.state, ChaseState)
    ghost.change_state(FrightenedState(duration=1.0))
    assert isinstance(ghost.state, FrightenedState)
    assert ghost.state.get_color() == COLOR_BLUE_GHOST
    ghost.update(1.5)  # Elapsed beyond 1.0s timer
    assert isinstance(ghost.state, ChaseState), "Task 6 Failed: FrightenedState timer expiration did not revert to ChaseState"
    print("  [PASS] Test 6: Ghost AI Finite State Machine transfer verified")

    print("\nALL 6 VERIFICATION CHECKS PASSED SUCCESSFULLY!")


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SF211 Week 13: State Pattern Starter")
    clock = pygame.time.Clock()

    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.change_state(TitleMenuState(game))
    game.running = True

    while game.running:
        dt = clock.tick(FPS) / 1000.0
        game.handle_events()
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run automated test suite")
    args = parser.parse_args()
    if args.check:
        run_checks()
    else:
        main()
