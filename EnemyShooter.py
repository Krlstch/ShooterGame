import math
import random
from EnemyBullet import EnemyBullet


class EnemyShooter:
    def __init__(self, x, y, observer):
        self.x = x
        self.y = y
        self.direct = 0
        self.speed = 0.5
        self.observer = observer
        self.size = 10
        self.type = random.choice([-1, 1])
        self.reload_time = 0
        self.max_reload_time = 300 - observer.difficulty * 10
        observer.add_enemy(self)

    def update_pos(self):
        if math.pow(self.x - self.observer.char.x, 2) + math.pow(self.y - self.observer.char.y, 2) > 160000 or \
                self.x < 20 or self.y < 20 or self.x > self.observer.x - 20 or self.y > self.observer.y - 20:
            # if further than 400 units from player or too close to border then walk toward player
            self.x += self.speed * math.cos(self.direct)
            self.y += self.speed * math.sin(self.direct)
        else:
            # else strafe
            self.x += self.speed * math.cos(self.direct + self.type * math.pi / 2)
            self.y += self.speed * math.sin(self.direct + self.type * math.pi / 2)
            if random.randint(1, 1000) == 1000:
                self.type = -self.type
        if self.reload_time == 0:
            self.shoot()
        else:
            self.reload_time -= 1

        # check if enemy is overlapping with char
        return math.pow(self.x - self.observer.char.x, 2) + math.pow(self.y - self.observer.char.y, 2) < \
               math.pow(self.observer.char.size + self.size, 2)

    def update_direction(self):
        if (self.observer.char.x, self.observer.char.y) == (self.x, self.y):
            pass
        elif self.observer.char.x > self.x:
            self.direct = math.asin(
                (self.observer.char.y - self.y) /
                math.sqrt(math.pow(self.observer.char.y - self.y, 2) + math.pow(self.observer.char.x - self.x, 2)))
        else:
            self.direct = math.pi - math.asin(
                (self.observer.char.y - self.y) /
                math.sqrt(math.pow(self.observer.char.y - self.y, 2) + math.pow(self.observer.char.x - self.x, 2)))

    def shoot(self):
        bullet = EnemyBullet(self.x, self.y, self.direct, self.observer)
        self.reload_time = self.max_reload_time
