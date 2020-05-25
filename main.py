import pygame
from Char import Char
from Observer import Observer

observer = Observer(800, 600)
pygame.init()
gameDisplay = pygame.display.set_mode((observer.x, observer.y))
pygame.display.set_caption('Alien Shooter')

char = Char(observer)

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    if keys[pygame.K_w]:
        char.update_position("w")

    if keys[pygame.K_s]:
        char.update_position("s")

    if keys[pygame.K_a]:
        char.update_position("a")

    if keys[pygame.K_d]:
        char.update_position("d")

    if mouse[0]:
        char.shoot()

    char.update_direction(pygame.mouse.get_pos())
    char.update_reload()
    observer.update_bullets()

    gameDisplay.fill((0, 0, 0))

    pygame.draw.rect(gameDisplay, (0, 255, 0), (char.x, char.y, 10, 10))
    for bullet in observer.bullets:
        pygame.draw.rect(gameDisplay, (255, 0, 0), (bullet.x, bullet.y, 1, 1))
    pygame.display.update()

pygame.quit()
quit()
