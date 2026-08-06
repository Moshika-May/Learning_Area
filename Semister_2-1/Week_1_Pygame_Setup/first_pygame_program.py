import  pygame
import  random

WIDTH, HEIGHT = 800, 600
BACKGROUND = "black"
BALL_COLOR = "white"
FPS = 300
balls = []

for _ in range(50):
    radius = random.randint(10, 20)
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)
    dx = random.randint(1, 5) * random.choice([-1, 1])
    dy = random.randint(1, 5) * random.choice([-1, 1])
    balls.append({
        "x": x,
        "y": y,
        "dx": dx,
        "dy": dy,
        "radius": radius
    })

def handle_events():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
    return True

def update_ball():
    for ball in balls:
        ball["x"] += ball["dx"]
        ball["y"] += ball["dy"]
        if (ball["x"] - ball["radius"] <= 0):
            ball["x"] = ball["radius"]
            ball["dx"] = -ball["dx"]
        elif (ball["x"] + ball["radius"] >= WIDTH):
            ball["x"] = WIDTH - ball["radius"]
            ball["dx"] = -ball["dx"]
        if (ball["y"] - ball["radius"] <= 0):
            ball["y"] = ball["radius"]
            ball["dy"] = -ball["dy"]
        elif (ball["y"] + ball["radius"] >= HEIGHT):
            ball["y"] = HEIGHT - ball["radius"]
            ball["dy"] = -ball["dy"]

def draw(screen):
    screen.fill(BACKGROUND)
    for ball in balls:
        pygame.draw.circle(screen, BALL_COLOR, (ball["x"], ball["y"]), ball["radius"])
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball")
    clock = pygame.time.Clock()
    running = True
    while (running):
        running = handle_events()
        update_ball()
        draw(screen)
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
