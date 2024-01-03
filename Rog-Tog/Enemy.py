import random
import pygame
import Item


class ENEMY(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(ENEMY, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pygame.Vector2(self.rect.center)
        self.time_to_move = pygame.time.get_ticks() + 300
        self.speed = 400
        self.dmg = 10
        self.HP = 100

    def get_dmg(self, dmg):
        if self.can_move():
            self.HP -= dmg

    def move(self, pos):
        return (pos - self.pos).normalize()

    def can_move(self):
        return self.time_to_move < pygame.time.get_ticks()

    def update(self, delta, pos, group_item, group_bullet, width, height):
        if self.can_move():
            self.pos += self.move(pos) * delta * self.speed
            self.rect.center = self.pos
            if self.HP < 0:
                if random.random() < 0.1:
                    group_item.add(Item.ITEM(self.pos))
                self.kill()
