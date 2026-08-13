import pygame
import random

WIDTH, HEIGHT = 800, 600
BACKGROUND = "black" 
FPS = 300

class Ball:
    def __init__(self, x: int, y: int, radius: int, dx: int, dy: int, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = -self.dx
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.dx = -self.dx
 
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = -self.dy
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

def create_random_ball():
    radius = 10
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)
    dx = random.randint(1, 5) * random.choice([-1, 1])
    dy = random.randint(1, 5) * random.choice([-1, 1])
    color = random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)
    return Ball(x, y, radius, dx, dy, color)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           return False 
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Balls RGB")
    balls = tuple(create_random_ball() for _ in range(50))
    clock = pygame.time.Clock()
    running = True
    while running:
        running = handle_events()
        screen.fill(BACKGROUND)
        for ball in balls:
            ball.update()
            ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
