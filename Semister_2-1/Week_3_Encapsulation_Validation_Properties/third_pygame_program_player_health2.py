import pygame

WIDTH = 640
HEIGHT = 480
FPS = 100

class Player:
    def __init__(self, x, y, max_health=100, speed=5):
        self._x = x
        self._y = y
        self._width = 30
        self._height = 30
        self._max_health = max_health
        self._health = max_health
        self._speed = speed

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, min(value, self._max_health))

    @property
    def max_health(self):
        return self._max_health

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value < 0:
            raise ValueError("Speed cannot be negative")
        self._speed = value

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def take_damage(self, amount):
        if amount < 0:
            raise ValueError("Damage cannot be negative")
        self.health -= amount

    def heal(self, amount):
        if amount < 0:
            raise ValueError("Heal cannot be negative")
        self.health += amount

    def move_left(self):
        self._x = max(0, self._x - self._speed)

    def move_right(self, screen_width):
        self._x = min(screen_width - self._width, self._x + self._speed)

    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 6
        bar_x = self._x + (self._width - bar_width) // 2
        bar_y = self._y - bar_height - 4

        ratio = self._health / self._max_health

        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        fill_rect = pygame.Rect(bar_x, bar_y, int(bar_width * ratio), bar_height)

        red = int(255 * (1 - ratio))
        green = int(255 * ratio)

        pygame.draw.rect(screen, (100, 0, 0), background_rect)
        pygame.draw.rect(screen, (red, green, 0), fill_rect)

    def draw(self, screen):
        player_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        pygame.draw.rect(screen, (40, 120, 220), player_rect)
        self.draw_health_bar(screen)

def handle_keydown(event, player):
    if event.key == pygame.K_d:
        player.take_damage(10)
    elif event.key == pygame.K_h:
        player.heal(10)

def handle_held_keys(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right(WIDTH)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Player Health Bar Game Test")
    clock = pygame.time.Clock()
    player = Player((WIDTH // 2) - 15, (HEIGHT // 2) - 15, speed=10)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, player)
        handle_held_keys(player)
        screen.fill((15, 15, 20))
        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
