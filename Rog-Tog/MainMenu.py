import pygame
import Table
from GLOBALS import FPS, WIDTH, HEIGHT, WIDTH_M, HEIGHT_M

pygame.init()

game_status = "Menu"

mouse_click = True

Ww, Hh, = WIDTH / WIDTH_M, HEIGHT / HEIGHT_M

screen = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()

group_button = pygame.sprite.Group()
group_text = pygame.sprite.Group()

mouse_surf = pygame.Surface((5, 5))
mouse_surf.fill((255, 255, 255))


def start_game():
    global game_status
    game_status = "Play"


def quit_from_game():
    pygame.quit()
    quit()


TileGame = Table.TABLE((230, 20), (50, 50, 50), "SIMPLE ROUGHLIKE GAME", (WIDTH // 3+120, 300))
TileGame.image = pygame.transform.scale(TileGame.image, (460, 50))
TileGame.rect = TileGame.image.get_rect(center=(TileGame.rect.center))
group_text.add(TileGame)

TileGame = Table.TABLE((230, 20), (90, 90, 90), "Play", (WIDTH // 3+120, 400), start_game)
TileGame.image = pygame.transform.scale(TileGame.image, (460, 50))
TileGame.rect = TileGame.image.get_rect(center=(TileGame.rect.center))
group_button.add(TileGame)

TileGame = Table.TABLE((230, 20), (90, 90, 90), "Quit", (WIDTH // 3+120, 500), quit_from_game)
TileGame.image = pygame.transform.scale(TileGame.image, (460, 50))
TileGame.rect = TileGame.image.get_rect(center=(TileGame.rect.center))
group_button.add(TileGame)


def mouse_pos_get():
    Mpos = pygame.mouse.get_pos()
    Mpos = (Mpos[0] * Ww, Mpos[1] * Hh)
    return Mpos


def pos_inside(pos, rect):
    return rect.left < pos[0] < rect.right and rect.top < pos[1] < rect.bottom


def update():
    global mouse_surf, mouse_click, game_status
    clock.tick(FPS)

    mouse = mouse_pos_get()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN and mouse_click:
            mouse_click = False
            mouse = mouse_pos_get()

            for btn in group_button:
                if pos_inside(mouse, btn.rect):
                    btn.do_click()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = True

    for btn in group_button:
        if pos_inside(mouse, btn.rect):
            btn.change_color((120, 120, 120))
            btn.image = pygame.transform.scale(btn.image, (460, 50))
            btn.rect = btn.image.get_rect(center=(btn.rect.center))
        else:
            btn.change_color((90, 90, 90))
            btn.image = pygame.transform.scale(btn.image, (460, 50))
            btn.rect = TileGame.image.get_rect(center=(btn.rect.center))

    screen.fill((50, 50, 50))
    group_button.draw(screen)
    group_text.draw(screen)
    screen.blit(mouse_surf, mouse)

    return screen
