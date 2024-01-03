import json
import pygame
import os

pygame.init()

weapon = {}

race_green = []
race_blue = []
race_red = []
race_gold = []

action_race = {"green": False, "blue": False, "red": False, "gold": False}

pygame.font.init()
FONT_TEXT = pygame.font.Font(os.path.dirname(__file__) + "/Data/fonts/game_font.ttf", 17)

with open("Data/json/Weapons.json", "r") as weapon_settings:
    weapon = json.load(weapon_settings)

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

print(race_blue, race_gold, race_red, race_green)

FPS = 60
WIDTH, HEIGHT = 1280, 800
WIDTH_M, HEIGHT_M = pygame.display.Info().current_w, pygame.display.Info().current_h
with open("Data/json/Config.json", "r") as configJSON:
    config = json.load(configJSON)
    print(config)
    FPS = config["FPS"]
    WIDTH_M, HEIGHT_M = config["WIDTH"], config["HEIGHT"]