import pygame.time
import Enemy
import Bullet
import Item
import random

class SHOOTENEMY(Enemy.ENEMY):
    def __init__(self, pos):
        super(SHOOTENEMY, self).__init__(pos)
        self.delay = pygame.time.get_ticks()
        self.tp = random.random() < .5
        self.tp_delay = pygame.time.get_ticks()
        self.type_shoot = random.randint(1, 3)
        self.bullet_shape = random.choice(["square", "circle", "triangle", "oval", "rectangle"])
        self.bullet_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def make_bullet(self, pos_pl, direct=None):
        if direct is None:
            if (pos_pl - self.pos).length() != 0:
                bl = Bullet.BULLET(pos=self.pos.copy(), direct=(pos_pl - self.pos).normalize(), can_attack_player=True,
                                   die_time=3000, dmg=15, shape=self.bullet_shape, color=self.bullet_color)
                return bl
        else:
            if direct.length != 0:
                bl = Bullet.BULLET(pos=self.pos.copy(), direct=direct, can_attack_player=True,
                                   die_time=3000, dmg=15, shape=self.bullet_shape, color=self.bullet_color)
                return bl
        return None

    def update(self, delta, pos, group_item, group_bullet, width, height):
        if self.can_move():
            if self.delay < pygame.time.get_ticks():
                if self.type_shoot == 1:
                    group_bullet.add(self.make_bullet(pos))
                elif self.type_shoot == 2:
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(1, 0)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(0, 1)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(0, -1)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(-1, 0)))
                elif self.type_shoot == 3:
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(1, 0)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(0, 1)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(0, -1)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(-1, 0)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(-1, -1)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(-1, 1)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(1, 1)))
                    group_bullet.add(self.make_bullet(pos, direct=pygame.Vector2(1, -1)))

                self.delay = pygame.time.get_ticks() + 500

                if self.tp and self.tp_delay < pygame.time.get_ticks():
                    self.tp_delay = pygame.time.get_ticks() + 2000
                    self.pos.x = random.randint(20, width-20)
                    self.pos.y = random.randint(20, height-20)
                    self.rect.center = self.pos
                    self.time_to_move = pygame.time.get_ticks() + 50

            if self.HP < 0:
                if random.random() < 0.1:
                    group_item.add(Item.ITEM(self.pos))
                self.kill()
