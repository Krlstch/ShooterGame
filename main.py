import math
import pygame

from Weapon import Weapon
from Char import Char
from EnemyGrunt import EnemyGrunt
from EnemyShooter import EnemyShooter
from Observer import Observer
import time


def draw(gameDisplay, char, weapon, bullets, enemies):
    gameDisplay.fill((0, 0, 0))
    player_sprite_rotated = pygame.transform.rotate(player_sprite, - char.direct * 180 / math.pi)
    gameDisplay.blit(player_sprite_rotated, (int(char.x) - 10, int(char.y) - 10))
    for bullet in bullets:
        pygame.draw.rect(gameDisplay, (255, 0, 0), (int(bullet.x), int(bullet.y), 3, 3))
    for enemy in enemies:
        if isinstance(enemy, EnemyGrunt):
            enemy_sprite_rotated = pygame.transform.rotate(enemy_grunt_sprite, - enemy.direct * 180 / math.pi)
        else:  # if isinstance(enemy, EnemyShooter):
            enemy_sprite_rotated = pygame.transform.rotate(enemy_shooter_sprite, - enemy.direct * 180 / math.pi)
        gameDisplay.blit(enemy_sprite_rotated, (int(enemy.x) - 10, int(enemy.y) - 10))
    gameDisplay.blit(hud_screen, (0, observer.y))
    text_score = font.render('Score: ' + str(observer.score), True, (255, 0, 0))
    text_max_score = font.render('Best Score: ' + str(observer.max_score), True, (255, 0, 0))
    gameDisplay.blit(text_score, (10, observer.y + 10))
    gameDisplay.blit(text_max_score, (10, observer.y + 60))
    pygame.draw.rect(gameDisplay, (127, 127, 127), (observer.x - 210, observer.y + 60, 200, 20))
    pygame.draw.rect(gameDisplay, (175, 175, 175), (observer.x - 208, observer.y + 62, 196, 16))
    if weapon.reload_time == -1:
        pygame.draw.rect(gameDisplay, (255, 0, 0),
                         (observer.x - 208, observer.y + 62, 196 * (weapon.ammo / weapon.max_ammo), 16))
    else:
        pygame.draw.rect(gameDisplay, (255, 0, 0),
                         (observer.x - 208, observer.y + 62, 196 * (weapon.reload_time / weapon.max_reload_time), 16))

    pygame.display.update()


def update(char, observer, weapon):
    char.update_direction(pygame.mouse.get_pos())
    weapon.update_reload_time()
    observer.update_bullets()
    observer.update_enemies()


def spawn_enemy(observer):
    observer.update_spawn_time()


def take_input(lmb_pressed):
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

    if keys[pygame.K_r]:
        if char.weapon.reload() == -1:
            reload_sound.play()

    if mouse[0]:
        if not lmb_pressed:
            shoot = char.shoot()
            if shoot == 1:
                shoot_sound.play()
            if shoot == -1:
                reload_sound.play()
            lmb_pressed = True
    else:
        lmb_pressed = False

    return lmb_pressed


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

    difficulty = {0: "images/Difficulty_veasy.png", 1: "images/Difficulty_easy.png", 2: "images/Difficulty_medium.png",
                  3: "images/Difficulty_hard.png", 4: "images/Difficulty_vhard.png"}
    observer = Observer(800, 600, best_score)
    char = Char(observer)
    weapon = Weapon(7, 120, 30, char)
    pygame.init()

    gameDisplay = pygame.display.set_mode((observer.x, observer.y + 100))
    shoot_sound = pygame.mixer.Sound('sound/shoot.wav')
    reload_sound = pygame.mixer.Sound('sound/reload.wav')
    pygame.display.set_caption('Alien Shooter')
    play_screen = pygame.image.load('images/Start.png')
    game_over_screen = pygame.image.load('images/game_over.png')
    player_sprite = pygame.image.load('images/player.png')
    enemy_grunt_sprite = pygame.image.load('images/EnemyGrunt.png')
    enemy_shooter_sprite = pygame.image.load('images/EnemyShooter.png')
    hud_screen = pygame.image.load('images/Hud.png')
    difficulty_screen = pygame.image.load(difficulty[observer.difficulty])

    font = pygame.font.SysFont("Arial", 32)
    font_large = pygame.font.SysFont("Arial", 128)
    run = True
    target_fps = 60
    prev_time = time.time()
    lmb_pressed = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN or \
                    event.type == pygame.KEYDOWN:
                if observer.game_state == 0:
                    if 295 < pygame.mouse.get_pos()[0] < 504 and 193 < pygame.mouse.get_pos()[1] < 256:  # start
                        observer.game_state = 1
                    elif 295 < pygame.mouse.get_pos()[0] < 504 and 358 < pygame.mouse.get_pos()[1] < 418:  # end
                        run = False
                    elif 295 < pygame.mouse.get_pos()[0] < 504 and 276 < pygame.mouse.get_pos()[1] < 336:  # difficulty
                        observer.difficulty = (observer.difficulty + 1) % 5
                        difficulty_screen = pygame.image.load(difficulty[observer.difficulty])
                if observer.game_state == 2:
                    observer.game_state = 0

        if observer.game_state == 0:
            lmb_pressed = True
            observer.new_record = False
            char.x = observer.x / 2
            char.y = observer.y / 2
            weapon.ammo = weapon.max_ammo
            weapon.reload_time = -1
            weapon.delay = 0
            gameDisplay.fill((0, 0, 0))
            gameDisplay.blit(play_screen, (0, 0))
            gameDisplay.blit(difficulty_screen, (295, 276))
            pygame.display.update()

        elif observer.game_state == 1:
            lmb_pressed = take_input(lmb_pressed)
            spawn_enemy(observer)
            update(char, observer, weapon)
            draw(gameDisplay, char, weapon, observer.bullets, observer.enemies)

        else:
            gameDisplay.fill((0, 0, 0))
            text_game_over = font_large.render('You Died', True, (255, 0, 0))
            gameDisplay.blit(text_game_over, (observer.x / 2 - 32 * 8, observer.y / 2 - 32 * 5))
            text_game_over = font.render('Score: ' + str(observer.old_score), True, (255, 0, 0))
            gameDisplay.blit(text_game_over, (observer.x / 2 - 64 * 1, observer.y / 2 + 16))
            text_game_over = font.render('Best Score: ' + str(observer.max_score), True, (255, 0, 0))
            gameDisplay.blit(text_game_over, (observer.x / 2 - 16 * 4, observer.y / 2 + 80))
            if observer.new_record:
                text_game_over = font.render('New Record !', True, (255, 0, 0))
                gameDisplay.blit(text_game_over, (observer.x / 2 - 16 * 4, observer.y / 2 + 144))
            pygame.display.update()

        curr_time = time.time()
        diff = curr_time - prev_time
        delay = max(1.0 / target_fps - diff, 0)
        time.sleep(delay)
        fps = 1.0 / (delay + diff)
        prev_time = curr_time

    pygame.quit()
    quit()
