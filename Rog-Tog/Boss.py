import pygame
import Enemy
import Bullet
import random

class BOSS(Enemy.ENEMY):
    def __init__(self, pos):
        super(BOSS, self).__init__(pos)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hp_max = 5000
        self.speed = 600
        self.dmg = 5
        self.time_to_shoot = pygame.time.get_ticks() + 100
        self.HP = self.hp_max
        self.bullet_shape = random.choice(["square", "circle", "triangle", "oval", "rectangle"])
        self.bullet_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def make_bullet(self, pos_pl, width, height):
        pos = pygame.math.Vector2(self.pos_bullet(width, height))

        bl = Bullet.BULLET(pos=pos, direct=(pos_pl - pos).normalize(), can_attack_player=True,
                           die_time=3000, dmg=15, shape=self.bullet_shape, color=self.bullet_color)
        return bl

    @staticmethod
    def pos_bullet(width, height):
        a = random.randint(1, 4)
        if a == 1:
            return [random.randint(0, width), -20]
        if a == 2:
            return [random.randint(0, width), height+20]
        if a == 3:
            return [-20, random.randint(0, height)]
        if a == 4:
            return [width+20, random.randint(0, height)]

    def make_bullet(self, pos_pl, width, height):
        # pos, direct, dmg, can_attack_player, die_time
        pos = pygame.math.Vector2(self.pos_bullet(width, height))

        bl = Bullet.BULLET(pos=pos, direct=(pos_pl - pos).normalize(), can_attack_player=True,
                           die_time=3000, dmg=15)
        return bl

    def update(self, delta, pos, group_item, group_bullet, width, height):
        if self.can_move():
            self.pos += self.move(pos) * delta * self.speed
            self.rect.center = self.pos

            if self.time_to_shoot < pygame.time.get_ticks():
                group_bullet.add(self.make_bullet(pos_pl=pos, width=width, height=height))
                self.time_to_shoot = pygame.time.get_ticks() + 95

        if self.HP < 0:
            self.kill()
