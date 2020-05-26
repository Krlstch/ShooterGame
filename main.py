import math
import pygame
from Char import Char
from EnemyGrunt import EnemyGrunt
from EnemyShooter import EnemyShooter
from Observer import Observer


def draw(gameDisplay, char, bullets, enemies):
    gameDisplay.fill((0, 0, 0))
    player_sprite_rotated = pygame.transform.rotate(player_sprite, - char.direct * 180 / math.pi)
    gameDisplay.blit(player_sprite_rotated, (int(char.x) - 10, int(char.y) - 10))
    gameDisplay.blit(hud_screen, (0, observer.y))
    text_score = font.render('Score: ' + str(observer.score), True, (255, 0, 0))
    text_max_score = font.render('Best Score: ' + str(observer.max_score), True, (255, 0, 0))
    gameDisplay.blit(text_score, (10, observer.y + 10))
    gameDisplay.blit(text_max_score, (10, observer.y + 60))
    for bullet in bullets:
        pygame.draw.rect(gameDisplay, (255, 0, 0), (int(bullet.x), int(bullet.y), 3, 3))
    for enemy in enemies:
        if isinstance(enemy, EnemyGrunt):
            enemy_sprite_rotated = pygame.transform.rotate(enemy_grunt_sprite, - enemy.direct * 180 / math.pi)
        else:  # if isinstance(enemy, EnemyShooter):
            enemy_sprite_rotated = pygame.transform.rotate(enemy_shooter_sprite, - enemy.direct * 180 / math.pi)
        gameDisplay.blit(enemy_sprite_rotated, (int(enemy.x) - 10, int(enemy.y) - 10))
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
    try:
        file_best_score = open("Best Score.txt", "r")
    except FileNotFoundError:
        file_best_score = open("Best Score.txt", "w")
        file_best_score.close()
        file_best_score = open("Best Score.txt", "r")
    try:
        best_score = int(file_best_score.read())
    except ValueError:
        best_score = 0
    file_best_score.close()

    difficulty = {0: "Difficulty_veasy.png", 1: "Difficulty_easy.png", 2: "Difficulty_medium.png", 3: "Difficulty_hard.png", 4: "Difficulty_vhard.png"}
    observer = Observer(800, 600, best_score)
    pygame.init()
    gameDisplay = pygame.display.set_mode((observer.x, observer.y + 100))
    pygame.display.set_caption('Alien Shooter')
    play_screen = pygame.image.load('Start.png')
    game_over_screen = pygame.image.load('game_over.png')
    player_sprite = pygame.image.load('player.png')
    enemy_grunt_sprite = pygame.image.load('EnemyGrunt.png')
    enemy_shooter_sprite = pygame.image.load('EnemyShooter.png')
    hud_screen = pygame.image.load('Hud.png')
    difficulty_screen = pygame.image.load(difficulty[observer.difficulty])
    char = Char(observer)
    font = pygame.font.SysFont("Arial", 32)
    font_large = pygame.font.SysFont("Arial", 64)
    run = True

    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN or \
                    event.type == pygame.KEYDOWN:
                if observer.game_state == 0:
                    if 260 < pygame.mouse.get_pos()[0] < 469 and 193 < pygame.mouse.get_pos()[1] < 256:  # start
                        observer.game_state = 1
                    elif 260 < pygame.mouse.get_pos()[0] < 469 and 358 < pygame.mouse.get_pos()[1] < 418:  # end
                        run = False
                    elif 260 < pygame.mouse.get_pos()[0] < 469 and 276 < pygame.mouse.get_pos()[1] < 336:  # difficulty
                        observer.difficulty = (observer.difficulty + 1) % 5
                        difficulty_screen = pygame.image.load(difficulty[observer.difficulty])
                if observer.game_state == 2:
                    observer.game_state = 0

        if observer.game_state == 0:
            gameDisplay.blit(play_screen, (0, 0))
            gameDisplay.blit(difficulty_screen, (260, 276))
            pygame.display.update()

        elif observer.game_state == 1:
            take_input()
            spawn_enemy(observer)
            update(char, observer)
            draw(gameDisplay, char, observer.bullets, observer.enemies)

        else:
            gameDisplay.fill((0, 0, 0))
            text_game_over = font_large.render('You Died', True, (255, 0, 0))
            gameDisplay.blit(text_game_over, (observer.x / 2 - 64 * 3, observer.y / 2 - 64))
            text_game_over = font.render('Score: ' + str(observer.old_score), True, (255, 0, 0))
            gameDisplay.blit(text_game_over, (observer.x / 2 - 64 * 2, observer.y / 2 + 16))
            text_game_over = font.render('Best Score: ' + str(observer.max_score), True, (255, 0, 0))
            gameDisplay.blit(text_game_over, (observer.x / 2 - 32 * 5, observer.y / 2 + 80))
            if observer.new_record:
                text_game_over = font.render('New Record !', True, (255, 0, 0))
                gameDisplay.blit(text_game_over, (observer.x / 2 - 16 * 9, observer.y / 2 + 144))
            pygame.display.update()

    pygame.quit()
    quit()
