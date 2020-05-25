import pygame
from Char import Char

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Alien Shooter')

char = Char()

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        char.update_position("w")

    if keys[pygame.K_s]:
        char.update_position("s")

    if keys[pygame.K_a]:
        char.update_position("a")

    if keys[pygame.K_d]:
        char.update_position("d")

    char.update_direction(pygame.mouse.get_pos())

    gameDisplay.fill((0, 0, 0))
    pygame.draw.rect(gameDisplay, (255, 0, 0), (char.x, char.y, 10, 10))
    pygame.display.update()

pygame.quit()
quit()
