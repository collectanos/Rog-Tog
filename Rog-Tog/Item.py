import pygame


class ITEM(pygame.sprite.Sprite):
    def __init__(self, pos, heal=20):
        super(ITEM, self).__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.heal = heal

    def pick_up_effect(self, pl):
        pl.get_dmg(-self.heal)
