"""Week 10 Exercise: Polymorphic Sprite Arena.

Tasks:
  1. Complete Block, Player, Enemy, Collectible, and Bullet subclasses extending pygame.sprite.Sprite.
  2. Implement polymorphic update() methods for Player and Enemy.
  3. Implement Bullet update() and off-screen cleanup with self.kill().
  4. Build the polymorphic game loop using all_sprites.update(),
     pygame.sprite.groupcollide(), and all_sprites.draw(screen).

Run tests:
  python3 arena.py --check
Run interactive game:
  python3 arena.py
"""

import argparse
import sys
import pygame

WIDTH, HEIGHT, FPS = 800, 600, 60
BG = (24, 28, 38)


# =============================================================================
# TASK 1: Define Base Sprite and Subclasses
# =============================================================================

class Block(pygame.sprite.Sprite):
    """Base sprite with image, rect, and default polymorphic update."""

    def __init__(self, x, y, size, color):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, controls=None):
        pass


class Player(Block):
    """Player sprite (38x38, color: (70, 145, 240)) controlled with Arrow keys."""

    def __init__(self, x, y):
        super().__init__(x, y, (38, 38), (70, 145, 240))

    def update(self, controls=None):
        if controls:
            dx = controls[pygame.K_RIGHT] - controls[pygame.K_LEFT]
            dy = controls[pygame.K_DOWN] - controls[pygame.K_UP]
            self.rect.x += 5 * dx
            self.rect.y += 5 * dy
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Enemy(Block):
    """Enemy sprite (38x38, color: (225, 90, 80)) patrolling horizontally."""

    def __init__(self, x, y):
        super().__init__(x, y, (38, 38), (225, 90, 80))
        self.velocity = 2

    def update(self, controls=None):
        self.rect.x += self.velocity
        if self.rect.left <= 80 or self.rect.right >= 720:
            self.velocity *= -1


class Collectible(Block):
    """Stationary coin/bonus (22x22, color: (245, 195, 65))."""

    def __init__(self, x, y):
        super().__init__(x, y, (22, 22), (245, 195, 65))


class Bullet(Block):
    """Bullet projectile (8x18, color: (235, 235, 245)) moving upward."""

    def __init__(self, x, y):
        super().__init__(x, y, (8, 18), (235, 235, 245))

    def update(self, controls=None):
        self.rect.y -= 8
        if self.rect.bottom < 0:
            self.kill()


# =============================================================================
# Automated Verification Checks
# =============================================================================

def run_checks():
    """Run verification checks."""
    player = Player(100, 100)
    enemy = Enemy(200, 200)
    collectible = Collectible(300, 300)
    bullet = Bullet(400, 100)

    all_sprites = pygame.sprite.Group(player, enemy, collectible, bullet)
    enemies = pygame.sprite.Group(enemy)
    bullets = pygame.sprite.Group(bullet)

    assert len(all_sprites) == 4, f"Expected 4 sprites, got {len(all_sprites)}"
    assert len({type(s) for s in all_sprites}) == 4, "Expected 4 distinct sprite types"
    print("  [PASS] Task 1: 4 distinct Sprite subclasses created in heterogeneous Group")

    init_enemy_x = enemy.rect.x
    init_bullet_y = bullet.rect.y
    all_sprites.update(None)
    assert enemy.rect.x != init_enemy_x, "Enemy should move during update()"
    assert bullet.rect.y != init_bullet_y, "Bullet should move during update()"
    print("  [PASS] Task 2: Polymorphic update() dispatches to all sprites without type checks")

    offscreen_bullet = Bullet(400, -20)
    all_sprites.add(offscreen_bullet)
    bullets.add(offscreen_bullet)
    all_sprites.update(None)
    assert offscreen_bullet not in all_sprites, "Off-screen bullet should be removed from all_sprites"
    assert offscreen_bullet not in bullets, "Off-screen bullet should be removed from bullets"
    print("  [PASS] Task 3: Off-screen bullet calls kill() and cleans up from all groups")

    colliding_bullet = Bullet(enemy.rect.x, enemy.rect.y)
    all_sprites.add(colliding_bullet)
    bullets.add(colliding_bullet)
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    assert colliding_bullet in hits, "groupcollide should detect collision"
    assert enemy in hits[colliding_bullet], "Hit list should contain enemy"
    assert enemy not in all_sprites and enemy not in enemies, "Enemy should be killed"
    assert colliding_bullet not in all_sprites and colliding_bullet not in bullets, "Bullet should be killed"
    print("  [PASS] Task 4: groupcollide() resolves collisions and removes hit sprites")

    print("\nAll Week 10 exercise checks passed successfully!")


# =============================================================================
# Interactive Game Loop
# =============================================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(380, 500)
    enemies = pygame.sprite.Group(Enemy(160, 180), Enemy(400, 120), Enemy(600, 220))
    collectibles = pygame.sprite.Group(Collectible(200, 350), Collectible(600, 350))
    bullets = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group(player)
    all_sprites.add(enemies)
    all_sprites.add(collectibles)

    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # TODO Task 3: Spawn bullet at player and add to both groups
                bullet = Bullet(player.rect.centerx - 4, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

        # TODO Task 4: Polymorphic Update — ZERO isinstance checks
        all_sprites.update(pygame.key.get_pressed())

        # TODO Task 4: Resolve Collisions with groupcollide
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for bullet, hit_enemies in hits.items():
            score += len(hit_enemies) * 10

        # Optional: Collectible collision
        collected = pygame.sprite.spritecollide(player, collectibles, True)
        score += len(collected) * 5

        # TODO Task 4: Polymorphic Render — ZERO isinstance checks
        screen.fill(BG)
        all_sprites.draw(screen)

        pygame.display.set_caption(
            f"Week 10 Arena | Score: {score} | Sprites: {len(all_sprites)} | Arrows: Move, SPACE: Shoot"
        )
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run automated verification checks")
    args = parser.parse_args()

    if args.check:
        run_checks()
    else:
        main()
