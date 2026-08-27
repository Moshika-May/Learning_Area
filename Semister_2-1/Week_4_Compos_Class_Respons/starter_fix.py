"""
Composition & Class Responsibilities in OOP -- Pygame Demo
===========================================================

TEACHING GOAL
-------------
Show students that instead of building one big Entity class (or a deep
inheritance tree like Entity -> Player -> Enemy -> FlyingEnemy...), we can
give each *behavior* its own small class with ONE responsibility, and build
game objects by *composing* those pieces together.

    Transform    -> only knows about position/movement
    Health       -> only knows about hit points
    Shield       -> only knows about absorbing/recharging armor
    Renderer     -> only knows how to draw a shape
    Controller   -> only decides "what direction should I move this frame?"

An Entity is just a container that HAS-A Transform, HAS-A Health,
HAS-A Renderer, HAS-A Controller. Swap any one component and you get a
different kind of object, with no new subclass and no shared base-class
bloat.

Controls: Arrow keys / WASD move the blue Player square. SPACE fires a
bullet in the direction you're currently moving (or last moved).
Walk into an enemy, or shoot it, to damage it.

Run:  python composition_demo.py   (requires: pip install pygame)
"""

import random
import pygame

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 100


# ---------------------------------------------------------------------------
# COMPONENTS
# Each class below has exactly ONE job.
# ---------------------------------------------------------------------------

class Transform:
    """Responsibility: track WHERE something is and move it."""

    # FIX: added `clamp` so bullets (clamp=False) can leave the screen
    # instead of getting stuck at the wall like the player/enemies do.
    def __init__(self, x, y, speed=200, clamp=True):
        self.x = x
        self.y = y
        self.speed = speed  # pixels per second
        self.clamp = clamp

    def move(self, dx, dy, dt):
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
        if self.clamp:
            # keep on screen
            self.x = max(0, min(WIDTH - 40, self.x))
            self.y = max(0, min(HEIGHT - 40, self.y))

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), 40, 40)

    # FIX: added — main() filters bullets with `b.transform.on_screen`
    # but this property never existed.
    @property
    def on_screen(self):
        return -40 <= self.x <= WIDTH and -40 <= self.y <= HEIGHT


class Shield:
    """Responsibility: absorb incoming damage before it reaches Health,
    and recharge itself over time after a delay."""

    def __init__(self, max_shield, recharge_rate, recharge_delay):
        self.max_shield = max_shield
        self.shield = max_shield
        self.recharge_rate = recharge_rate
        self.recharge_delay = recharge_delay
        # FIX: was `self.cooldown = 0.1` — wrong name (no underscore) AND
        # absorb_damage()/recharge() both need this to exist as `_cooldown`
        # from the start, or recharge() crashes before any damage is taken.
        self._cooldown = 0

    def absorb_damage(self, amount):
        self._cooldown = self.recharge_delay
        if amount <= self.shield:
            self.shield -= amount
            return 0
        leftover = amount - self.shield
        self.shield = 0
        return leftover

    def recharge(self, dt):
        if self._cooldown > 0:
            # FIX: was decrementing `self.cooldown` (a different, unused
            # attribute) instead of `self._cooldown` — the timer never
            # actually counted down, so the shield never recharged.
            self._cooldown -= dt
            return
        self.shield = min(self.max_shield, self.shield + self.recharge_rate * dt)

    @property
    def is_active(self):
        return self.shield > 0

    # FIX: was `def draw_bar(self):` with no screen/rect params, but the
    # body used `screen`/`rect` anyway (undefined names -> NameError), and
    # callers pass draw_bar(screen, rect). Also unified both bars to the
    # same y-offset (-18) so they overlap correctly instead of the
    # background bar sitting above the foreground bar.
    def draw_bar(self, screen, rect):
        pct = self.shield / self.max_shield
        bar_bg = pygame.Rect(rect.x, rect.y - 18, rect.width, 4)
        bar_fg = pygame.Rect(rect.x, rect.y - 18, int(rect.width * pct), 4)
        pygame.draw.rect(screen, (30, 40, 60), bar_bg)
        pygame.draw.rect(screen, (80, 100, 255), bar_fg)


class PatrolController:
    """Responsibility: move toward waypoints in order, looping forever."""

    def __init__(self, transform, waypoints, arrive_threshold=4):
        self.transform = transform
        self.waypoints = waypoints
        self.arrive_threshold = arrive_threshold
        # FIX: was missing entirely — get_direction() indexes
        # self.waypoints[self.index] and would raise AttributeError
        # on the very first call without this.
        self.index = 0

    def get_direction(self, dt):
        target_x, target_y = self.waypoints[self.index]
        dx = target_x - self.transform.x
        # FIX: typo `tarfet_y` -> `target_y` (was a NameError)
        dy = target_y - self.transform.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist < self.arrive_threshold:
            self.index = (self.index + 1) % len(self.waypoints)
            return (0, 0)
        return (dx / dist, dy / dist)


class LinearController:
    """Responsibility: always return the same fixed direction (bullets)."""

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def get_direction(self, dt):
        return (self.dx, self.dy)


class Health:
    """Responsibility: track hit points and whether the owner is alive."""

    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.hp = max_hp

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    @property
    def is_alive(self):
        return self.hp > 0

    def draw_bar(self, screen, rect):
        """Small helper so Health owns its own UI, not Entity."""
        pct = self.hp / self.max_hp
        bar_bg = pygame.Rect(rect.x, rect.y - 10, rect.width, 5)
        bar_fg = pygame.Rect(rect.x, rect.y - 10, int(rect.width * pct), 5)
        pygame.draw.rect(screen, (60, 60, 60), bar_bg)
        pygame.draw.rect(screen, (0, 200, 0), bar_fg)


class Renderer:
    """Responsibility: draw a shape. Knows nothing about movement or HP."""

    def __init__(self, color):
        self.color = color

    def draw(self, screen, rect):
        pygame.draw.rect(screen, self.color, rect)


class InputController:
    """Responsibility: turn keyboard state into a movement direction.
    Used by the player-controlled entity.
    """

    # FIX: added — main() reads player.controller.last_dx/last_dy to
    # know which way to fire a bullet, but these were never created.
    def __init__(self):
        self.last_dx, self.last_dy = 0, -1  # default facing: up

    def get_direction(self, dt):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - \
             (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - \
             (keys[pygame.K_UP] or keys[pygame.K_w])
        if dx or dy:
            self.last_dx, self.last_dy = dx, dy
        return dx, dy


class WanderController:
    """Responsibility: pick a random direction and change its mind sometimes.
    Used by the enemy — same interface as InputController (get_direction),
    but a totally different decision process. Entity doesn't care which
    one it's holding.
    """

    def __init__(self):
        self.dx, self.dy = 0, 0
        self.timer = 0

    def get_direction(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.timer = random.uniform(0.5, 1.5)
        return self.dx, self.dy


def make_bullet(x, y, dx, dy, speed=800):
    """Build a bullet using the plain Entity class — no new subclass needed."""
    return Entity(
        transform=Transform(x, y, speed=speed, clamp=False),
        renderer=Renderer((255, 220, 60)),
        health=Health(1),
        controller=LinearController(dx, dy),
    )


# ---------------------------------------------------------------------------
# ENTITY — the composition itself
# ---------------------------------------------------------------------------

class Entity:
    """An Entity HAS-A Transform, Renderer, Health, and Controller.

    Notice: Entity contains almost no logic of its own. It just asks each
    component to do its one job and coordinates them. This is composition:
    behavior is built by plugging pieces together, not by inheriting from
    an ever-growing base class.
    """

    def __init__(self, transform: Transform, renderer: Renderer,
                 health: Health, controller):
        self.transform = transform
        self.renderer = renderer
        self.health = health
        self.controller = controller

    def update(self, dt):
        dx, dy = self.controller.get_direction(dt)
        self.transform.move(dx, dy, dt)

    # FIX: added. main() calls `enermy.take_damage(1)` on every entity in
    # the enemies list, including plain (non-shielded) ones — without this
    # method on the base class that raised AttributeError.
    def take_damage(self, amount):
        self.health.take_damage(amount)

    def draw(self, screen):
        rect = self.transform.rect
        self.renderer.draw(screen, rect)
        self.health.draw_bar(screen, rect)


class ShieldedEntity(Entity):
    """An Entity that also HAS-A Shield. Damage hits the shield first;
    only whatever punches through reaches Health."""

    def __init__(self, transform, renderer, health, controller, shield: Shield):
        super().__init__(transform, renderer, health, controller)
        self.shield = shield

    def take_damage(self, amount):
        leftover = self.shield.absorb_damage(amount)
        if leftover > 0:
            self.health.take_damage(leftover)

    def update(self, dt):
        super().update(dt)
        self.shield.recharge(dt)

    def draw(self, screen):
        super().draw(screen)
        if self.shield.is_active or self.shield.shield < self.shield.max_shield:
            self.shield.draw_bar(screen, self.transform.rect)


# ---------------------------------------------------------------------------
# GAME LOOP
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Composition Demo")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    # Build the player: same Entity class, different components plugged in.
    player = Entity(
        transform=Transform(100, 300, speed=240),
        renderer=Renderer((60, 120, 255)),
        health=Health(100),
        controller=InputController(),
    )

    patrol_transform = Transform(600, 100)
    patrol_enemy = Entity(
        transform=patrol_transform,
        renderer=Renderer((220, 60, 60)),
        health=Health(40),
        controller=PatrolController(
            patrol_transform,
            waypoints=[(600, 100), (600, 400), (300, 400), (300, 100)],
        ),
    )

    shielded_transform = Transform(400, 400)
    shielded_enemy = ShieldedEntity(
        transform=shielded_transform,
        renderer=Renderer((100, 90, 220)),
        health=Health(50),
        controller=WanderController(),
        shield=Shield(max_shield=40, recharge_rate=10, recharge_delay=1.0),
    )

    # FIX: removed the old standalone `enemy = Entity(..., WanderController())`
    # from starter.py. It was never added to `enemies`, yet the update/
    # collision loops below (originally written with a `enermy` loop var
    # but an `enemy` condition inside) silently checked/damaged *that*
    # leftover object instead of the real list contents — patrol_enemy and
    # shielded_enemy were never actually being updated or hit by bullets.
    # Renamed enermy/enermies -> enemy/enemies everywhere and made every
    # loop consistently use its own loop variable, so this typo/shadowing
    # bug can't happen again.
    enemies = [patrol_enemy, shielded_enemy]
    bullets = []
    space_was_down = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not space_was_down:
            fx, fy = player.controller.last_dx, player.controller.last_dy
            length = (fx ** 2 + fy ** 2) ** 0.5 or 1
            bx = player.transform.x + 20
            by = player.transform.y + 20
            bullets.append(make_bullet(bx, by, fx / length, fy / length))
        space_was_down = keys[pygame.K_SPACE]

        player.update(dt)

        for enemy in enemies:
            if enemy.health.is_alive:
                enemy.update(dt)

        for bullet in bullets:
            bullet.update(dt)

        for bullet in bullets:
            if not bullet.health.is_alive:
                continue
            for enemy in enemies:
                if enemy.health.is_alive and bullet.transform.rect.colliderect(enemy.transform.rect):
                    # FIX: was `enemy.health.take_damage(15)`, which bypassed
                    # the shield completely for shielded_enemy. Using
                    # take_damage() routes it through the shield first.
                    enemy.take_damage(15)
                    bullet.health.take_damage(1)

        bullets = [b for b in bullets if b.health.is_alive and b.transform.on_screen]

        for enemy in enemies:
            if enemy.health.is_alive and player.transform.rect.colliderect(enemy.transform.rect):
                enemy.take_damage(1)

        screen.fill((25, 25, 30))
        player.draw(screen)
        for enemy in enemies:
            if enemy.health.is_alive:
                enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        if not any(enemy.health.is_alive for enemy in enemies):
            msg = font.render("All enemies defeated!", True, (255, 255, 255))
            screen.blit(msg, (WIDTH // 2 - 90, 20))

        hint = font.render(
            "Arrows/WASD move, SPACE shoot. Touch or shoot enemies to damage them.",
            True, (200, 200, 200))
        screen.blit(hint, (10, HEIGHT - 25))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
