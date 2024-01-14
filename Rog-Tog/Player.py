import pygame
import Bullet
from random import randint

pygame.init()


class PLAYER(pygame.sprite.Sprite):
    def __init__(self, pos, weapon):
        super(PLAYER, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.pos = pos
        self.speed = 500
        self.rect = self.image.get_rect()
        self.time_shoot = pygame.time.get_ticks() + 100
        self.max_hp = 100
        self.hp = self.max_hp
        self.time_hit = pygame.time.get_ticks()
        self.time_dash = 0
        self.weapon = weapon
        self.weapon1 = None
        self.use_weapon = 0
        self.spam_dash = True
        self.auto_shoot = True

    def live(self):
        return self.hp > 0

    def get_dmg(self, dmg):
        if self.time_hit < pygame.time.get_ticks():
            self.hp -= dmg
            self.time_hit = pygame.time.get_ticks() + 150
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    @staticmethod
    def move():
        direct = pygame.Vector2()
        press_key = pygame.key.get_pressed()

        if press_key[pygame.K_s] or press_key[1099]:
            direct.y = 1
        elif press_key[pygame.K_w] or press_key[1094]:
            direct.y = -1
        else:
            direct.y = 0

        if press_key[pygame.K_d] or press_key[1074]:
            direct.x = 1
        elif press_key[pygame.K_a] or press_key[1092]:
            direct.x = -1
        else:
            direct.x = 0

        if direct.length() != 0:
            return direct.normalize()
        return direct

    def change_weapon(self):
        press_key = pygame.key.get_pressed()

        if press_key[pygame.K_1]:
            self.use_weapon = 0
        if press_key[pygame.K_2] and self.weapon1:
            self.use_weapon = 1

    def get_active_weapon(self):
        if self.use_weapon:
            return self.weapon1
        else:
            return self.weapon

    def non_active_weapon(self):
        if self.use_weapon:
            return self.weapon
        else:
            return self.weapon1

    def pick_up_weapon(self, weapon):
        if self.weapon1 is None:
            self.weapon1 = weapon
            return

        c = self.get_active_weapon()

        if self.use_weapon:
            self.weapon1 = weapon
        else:
            self.weapon = weapon

        return c

    def make_bullet(self, wW, hH, PosM=None, direct=None):
        Pos = PosM
        directF = direct

        if Pos is None:
            Pos = pygame.mouse.get_pos()

        if direct is None:
            directF = pygame.Vector2(Pos[0] * wW, Pos[1] * hH) - self.pos

        if directF.length() != 0:
            return Bullet.BULLET(self.pos.copy(), directF.normalize(), self.get_active_weapon().dmg, False,
                                 die_time=self.get_active_weapon().die)

    def shoot(self, group, wW, hH):
        if self.get_active_weapon().type_shoot == 1:
            group.add(self.make_bullet(wW, hH))

        elif self.get_active_weapon().type_shoot == 2:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos()[0]*wW, pygame.mouse.get_pos()[1] * hH)
            pos_bullet = (mouse_pos - self.pos).normalize() * 200
            for i in range(3):
                x, y = randint(int(pos_bullet[0]-100), int(pos_bullet[0]+100)), randint(int(pos_bullet[1]-100), int(pos_bullet[1]+100))
                group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(x, y)))

        elif self.get_active_weapon().type_shoot == 3:
            group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(1, 0)))
            group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(0, 1)))
            group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(-1, 0)))
            group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(0, -1)))
            group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(1, 1)))
            group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(-1, -1)))
            group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(1, -1)))
            group.add(self.make_bullet(wW, hH, direct=pygame.Vector2(-1, 1)))

    def set_new_pos(self):
        self.pos = self.rect.center

    def stay_in_arena(self, width, height):
        if self.rect.left < 0:
            self.rect.left = 0
            self.set_new_pos()
        if self.rect.right > width:
            self.rect.right = width
            self.set_new_pos()
        if self.rect.top < 0:
            self.rect.top = 0
            self.set_new_pos()
        if self.rect.bottom > height:
            self.rect.bottom = height
            self.set_new_pos()

    def update(self, delta, bullet_group, width, height, width_m, height_m):
        if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_SPACE])\
                and self.time_dash < pygame.time.get_ticks() and self.spam_dash:
            self.pos += (self.move() * self.speed * delta * 11)
            self.time_dash = pygame.time.get_ticks() + 250
            self.time_hit = pygame.time.get_ticks() + 30
            self.spam_dash = False
        else:
            self.pos += (self.move() * self.speed * delta)

        self.change_weapon()

        if not pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.spam_dash = True

        if pygame.mouse.get_pressed()[0] and self.get_active_weapon().shoot() and self.auto_shoot:
            self.shoot(bullet_group, (width/width_m), (height/height_m))
            if not self.get_active_weapon().auto_shoot:
                self.auto_shoot = False

        if not pygame.mouse.get_pressed()[0]:
            self.auto_shoot = True

        self.rect.center = self.pos

        self.stay_in_arena(width, height)
