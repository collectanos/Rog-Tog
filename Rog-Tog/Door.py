import pygame


class DOOR(pygame.sprite.Sprite):
    def __init__(self, move, coord):
        super(DOOR, self).__init__()
        self.move_in_map = move
        self.image = pygame.Surface((40, 40))
        self.image.fill((84, 67, 41))
        self.rect = self.image.get_rect()
        self.rect.center = coord
        self.next_lvl = False
