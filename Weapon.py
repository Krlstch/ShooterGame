class Weapon:
    def __init__(self, max_ammo, max_reload_time, max_delay, char):
        self.max_ammo = max_ammo
        self.ammo = max_ammo
        self.max_reload_time = max_reload_time
        self.reload_time = -1
        self.char = char
        self.char.add_weapon(self)
        self.max_delay = max_delay
        self.delay = 0

    def shoot(self):
        if self.ammo > 0 and self.reload_time == -1:
            if self.delay == 0:
                self.ammo -= 1
                self.delay = self.max_delay
                return 1
            else:
                return 0
        else:
            return self.reload()

    def reload(self):
        if self.reload_time == -1:
            self.reload_time = self.max_reload_time
            return -1
        return -2

    def update_reload_time(self):
        if self.delay > 0:
            self.delay -= 1

        if self.reload_time > 0:
            self.reload_time -= 1

        if self.reload_time == 0:
            self.reload_time = -1
            self.ammo = self.max_ammo
