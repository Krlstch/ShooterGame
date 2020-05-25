import math
from Bullet import Bullet


class Char:
    def __init__(self, observer):
        self.x = observer.x / 2
        self.y = observer.y / 2
        self.direct = 0
        self.speed = 5
        self.strafe_speed = 5
        self.back_speed = 2
        self.observer = observer
        self.reload_time = 0
        self.max_reload_time = 10
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
            self.x += self.speed * math.cos(self.direct)
            self.y += self.speed * math.sin(self.direct)

        if button == "s":
            self.x += self.back_speed * math.cos(self.direct + math.pi)
            self.y += self.back_speed * math.sin(self.direct + math.pi)

        if button == "a":
            self.x += self.strafe_speed * math.cos(self.direct - math.pi / 2)
            self.y += self.strafe_speed * math.sin(self.direct - math.pi / 2)

        if button == "d":
            self.x += self.strafe_speed * math.cos(self.direct + math.pi / 2)
            self.y += self.strafe_speed * math.sin(self.direct + math.pi / 2)

        if self.x < 0:
            self.x = 0

        if self.x > self.observer.x:
            self.x = self.observer.x

        if self.y < 0:
            self.y = 0

        if self.y > self.observer.y:
            self.y = self.observer.y

    def update_reload(self):
        if self.reload_time > 0:
            self.reload_time -= 1

    def shoot(self):
        if self.reload_time == 0:
            bullet = Bullet(self.x, self.y, self.direct, self.observer)
            self.reload_time = self.max_reload_time
