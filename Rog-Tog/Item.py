import pygame

class HealingItem(pygame.sprite.Sprite):
    def __init__(self, pos, heal=20):
        super(HealingItem, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))  # Белый фон
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.heal = heal
        self._draw_green_cross()

    def _draw_green_cross(self):
        pygame.draw.rect(self.image, (0, 255, 0), (8, 2, 4, 16))  # Вертикальная линия
        pygame.draw.rect(self.image, (0, 255, 0), (2, 8, 16, 4))  # Горизонтальная линия

    def pick_up_effect(self, player):
        player.get_dmg(-self.heal)
