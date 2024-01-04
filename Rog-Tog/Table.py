import pygame
import Draw_windows


class TABLE(pygame.sprite.Sprite):
    def __init__(self, size, color, text, pos, font_size, command=None):
        super(TABLE, self).__init__()
        self.image = Draw_windows.DRAW().table(size, color, text, font_size)
        self.size = size
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.font_size = font_size
        self.command = command

    def change_color(self, color):
        self.image = Draw_windows.DRAW().table(self.size, color, self.text, self.font_size)

    def pos_in(self, pos):
        return self.rect.left < pos[0] < self.rect.right and self.rect.top < pos[1] < self.rect.bottom

    def do_click(self):
        if self.command:
            self.command()

    def update(self, mouse):
        if self.pos_in(mouse) and self.command:
            self.change_color((120, 120, 120))
            self.image = pygame.transform.scale(self.image, (self.size))
            self.rect = self.image.get_rect(center=(self.rect.center))
        else:
            self.change_color(self.color)
            self.image = pygame.transform.scale(self.image, (self.size))
            self.rect = self.image.get_rect(center=(self.rect.center))
