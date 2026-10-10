"""
Question 1 Starter: Procedural Pulsing Balls (40 points)

This file contains a working procedural Pygame script that animates three balls
pulsing (growing and shrinking) between given minimum and maximum radii.

Your task:
Refactor this procedural implementation into clean Object-Oriented code:
1. Encapsulate ball state into a `PulsingBall` class.
2. Protect all internal state with leading underscores and provide read-only @property getters.
3. Implement `update()` (to grow/shrink and bounce between min and max radii) and `draw(screen)`.
4. Rewrite the main loop to use a list of `PulsingBall` instances.
"""

import sys
import pygame

# Constants & Configurations
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

COLOR_BG = (30, 30, 40)
COLOR_GUIDE = (60, 60, 75)
COLOR_GREEN = (50, 200, 80)
COLOR_YELLOW = (240, 210, 40)
COLOR_CYAN = (40, 210, 210)

# State for Ball 1
b1_x = 150.0
b1_y = 300.0
b1_radius = 30.0
b1_min_radius = 15.0
b1_max_radius = 60.0
b1_color = COLOR_GREEN
b1_growth_speed = 1.0
b1_dir = 1  # 1 = growing, -1 = shrinking

# State for Ball 2
b2_x = 300.0
b2_y = 300.0
b2_radius = 50.0
b2_min_radius = 20.0
b2_max_radius = 80.0
b2_color = COLOR_YELLOW
b2_growth_speed = 1.5
b2_dir = -1

# State for Ball 3
b3_x = 450.0
b3_y = 300.0
b3_radius = 25.0
b3_min_radius = 10.0
b3_max_radius = 50.0
b3_color = COLOR_CYAN
b3_growth_speed = 0.8
b3_dir = 1


def main():
    global b1_radius, b1_dir, b2_radius, b2_dir, b3_radius, b3_dir

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Q1 Starter: Procedural Pulsing Balls")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- UPDATE BALL 1 ---
        b1_radius += b1_growth_speed * b1_dir
        if b1_radius <= b1_min_radius:
            b1_radius = b1_min_radius
            b1_dir = 1
        elif b1_radius >= b1_max_radius:
            b1_radius = b1_max_radius
            b1_dir = -1

        # --- UPDATE BALL 2 ---
        b2_radius += b2_growth_speed * b2_dir
        if b2_radius <= b2_min_radius:
            b2_radius = b2_min_radius
            b2_dir = 1
        elif b2_radius >= b2_max_radius:
            b2_radius = b2_max_radius
            b2_dir = -1

        # --- UPDATE BALL 3 ---
        b3_radius += b3_growth_speed * b3_dir
        if b3_radius <= b3_min_radius:
            b3_radius = b3_min_radius
            b3_dir = 1
        elif b3_radius >= b3_max_radius:
            b3_radius = b3_max_radius
            b3_dir = -1

        # --- DRAW ---
        screen.fill(COLOR_BG)

        # Draw outer boundary guides (max radius)
        pygame.draw.circle(screen, COLOR_GUIDE, (int(b1_x), int(b1_y)), int(b1_max_radius), 1)
        pygame.draw.circle(screen, COLOR_GUIDE, (int(b2_x), int(b2_y)), int(b2_max_radius), 1)
        pygame.draw.circle(screen, COLOR_GUIDE, (int(b3_x), int(b3_y)), int(b3_max_radius), 1)

        # Draw balls
        pygame.draw.circle(screen, b1_color, (int(b1_x), int(b1_y)), int(b1_radius))
        pygame.draw.circle(screen, b2_color, (int(b2_x), int(b2_y)), int(b2_radius))
        pygame.draw.circle(screen, b3_color, (int(b3_x), int(b3_y)), int(b3_radius))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
