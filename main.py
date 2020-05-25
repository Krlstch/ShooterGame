import pygame
from Char import Char
from Observer import Observer
from Enemy import Enemy


def draw(gameDisplay, char, bullets, enemies):
    gameDisplay.fill((0, 0, 0))
    pygame.draw.circle(gameDisplay, (0, 255, 0), (int(char.x), int(char.y)), 10, 10)
    for bullet in bullets:
        pygame.draw.rect(gameDisplay, (255, 0, 0), (int(bullet.x), int(bullet.y), 1, 1))
    for enemy in enemies:
        pygame.draw.circle(gameDisplay, (255, 0, 0), (int(enemy.x), int(enemy.y)), 10, 10)
    pygame.display.update()


def update(char, observer):
    char.update_direction(pygame.mouse.get_pos())
    char.update_reload()
    observer.update_bullets()
    observer.update_enemies()


def spawn_enemy(observer):
    observer.update_spawn_time()


def take_input():
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


if __name__ == "__main__":
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

        take_input()
        spawn_enemy(observer)
        update(char, observer)
        draw(gameDisplay, char, observer.bullets, observer.enemies)

    pygame.quit()
    quit()
