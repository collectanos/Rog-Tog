import pygame
import random
import GLOBALS
import Weapon


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Chest, self).__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    @staticmethod
    def make_weapon(name):
        obj = GLOBALS.weapon[name]
        return Weapon.WEAPON(name=name, race=obj["race"], delay=obj["delay"], dmg=obj["dmg"], reload=obj["reload"],
                             type_shoot=obj["type_shoot"], bullet_per_clip=obj["bullet_per_clip"],
                             auto_shoot=obj['auto_shoot'], count_clip=obj['count_clip'], die=obj['die'],
                             image=obj['image'])

    def gen_weapon(self):
        print(GLOBALS.race_gold, GLOBALS.race_red, GLOBALS.race_blue, GLOBALS.race_green)
        race = "green"
        if random.random() < .4:
            race = "blue"
        if random.random() < .2:
            race = "red"
        if random.random() < .05:
            race = "gold"

        if not GLOBALS.race_gold:
            race = "red"
        if not GLOBALS.race_red:
            race = "blue"
        if not GLOBALS.race_blue:
            race = "green"

        if race == "gold":
            name = random.choice(GLOBALS.race_gold)
        elif race == "red":
            name = random.choice(GLOBALS.race_red)
        elif race == "blue":
            name = random.choice(GLOBALS.race_blue)
        else:
            name = random.choice(GLOBALS.race_green)

        return self.make_weapon(name)
