class Observer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = set()
        self.char = None

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def add_char(self, char):
        self.char = char

    def update_bullets(self):
        deleted_bullets = []
        for bullet in self.bullets:
            if not bullet.update_pos():
                deleted_bullets.append(bullet)
        for bullet in deleted_bullets:
            self.bullets.remove(bullet)
