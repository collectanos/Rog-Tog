import pygame

class WEAPON:
    def __init__(self, name="Pistol", race="green", delay=15, dmg=75, reload=20, type_shoot=1, bullet_per_clip=-1,
                 auto_shoot=False, count_clip=-1, die=1000, image="Data/img/Pistol.png", bullet_shape="square", bullet_color=None):
        self.name = name
        self.delay = delay
        self.reload = reload
        self.type_shoot = type_shoot
        self.dmg = dmg
        self.bullets_per_clip = bullet_per_clip
        self.count_clip = count_clip
        self.clip_now = self.bullets_per_clip
        self.image = pygame.image.load(image)
        self.race = race
        self.auto_shoot = auto_shoot
        self.die = die
        self.bullet_shape = bullet_shape
        self.bullet_color = bullet_color
        self.time_to_shoot = 0
        self.time_to_reload = 0


    def can_shoot(self):
        return self.time_to_shoot < pygame.time.get_ticks()

    def clip_have_ammo(self):
        return self.clip_now != 0

    def can_reload(self):
        return self.time_to_reload < pygame.time.get_ticks()

    def can_switch_clip(self):
        return self.count_clip != 0

    def reloading(self):
        self.clip_now = self.bullets_per_clip
        self.count_clip -= 1

    def shoot(self):
        if not self.clip_have_ammo():
            if self.can_reload() and self.can_switch_clip():
                self.reloading()
            return False

        if self.can_shoot():
            self.time_to_shoot = pygame.time.get_ticks() + self.delay
            self.clip_now -= 1
            if self.clip_now < 0:
                self.clip_now = -1

            if not self.clip_have_ammo():
                self.time_to_reload = pygame.time.get_ticks() + self.reload

            return True

        return False
