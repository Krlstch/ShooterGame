import math


class EnemyGrunt:
    def __init__(self, x, y, observer):
        self.x = x
        self.y = y
        self.direct = 0
        self.speed = 1 + 0.1 * observer.difficulty
        self.observer = observer
        self.size = 10
        observer.add_enemy(self)

    def update_pos(self):
        self.x += self.speed * math.cos(self.direct)
        self.y += self.speed * math.sin(self.direct)

        if math.pow(self.x - self.observer.char.x, 2) + math.pow(self.y - self.observer.char.y, 2) < math.pow(self.observer.char.size + self.size, 2):
            return True
        else:
            return False

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


