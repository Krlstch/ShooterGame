import math


class EnemyGrunt:
    def __init__(self, x, y, observer):
        self.x = x
        self.y = y
        self.direct = 0
        self.speed = 3
        self.observer = observer
        self.size = 10
        observer.add_enemy(self)

    def update_pos(self):
        self.x += self.speed * math.cos(self.direct)
        self.y += self.speed * math.sin(self.direct)

    def update_direction(self, char_pos):
        if char_pos == (self.x, self.y):
            pass
        elif char_pos[0] > self.x:
            self.direct = math.asin(
                (char_pos[1] - self.y) /
                math.sqrt(math.pow(char_pos[1] - self.y, 2) + math.pow(char_pos[0] - self.x, 2)))
        else:
            self.direct = math.pi - math.asin(
                (char_pos[1] - self.y) /
                math.sqrt(math.pow(char_pos[1] - self.y, 2) + math.pow(char_pos[0] - self.x, 2)))