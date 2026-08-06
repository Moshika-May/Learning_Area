import  pygame

WIDTH, HEIGHT = 800, 600
BACKGROUND = "black"
BALL_COLOR = "white"
FPS = 300
x = 350
y = 250
dx = 12
dy = 9
radius = 20

def handle_events():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
    return True

def update_ball():
    global x, y, dx, dy
    x += dx
    y += dy
    if (x - radius <= 0 or x + radius >= WIDTH):
        dx = -dx
    if (y - radius <= 0 or y + radius >= HEIGHT):
        dy = -dy

def draw(screen):
    screen.fill(BACKGROUND)
    pygame.draw.circle(screen, BALL_COLOR, (x, y), radius)
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
