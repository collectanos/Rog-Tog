import pygame

class BULLET(pygame.sprite.Sprite):
    def __init__(self, pos, direct, dmg, can_attack_player, die_time, shape="square", color=None):
        super(BULLET, self).__init__()
        
        sizes = {
            "square": (5, 5),
            "circle": (6, 6), 
            "triangle": (7, 7),
            "oval": (8, 4),
            "rectangle": (8, 3)
        }
        
        size = sizes.get(shape, (5, 5))
        self.image = pygame.Surface(size)
        
        if color is None:
            color = (255, 0, 0) if can_attack_player else (227, 168, 20)
        
        if shape == "square":
            self.image.fill(color)
        elif shape == "circle":
            self.image.fill((0,0,0))
            self.image.set_colorkey((0,0,0))
            pygame.draw.circle(self.image, color, (size[0]//2, size[1]//2), min(size[0], size[1])//2)
        elif shape == "triangle":
            self.image.fill((0,0,0))
            self.image.set_colorkey((0,0,0))
            points = [(0, size[1]), (size[0]//2, 0), (size[0], size[1])]
            pygame.draw.polygon(self.image, color, points)
        elif shape == "oval":
            self.image.fill((0,0,0))
            self.image.set_colorkey((0,0,0))
            pygame.draw.ellipse(self.image, color, (0, 0, size[0], size[1]))
        elif shape == "rectangle":
            self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 500 if can_attack_player else 1000
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