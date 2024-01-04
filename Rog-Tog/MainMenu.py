import pygame
import Table
from GLOBALS import FPS, WIDTH, HEIGHT, WIDTH_M, HEIGHT_M
import os
from mod_cell import ModCell
import json
import GLOBALS

pygame.init()

game_status = "Menu"

menu_status = "Menu"

mouse_click = True

Ww, Hh, = WIDTH / WIDTH_M, HEIGHT / HEIGHT_M

screen = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()

btn_group = pygame.sprite.Group()
mod_list = pygame.sprite.Group()
list_of_mod = pygame.sprite.Group()

page = 0

mouse_surf = pygame.Surface((5, 5))
mouse_surf.fill((255, 255, 255))

active_mod = []


def load_active_mod():
    global active_mod
    with open("Data/json/Active_mod.json", "r") as f:
        active_mod  = json.load(f)["active"]


def start_game():
    global game_status
    game_status = "Play"


def quit_from_game():
    pygame.quit()
    quit()


def change_to():
    global menu_status
    menu_status = ["ModMenu", "Menu"][not menu_status == "Menu"]
    if menu_status == "Menu":
        GLOBALS.reset()
        GLOBALS.weapon_load()
        GLOBALS.init_weapon()
    if menu_status == "ModMenu":
        make_page_list_mod()


def page_next():
    global page
    page += 1
    make_page_list_mod()


def page_previous():
    global page
    page = max(page-1, 0)
    make_page_list_mod()


def mouse_pos_get():
    Mpos = pygame.mouse.get_pos()
    Mpos = (Mpos[0] * Ww, Mpos[1] * Hh)
    return Mpos


def change_state_mod(modName):
    global active_mod
    print("Change state mod")
    if modName in active_mod:
        active_mod.remove(modName)
    else:
        active_mod.append(modName)

    with open("Data/json/Active_mod.json", "w") as file:
        file.write(json.dumps({"active": active_mod}))

    make_page_list_mod()


def make_mod_cell(direct, i):
    with open(direct+"/Init.json") as file:
        modInfo = json.load(file)
        print(direct.split("/")[-1])
        print(modInfo, active_mod)
        print(direct.split("/")[-1] in active_mod)
        return ModCell(size=(800, 150), color=(90, 90, 90),
                       text=modInfo["description"],
                       title=modInfo["title"],
                       pos=(250, 150*i+160 +(20*i)),
                       font_size=40,
                       img=direct+"/"+modInfo["logo"],
                       active=direct.split("/")[-1] in active_mod,
                       command=lambda:change_state_mod(direct.split("/")[-1]),
                       )


def make_page_list_mod():
    global list_of_mod
    print("page is", page)
    list_of_mod = pygame.sprite.Group()
    modL = [i[1] for i in os.walk(os.getcwd() + "/Data/mods")][0][page*3:page*3+3]
    for mod in range(len(modL)):
        s = make_mod_cell("Data/mods/" + modL[mod], mod)
        list_of_mod.add(s)


# btn_group
TileGame = Table.TABLE(size=(500, 50), color=(50, 50, 50), text="SIMPLE ROUGHLIKE GAME", pos=(WIDTH//3-20, 300),  font_size=40)
btn_group.add(TileGame)

TileGame = Table.TABLE(size=(460, 50), color=(90, 90, 90), text="Play", pos=(WIDTH // 3-6, 400), font_size=45, command=start_game)
btn_group.add(TileGame)

TileGame = Table.TABLE(size=(460, 50), color=(90, 90, 90), text="Mods", pos=(WIDTH // 3-6, 500), font_size=45, command=change_to)
btn_group.add(TileGame)

TileGame = Table.TABLE(size=(460, 50), color=(90, 90, 90), text="Quit", pos=(WIDTH // 3-6, 600), font_size=45, command=quit_from_game)
btn_group.add(TileGame)

# mod_list
TileGame = Table.TABLE(size=(460, 50), color=(50, 50, 50), text="List of mods", pos=(WIDTH // 3, 40), font_size=50)
mod_list.add(TileGame)

TileGame = Table.TABLE(size=(80, 55), color=(50, 50, 50), text="<=", pos=(80, HEIGHT//2), font_size=50, command=page_previous)
mod_list.add(TileGame)

TileGame = Table.TABLE(size=(80, 55), color=(50, 50, 50), text="=>", pos=(1140, HEIGHT//2), font_size=50, command=page_next)
mod_list.add(TileGame)

TileGame = Table.TABLE(size=(460, 55), color=(90, 90, 90), text="back", pos=(WIDTH // 3-12, 720), font_size=50, command=change_to)
mod_list.add(TileGame)

load_active_mod()
print([i[1] for i in os.walk(os.getcwd() + "/Data/mods")][0])

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
            if menu_status == "Menu":
                for btn in btn_group:
                    if btn.pos_in(mouse):
                        btn.do_click()
            else:
                for btn in mod_list:
                    if btn.pos_in(mouse):
                        btn.do_click()
                for btn in list_of_mod:
                    if btn.pos_in(mouse):
                        btn.do_click()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = True

    
    screen.fill((50, 50, 50))
    if menu_status == "Menu":
        btn_group.update(mouse)
        btn_group.draw(screen)
    else:
        mod_list.update(mouse)
        list_of_mod.update(mouse)
        mod_list.draw(screen)
        list_of_mod.draw(screen)

    screen.blit(mouse_surf, mouse)

    return screen
