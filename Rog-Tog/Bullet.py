import pygame


class BULLET(pygame.sprite.Sprite):
    def __init__(self, pos, direct, dmg, can_attack_player, die_time):
        super(BULLET, self).__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        if can_attack_player:
            self.speed = 500
        else:
            self.image.fill((227, 168, 20))
            self.speed = 1000
        self.pos = pos
        self.direct = direct
        self.dmg = dmg
        self.can_attack_player = can_attack_player
        self.die_time = die_time + pygame.time.get_ticks()

    def update(self, delta):
        if self.die_time < pygame.time.get_ticks():
            self.kill()

        self.pos += self.direct * self.speed * delta

        self.rect.center = self.pos
