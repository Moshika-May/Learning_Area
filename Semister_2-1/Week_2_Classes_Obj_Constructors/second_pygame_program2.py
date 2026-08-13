import pygame
import random

WIDTH, HEIGHT = 800, 600
NUM_BALLS = 50
FPS = 50

class Ball:

    def __init__(self, x, y, radius, vx, vy, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx *= -1
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -1

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy *= -1
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), self.radius)


def create_random_ball():
    radius = 10
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)
    vx = random.choice([-1, 1]) * random.uniform(2, 4)
    vy = random.choice([-1, 1]) * random.uniform(2, 4)
    color = (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))
    return Ball(x, y, radius, vx, vy, color)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("50 Balls - OOP Refactor")
    clock = pygame.time.Clock()

    balls = [create_random_ball() for _ in range(NUM_BALLS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((20, 20, 30))

        for ball in balls:
            ball.update()
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
