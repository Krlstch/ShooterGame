import math


class EnemyShooter:
    def __init__(self, x, y, observer):
        self.x = x
        self.y = y
        self.direct = 0
        self.speed = 4
        self.observer = observer
        self.size = 10
        observer.add_enemy(self)

    def update_pos(self, bullets):
        old_x = self.x
        old_y = self.y
        self.x += self.speed * math.cos(self.direct)
        self.y += self.speed * math.sin(self.direct)
        for bullet in bullets:
            if math.pow(bullet.x - self.x, 2) + math.pow(bullet.y - self.y, 2) < math.pow(self.size, 2):
                return bullet
            if math.pow(bullet.x - old_x, 2) + math.pow(bullet.y - old_y, 2) < math.pow(self.size, 2):
                return bullet
        return None

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