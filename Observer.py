import random
from Enemy import Enemy


class Observer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = set()
        self.enemies = set()
        self.char = None
        self.enemy_time = 0
        self.max_enemy_time = 120
        self.min_enemy_time = 60

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def add_char(self, char):
        self.char = char

    def add_enemy(self, enemy):
        self.enemies.add(enemy)

    def update_bullets(self):
        deleted_bullets = []
        for bullet in self.bullets:
            if not bullet.update_pos():
                deleted_bullets.append(bullet)
        for bullet in deleted_bullets:
            self.delete_bullet(bullet)

    def delete_bullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def update_enemies(self):
        deleted_enemies = []
        deleted_bullets = []
        for enemy in self.enemies:
            enemy.update_direction((self.char.x, self.char.y))
            hit_bullet = enemy.update_pos(self.bullets)
            if hit_bullet is not None:
                deleted_enemies.append(enemy)
                deleted_bullets.append(hit_bullet)
        for enemy in deleted_enemies:
            self.delete_enemies(enemy)
        for bullet in deleted_bullets:
            self.delete_bullet(bullet)

    def delete_enemies(self, enemy):
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
        enemy = Enemy(x, y, self)