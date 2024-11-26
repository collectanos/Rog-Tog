import json
import pygame
import os
import ModManger

pygame.init()

weapon = {}

race_green = []
race_blue = []
race_red = []
race_gold = []

action_race = {"green": False, "blue": False, "red": False, "gold": False}

pygame.font.init()
FONT_TEXT = pygame.font.Font(os.path.dirname(__file__) + "/Data/fonts/game_font.ttf", 17)


def init_weapon():
    global race_green, race_blue, race_red, race_gold
    for i, name in zip(weapon.values(), weapon.keys()):
        if i in action_race.values():
            action_race[i] = True
        if i['race'] == 'green':
            race_green.append(name)
        elif i['race'] == 'blue':
            race_blue.append(name)
        elif i['race'] == 'red':
            race_red.append(name)
        elif i['race'] == 'gold':
            race_gold.append(name)


def reset():
    global weapon, race_blue, race_red, race_gold, race_green
    weapon = {}

    race_green = []
    race_blue = []
    race_red = []
    race_gold = []


def weapon_load():
    global weapon
    with open("Data/json/Weapons.json", "r") as weapon_settings:
        weapon = json.load(weapon_settings)

    weapon |= ModManger.ModManger("Data/json/Active_mod.json").weapon


FPS = 60
WIDTH, HEIGHT = 1280, 800
WIDTH_M, HEIGHT_M = pygame.display.Info().current_w, pygame.display.Info().current_h
with open("Data/json/Config.json", "r") as configJSON:
    config = json.load(configJSON)
    print(config)
    FPS = config["FPS"]
    WIDTH_M, HEIGHT_M = config["WIDTH"], config["HEIGHT"]
    WIDTH, HEIGHT = WIDTH_M, HEIGHT_M

weapon_load()
init_weapon()

print(race_blue, race_gold, race_red, race_green)
