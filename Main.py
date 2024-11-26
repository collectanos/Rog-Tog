import pygame
import MainGame
import MainMenu
import time
from GLOBALS import FPS, WIDTH, HEIGHT, WIDTH_M, HEIGHT_M


pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Simple Roughlike Game")
display = pygame.display.set_mode((WIDTH_M, HEIGHT_M), pygame.RESIZABLE)
delta = 1
while True:
    time_now = time.time()
    while MainMenu.game_status == "Play":
        time_now = time.time()

        screen, WIDTH, HEIGHT = MainGame.update(delta, WIDTH, HEIGHT)

        display.blit(screen, (0, 0))

        pygame.display.flip()
        delta = time.time() - time_now

    screen, WIDTH, HEIGHT = MainMenu.update(delta, WIDTH, HEIGHT)
    display.blit(screen, (0, 0))
    pygame.display.flip()
    delta = time.time() - time_now
