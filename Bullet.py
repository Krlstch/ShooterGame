import math


class Bullet:
    def __init__(self, x, y, direct, observer):
        self.x = x
        self.y = y
        self.direct = direct
        self.speed = 3
        self.observer = observer
        observer.add_bullet(self)

    def update_pos(self, enemies):
        old_x = self.x
        old_y = self.y
        self.x += self.speed * math.cos(self.direct)
        self.y += self.speed * math.sin(self.direct)
        if self.x > self.observer.x or self.x < 0 or self.y > self.observer.y or self.y < 0:
            return 0  # hit wall

        for enemy in enemies:
            if math.pow(self.x - enemy.x, 2) + math.pow(self.y - enemy.y, 2) < math.pow(enemy.size, 2) or \
                    math.pow(old_x - enemy.x, 2) + math.pow(old_y - enemy.y, 2) < math.pow(enemy.size, 2):
                return enemy
        return None
