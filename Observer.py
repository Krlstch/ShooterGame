import random
from EnemyGrunt import EnemyGrunt


class Observer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = set()
        self.enemies = set()
        self.char = None
        self.enemy_time = 0
        self.max_enemy_time = 20
        self.min_enemy_time = 1

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
            if isinstance(hit_target, EnemyGrunt):
                deleted_enemies.append(hit_target)
        for bullet in deleted_bullets:
            self.delete_bullet(bullet)
        for enemy in deleted_enemies:
            self.delete_enemy(enemy)

    def delete_bullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update_direction((self.char.x, self.char.y))
            enemy.update_pos()

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
        enemy = EnemyGrunt(x, y, self)
