import LevelGenerator
import pygame.time as time


class LEVEL:
    def __init__(self):
        self.state = ""
        self.seed = int(time.get_ticks())
        self.size = 4
        self.open_doors = True
        self.place = 8
        self.map = []
        self.x, self.y = 0, 0
        self.dif = 1
        self.make_new_level()

    def make_new_level(self):
        self.seed = int(time.get_ticks())
        gen = LevelGenerator.GENERATOR(self.seed, self.size, self.place, self.dif)
        self.map = gen.get_map()
        self.set_new_pos(*gen.start_gen)

    def get_doors(self):
        return self.get_room().get_doors()

    def get_room(self):
        return self.map[self.y][self.x]

    def set_in_player(self):
        self.map[self.y][self.x].plyer_in = True

    def near_no_enemy(self):
        for direct in self.get_room().get_doors():
            if direct == "up":
                if self.map[self.y - 1][self.x].type != "Null" and self.map[self.y - 1][self.x].type != "Enemy":
                    self.map[self.y-1][self.x].plyer_in = True
            elif direct == "down":
                if self.map[self.y+1][self.x].type != "Null" and self.map[self.y+1][self.x].type != "Enemy":
                    self.map[self.y+1][self.x].plyer_in = True
            elif direct == "left":
                if self.map[self.y][self.x-1].type != "Null" and self.map[self.y][self.x-1].type != "Enemy":
                    self.map[self.y][self.x-1].plyer_in = True
            elif direct == "right":
                if self.map[self.y][self.x+1].type != "Null" and self.map[self.y][self.x+1].type != "Enemy":
                    self.map[self.y][self.x+1].plyer_in = True

    def set_new_pos(self, x, y):
        self.x, self. y = x, y
        self.map[y][x].type = "Null"
        self.state = "Null"
        self.open_doors = True
        self.near_no_enemy()
        self.set_in_player()

    def add_pos(self, x, y):
        self.x += x
        self.y += y
        self.set_in_player()
        self.near_no_enemy()
        if self.get_room().type == "Enemy" or (self.get_room().type == "Boss" and not self.get_room().dead_boss):
            self.new_room()

    def new_room(self):
        if self.get_room().type == "Enemy":
            self.state = "Fight"
            self.open_doors = False
        elif self.get_room().type == "Boss":
            self.state = "Boss"
            self.open_doors = False

    def count_enemy(self):
        return self.get_room().value_enemy

    def room_clear(self):
        self.get_room().type = "Null"
        self.state = ""
        self.open_doors = True
