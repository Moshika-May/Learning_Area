"""Week 4 Starter Code: Building Modular Mechanics with Composition.

STUDENT INSTRUCTIONS:
In lecture, you learned how to decompose a god class into focused components
(Transform, Health, Renderer, InputController, Entity).

Now, put composition to work! Your challenge is to build new gameplay mechanics
by creating and combining reusable building blocks:

- Challenge 1: Implement `Shield` (absorbs damage before Health takes damage).
- Challenge 2: Implement `PatrolController` (steers an entity cyclically between waypoints).
- Challenge 3: Implement `LinearController` & `create_bullet` (assembles projectiles from components).
- Challenge 4: Implement `ShieldedEntity` (composes both Shield and Health).

Verify your implementation with automated tests:
    python code/week04/starter.py --check
Or run the interactive arena:
    python code/week04/starter.py
"""

import sys
import math
import random
import pygame

# Game Window Constants
WIDTH, HEIGHT = 800, 600
FPS = 60


# =============================================================================
# PART 1: BASE COMPONENTS (Pre-provided from Lecture)
# =============================================================================

class Transform:
    """Responsibility: track spatial position, speed, and boundaries."""

    def __init__(self, x: float, y: float, speed: float = 200.0):
        self.x = float(x)
        self.y = float(y)
        self.speed = float(speed)

    def move(self, dx: float, dy: float, dt: float, bounds=None):
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
        if bounds is not None:
            self.x = max(0.0, min(float(bounds.width - 40), self.x))
            self.y = max(0.0, min(float(bounds.height - 40), self.y))
        else:
            self.x = max(0.0, min(float(WIDTH - 40), self.x))
            self.y = max(0.0, min(float(HEIGHT - 40), self.y))

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), 40, 40)


class Health:
    """Responsibility: track hit points and render health bar UI."""

    def __init__(self, max_hp: int):
        self.max_hp = int(max_hp)
        self._hp = int(max_hp)

    @property
    def hp(self) -> int:
        return self._hp

    def take_damage(self, amount: int):
        if amount < 0:
            raise ValueError("Damage cannot be negative")
        self._hp = max(0, self._hp - int(amount))

    def heal(self, amount: int):
        if amount < 0:
            raise ValueError("Heal amount cannot be negative")
        self._hp = min(self.max_hp, self._hp + int(amount))

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    def draw_bar(self, screen: pygame.Surface, rect: pygame.Rect):
        pct = self._hp / self.max_hp if self.max_hp > 0 else 0
        bar_bg = pygame.Rect(rect.x, rect.y - 10, rect.width, 5)
        bar_fg = pygame.Rect(rect.x, rect.y - 10, int(rect.width * pct), 5)
        pygame.draw.rect(screen, (60, 60, 60), bar_bg)
        pygame.draw.rect(screen, (0, 200, 0), bar_fg)


class Renderer:
    """Responsibility: draw visual representation on screen."""

    def __init__(self, color: tuple[int, int, int]):
        self.color = color

    def draw(self, screen: pygame.Surface, rect: pygame.Rect):
        pygame.draw.rect(screen, self.color, rect)


class InputController:
    """Responsibility: turn keyboard input into a movement vector."""

    def get_direction(self, current_pos=(0, 0), dt=0.0) -> tuple[float, float]:
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        if dx != 0 and dy != 0:
            inv_len = 1.0 / math.sqrt(dx * dx + dy * dy)
            return dx * inv_len, dy * inv_len
        return float(dx), float(dy)


class Entity:
    """Coordinates base components via delegation."""

    def __init__(self, transform: Transform, renderer: Renderer, health: Health, controller):
        self.transform = transform
        self.renderer = renderer
        self.health = health
        self.controller = controller

    def update(self, dt: float):
        dx, dy = self.controller.get_direction((self.transform.x, self.transform.y), dt)
        self.transform.move(dx, dy, dt)

    def draw(self, screen: pygame.Surface):
        rect = self.transform.rect
        self.renderer.draw(screen, rect)
        if self.health is not None:
            self.health.draw_bar(screen, rect)


# =============================================================================
# PART 2: YOUR CHALLENGE IMPLEMENTATIONS (Complete these 4 tasks!)
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# CHALLENGE 1: Shield Component
# ─────────────────────────────────────────────────────────────────────────────
class Shield:
    """Responsibility: absorb incoming damage before it reaches Health."""

    def __init__(self, max_shield: int):
        self.max_shield = int(max_shield)
        self._shield = int(max_shield)

    @property
    def shield(self) -> int:
        return self._shield

    def absorb_damage(self, amount: int) -> int:
        """Absorb damage up to current shield points. Return remaining unabsorbed damage."""
        if amount < 0:
            raise ValueError("Damage cannot be negative")
        if self._shield >= amount:
            self._shield -= amount
            return 0
        overflow = amount - self._shield
        self._shield = 0
        return overflow

    def recharge(self, amount: int):
        """Recharge shield points up to max_shield."""
        if amount < 0:
            raise ValueError("Recharge amount cannot be negative")
        self._shield = min(self.max_shield, self._shield + amount)

    def draw_bar(self, screen: pygame.Surface, rect: pygame.Rect):
        """Draw cyan shield bar above the health bar."""
        pct = self._shield / self.max_shield if self.max_shield > 0 else 0
        bar_bg = pygame.Rect(rect.x, rect.y - 17, rect.width, 4)
        bar_fg = pygame.Rect(rect.x, rect.y - 17, int(rect.width * pct), 4)
        pygame.draw.rect(screen, (40, 40, 60), bar_bg)
        pygame.draw.rect(screen, (0, 200, 255), bar_fg)


# ─────────────────────────────────────────────────────────────────────────────
# CHALLENGE 2: PatrolController
# ─────────────────────────────────────────────────────────────────────────────
class PatrolController:
    """Responsibility: steer an entity cyclically through a sequence of waypoints."""

    def __init__(self, waypoints: list[tuple[float, float]], arrival_threshold: float = 6.0):
        if not waypoints:
            raise ValueError("PatrolController requires at least one waypoint")
        self.waypoints = [(float(x), float(y)) for x, y in waypoints]
        self.current_idx = 0
        self.arrival_threshold = arrival_threshold

    def get_direction(self, current_pos: tuple[float, float], dt: float = 0.0) -> tuple[float, float]:
        """Calculate a normalized direction vector (dx, dy) towards the current waypoint."""
        curr_x, curr_y = current_pos
        target_x, target_y = self.waypoints[self.current_idx]
        dist = math.hypot(target_x - curr_x, target_y - curr_y)

        if dist <= self.arrival_threshold:
            self.current_idx = (self.current_idx + 1) % len(self.waypoints)
            target_x, target_y = self.waypoints[self.current_idx]
            dist = math.hypot(target_x - curr_x, target_y - curr_y)

        dx = target_x - curr_x
        dy = target_y - curr_y
        if dist > 0.001:
            return dx / dist, dy / dist
        return 0.0, 0.0


# ─────────────────────────────────────────────────────────────────────────────
# CHALLENGE 3: LinearController & Bullets
# ─────────────────────────────────────────────────────────────────────────────
class LinearController:
    """Responsibility: move consistently along a fixed directional vector."""

    def __init__(self, dx: float, dy: float):
        """Normalize the input vector (dx, dy) and store self.dx, self.dy."""
        mag = math.hypot(dx, dy)
        if mag > 0.001:
            self.dx = dx / mag
            self.dy = dy / mag
        else:
            self.dx, self.dy = 0.0, 0.0

    def get_direction(self, current_pos=(0, 0), dt=0.0) -> tuple[float, float]:
        """Return the fixed normalized direction (self.dx, self.dy)."""
        return self.dx, self.dy


def create_bullet(x: float, y: float, dx: float, dy: float) -> Entity:
    """Assembles a projectile entity entirely from standard reusable components."""
    return Entity(
        transform=Transform(x, y, speed=450.0),
        renderer=Renderer((255, 220, 0)),
        health=Health(1),
        controller=LinearController(dx, dy),
    )


# ─────────────────────────────────────────────────────────────────────────────
# CHALLENGE 4: ShieldedEntity
# ─────────────────────────────────────────────────────────────────────────────
class ShieldedEntity(Entity):
    """An Entity that composes a Shield alongside Health."""

    def __init__(self, transform: Transform, renderer: Renderer, health: Health, shield: Shield, controller):
        super().__init__(transform, renderer, health, controller)
        self.shield = shield

    def take_damage(self, amount: int):
        """Route incoming damage through the Shield first."""
        overflow = self.shield.absorb_damage(amount)
        if overflow > 0 and self.health is not None:
            self.health.take_damage(overflow)

    def draw(self, screen: pygame.Surface):
        """Draw base entity visual & health bar, plus shield bar on top."""
        super().draw(screen)
        if self.shield is not None:
            self.shield.draw_bar(screen, self.transform.rect)


# =============================================================================
# PART 3: AUTOMATED VERIFICATION SUITE
# =============================================================================

def run_checks():
    """Deterministic automated verification of all modular components."""
    print("Running Week 4 automated verification suite...")

    # 1. Shield tests
    s = Shield(50)
    assert s.shield == 50
    overflow = s.absorb_damage(30)
    assert s.shield == 20 and overflow == 0, "Shield should absorb damage <= shield points"
    overflow = s.absorb_damage(30)
    assert s.shield == 0 and overflow == 10, "Shield should deplete and return overflow damage"
    s.recharge(40)
    assert s.shield == 40, "Shield.recharge should restore shield points"
    s.recharge(100)
    assert s.shield == 50, "Shield.recharge should clamp at max_shield"
    print("  [PASS] Shield component")

    # 2. PatrolController tests
    waypoints = [(100.0, 100.0), (300.0, 100.0)]
    pc = PatrolController(waypoints, arrival_threshold=5.0)
    dx, dy = pc.get_direction(current_pos=(100.0, 100.0), dt=0.016)
    assert dx > 0.9 and abs(dy) < 0.1, "PatrolController should point towards next waypoint"
    print("  [PASS] PatrolController")

    # 3. LinearController & Bullet tests
    bullet = create_bullet(200.0, 200.0, 1.0, 0.0)
    assert isinstance(bullet, Entity), "Bullets should be assembled from the Entity class"
    bullet.update(0.1)
    assert bullet.transform.x > 200.0, "Bullet should advance along direction vector"
    print("  [PASS] LinearController & Bullet composition")

    # 4. ShieldedEntity tests
    h = Health(100)
    sh = Shield(40)
    boss = ShieldedEntity(
        transform=Transform(400, 300, speed=100),
        renderer=Renderer((200, 50, 200)),
        health=h,
        shield=sh,
        controller=pc
    )
    boss.take_damage(25)
    assert boss.shield.shield == 15 and boss.health.hp == 100, "Damage within shield shouldn't touch Health"
    boss.take_damage(35)
    assert boss.shield.shield == 0 and boss.health.hp == 80, "Overflow damage should deduct from Health"
    print("  [PASS] ShieldedEntity coordination")

    print("\nSUCCESS: All Week 4 Exercise checks passed!")


# =============================================================================
# PART 4: INTERACTIVE DEMO ARENA
# =============================================================================

def main():
    if "--check" in sys.argv:
        run_checks()
        return

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Week 4: Composed Arena — Shielded Patrol vs Player Bullets")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # 1. Player Entity
    player = Entity(
        transform=Transform(100, 300, speed=240),
        renderer=Renderer((60, 140, 255)),
        health=Health(100),
        controller=InputController(),
    )

    # 2. Shielded Patrolling Enemy
    patrol_waypoints = [(600, 100), (600, 480), (350, 480), (350, 100)]
    enemy = ShieldedEntity(
        transform=Transform(600, 100, speed=160),
        renderer=Renderer((240, 60, 60)),
        health=Health(100),
        shield=Shield(60),
        controller=PatrolController(patrol_waypoints),
    )

    bullets: list[Entity] = []
    shoot_cooldown = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        shoot_cooldown = max(0.0, shoot_cooldown - dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and shoot_cooldown <= 0:
                    bullets.append(create_bullet(
                        player.transform.x + 35,
                        player.transform.y + 15,
                        dx=1.0, dy=0.0
                    ))
                    shoot_cooldown = 0.2
                elif event.key == pygame.K_r:
                    enemy.shield.recharge(30)

        # Update Entities
        player.update(dt)
        if enemy.health.is_alive:
            enemy.update(dt)

        for b in bullets:
            b.update(dt)
        bullets = [b for b in bullets if 0 <= b.transform.x <= WIDTH and 0 <= b.transform.y <= HEIGHT]

        # Check Bullet-Enemy collisions
        if enemy.health.is_alive:
            enemy_rect = enemy.transform.rect
            for b in bullets[:]:
                if enemy_rect.colliderect(b.transform.rect):
                    enemy.take_damage(20)
                    bullets.remove(b)

        # Rendering
        screen.fill((20, 24, 32))

        # Draw patrol path
        for i in range(len(patrol_waypoints)):
            pt1 = patrol_waypoints[i]
            pt2 = patrol_waypoints[(i + 1) % len(patrol_waypoints)]
            pygame.draw.line(screen, (45, 55, 75), (pt1[0] + 20, pt1[1] + 20), (pt2[0] + 20, pt2[1] + 20), 2)
            pygame.draw.circle(screen, (70, 90, 130), (pt1[0] + 20, pt1[1] + 20), 5)

        player.draw(screen)
        if enemy.health.is_alive:
            enemy.draw(screen)
        for b in bullets:
            b.draw(screen)

        # HUD Instructions
        txt1 = font.render("WASD/Arrows: Move | SPACE: Shoot Bullets | R: Recharge Enemy Shield", True, (200, 200, 210))
        if enemy.health.is_alive:
            txt2 = font.render(f"Enemy Shield: {enemy.shield.shield}/60 | Enemy HP: {enemy.health.hp}/100", True, (0, 220, 255) if enemy.shield.shield > 0 else (0, 220, 0))
        else:
            txt2 = font.render("Enemy Defeated! Press R to recharge and restore.", True, (255, 200, 50))
        screen.blit(txt1, (20, 20))
        screen.blit(txt2, (20, 50))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
