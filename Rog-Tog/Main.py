import pygame
import MainGame
import MainMenu
import time
from GLOBALS import FPS, WIDTH, HEIGHT, WIDTH_M, HEIGHT_M


pygame.init()

pygame.display.set_caption("Simple Roughlike Game")
display = pygame.display.set_mode((WIDTH_M, HEIGHT_M))
delta = 1

while True:

    while MainMenu.game_status == "Play":
        time_now = time.time()
        screen = MainGame.update(delta)
        display.blit(pygame.transform.scale(screen, (WIDTH_M, HEIGHT_M)), (0, 0))

        pygame.display.flip()
        delta = time.time() - time_now

    screen = MainMenu.update()
    display.blit(pygame.transform.scale(screen, (WIDTH_M, HEIGHT_M)), (0, 0))
    pygame.display.flip()
