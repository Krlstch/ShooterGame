import math


class Bullet:
    def __init__(self, x, y, direct, observer):
        self.x = x
        self.y = y
        self.direct = direct
        self.speed = 20
        self.observer = observer
        observer.add_bullet(self)

    def update_pos(self):
        self.x += self.speed * math.cos(self.direct)
        self.y += self.speed * math.sin(self.direct)
        if self.x > self.observer.x or self.x < 0 or self.y > self.observer.y or self.y < 0:
            return False
        return True

