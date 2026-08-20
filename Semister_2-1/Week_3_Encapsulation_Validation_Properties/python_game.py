for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d:
            player.take_damage(10)
        elif event.key == pygame.K_h:
            player.heal(10)

keys = pygame.key.get_pressed()
if key[pygame.K_LEFT]:
    player.move_left()
if ket[pygame.K_RIGHT]:
    player.move_right(WIDTH)
