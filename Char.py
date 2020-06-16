import math
from Bullet import Bullet


class Char:
    def __init__(self, observer):
        self.x = observer.x / 2
        self.y = observer.y / 2
        self.direct = 0
        self.speed = 0.8
        self.observer = observer
        self.size = 10
        self.weapon = None
        observer.add_char(self)

    def update_direction(self, cursor_pos):
        if cursor_pos == (self.x, self.y):
            pass
        elif cursor_pos[0] > self.x:
            self.direct = math.asin(
                (cursor_pos[1] - self.y) /
                math.sqrt(math.pow(cursor_pos[1] - self.y, 2) + math.pow(cursor_pos[0] - self.x, 2)))
        else:
            self.direct = math.pi - math.asin(
                (cursor_pos[1] - self.y) /
                math.sqrt(math.pow(cursor_pos[1] - self.y, 2) + math.pow(cursor_pos[0] - self.x, 2)))

    def update_position(self, button):
        if button == "w":
            self.y -= self.speed

        if button == "s":
            self.y += self.speed

        if button == "a":
            self.x -= self.speed

        if button == "d":
            self.x += self.speed

        # Deal with borders
        if self.x < 0:
            self.x = 0

        if self.x > self.observer.x:
            self.x = self.observer.x

        if self.y < 0:
            self.y = 0

        if self.y > self.observer.y:
            self.y = self.observer.y

    def shoot(self):
        shoot = self.weapon.shoot()  # check if weapon can shoot
        if shoot == 1:
            bullet = Bullet(self.x, self.y, self.direct, self.observer)
        return shoot

    def add_weapon(self, weapon):
        self.weapon = weapon
