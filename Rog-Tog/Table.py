import pygame
import Draw_windows


class TABLE(pygame.sprite.Sprite):
    def __init__(self, size, color, text, pos, command=None):
        super(TABLE, self).__init__()
        self.image = Draw_windows.DRAW().table(size, color, text)
        self.size = size
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.command = command

    def change_color(self, color):
        self.image = Draw_windows.DRAW().table(self.size, color, self.text)

    def do_click(self):
        if self.command:
            self.command()
