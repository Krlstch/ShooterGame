import random
from Char import Char
from EnemyShooter import EnemyShooter
from EnemyGrunt import EnemyGrunt


class Observer:
    def __init__(self, x, y, best_score):
        self.score = 0
        self.old_score = 0
        self.new_record = False
        self.max_score = best_score
        self.difficulty = 0
        self.x = x
        self.y = y
        self.bullets = set()
        self.enemies = set()
        self.char = None
        self.enemy_time = 0
        self.max_enemy_time = 300 + len(self.enemies) * 10 - self.difficulty * 15  # max time between spawning enemies
        self.min_enemy_time = max(len(self.enemies) * 15 - self.difficulty * 5, 0)  # min time between spawning enemies
        self.game_state = 0  # 0 - game hasn't started, 1 - game has started, 2 - game is over

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def add_char(self, char):
        self.char = char

    def add_enemy(self, enemy):
        self.enemies.add(enemy)

    def update_bullets(self):
        deleted_bullets = []
        deleted_enemies = []
        for bullet in self.bullets:
            hit_target = bullet.update_pos(self.enemies)  #check if bullet hit anything
            if hit_target is not None:  #if it hit anything set it to be removed
                deleted_bullets.append(bullet)
            if isinstance(hit_target, EnemyGrunt) or isinstance(hit_target, EnemyShooter):
                # if it hit enemy set it to be destroyed
                deleted_enemies.append(hit_target)
            if isinstance(hit_target, Char):
                self.game_over()
        for bullet in deleted_bullets:  # delete bullets which were set to be destroyed
            self.delete_bullet(bullet)
        for enemy in deleted_enemies:  # delete enemies which were set to be destroyed
            self.delete_enemy(enemy)

    def delete_bullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update_direction()
            if enemy.update_pos():  # if enemy collided with char
                self.game_over()

    def delete_enemy(self, enemy):
        # remove enemy and update the score
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            self.score += 100 + self.difficulty * 20

    def update_spawn_time(self):
        if self.enemy_time > 0:
            self.enemy_time -= 1
        else:
            # if time has come spawn an enemy and set new spawn time from [min_enemy_time, max_enemy_time]
            self.spawn_enemy()
            self.enemy_time = random.randint(self.min_enemy_time, self.max_enemy_time)

    def spawn_enemy(self):
        x = random.choice([0, self.x])
        y = random.choice([0, self.y])
        enemy_type = random.randint(1, 100)
        if enemy_type <= 30:
            enemy = EnemyShooter(x, y, self)
        else:
            enemy = EnemyGrunt(x, y, self)

    def game_over(self):
        self.game_state = 2  #game over
        # reset variables
        self.bullets = set()
        self.enemies = set()
        self.enemy_time = 0
        self.old_score = self.score
        if self.score > self.max_score:  # check if new record has been set
            self.max_score = self.score
            self.new_record = True
            file_best_score = open("Best Score.txt", "w")
            file_best_score.write(str(self.max_score))
            file_best_score.close()
        self.score = 0
