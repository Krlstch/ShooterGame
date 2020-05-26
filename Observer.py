import random
from Char import Char
from EnemyShooter import EnemyShooter
from EnemyGrunt import EnemyGrunt


class Observer:
    def __init__(self, x, y):
        self.difficulty = 0
        self.x = x
        self.y = y
        self.bullets = set()
        self.enemies = set()
        self.char = None
        self.enemy_time = 0
        self.max_enemy_time = 40 + len(self.enemies) * 10 - self.difficulty * 5
        self.min_enemy_time = 20 + len(self.enemies) * 10 - self.difficulty * 5
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
            hit_target = bullet.update_pos(self.enemies)
            if hit_target is not None:
                deleted_bullets.append(bullet)
            if isinstance(hit_target, EnemyGrunt) or isinstance(hit_target, EnemyShooter):
                deleted_enemies.append(hit_target)
            if isinstance(hit_target, Char):
                self.game_over()
        for bullet in deleted_bullets:
            self.delete_bullet(bullet)
        for enemy in deleted_enemies:
            self.delete_enemy(enemy)

    def delete_bullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update_direction()
            hit = enemy.update_pos()
            if hit:
                self.game_over()

    def delete_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def update_spawn_time(self):
        if self.enemy_time > 0:
            self.enemy_time -= 1
        else:
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
        self.bullets = set()
        self.enemies = set()
        self.enemy_time = 0
