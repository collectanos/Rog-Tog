import Room
import random


class GENERATOR:
    def __init__(self, seed, size, place, lvl):
        print(seed, size, place)
        self.map = [[''] * size for _ in range(size)]
        self.lvl = lvl
        self.size = size
        random.seed(seed)
        self.start_gen = [random.randint(0, size-1), random.randint(0, size-1)]
        self.boss = False
        self.boss_pos = []
        self.max_chest = 5
        self.chest_count = 0
        self.make_place(place, *self.start_gen)
        self.correct_place()
        self.map[self.boss_pos[1]][self.boss_pos[0]].type = "Boss"

    def get_map(self):
        return [i.copy() for i in self.map]

    def make_room(self, size):
        rm = Room.ROOM(size=size, count_enemy=int(10 * (self.lvl/10+1)))
        rm.set_doors(*[random.randint(0, 1) for _ in range(4)])
        rm.type = "Enemy"
        return rm

    def in_place(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def get_free_place(self, x, y):
        return [
                self.in_place(x, y-1) and not self.map[y-1][x],
                self.in_place(x, y+1) and not self.map[y+1][x],
                self.in_place(x-1, y) and not self.map[y][x-1],
                self.in_place(x+1, y) and not self.map[y][x+1]
            ]

    def get_inside_place(self, x, y):
        return [
            self.in_place(x, y-1),
            self.in_place(x, y+1),
            self.in_place(x-1, y),
            self.in_place(x+1, y)
            ]

    @staticmethod
    def free_paths_to_words(paths):
        words = []
        for i in [i if i[0] else None for i in zip(paths, ["up", "down", "left", "right"])]:
            if not (i is None):
                words.append(i[1])

        return words

    @staticmethod
    def word_to_vect(word):
        return {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0]}[word]

    @staticmethod
    def vect_to_word(vect):
        if [0, -1] == vect:
            return "up"
        if [0, 1] == vect:
            return "down"
        if [1, 0] == vect:
            return "right"
        if [-1, 0] == vect:
            return "left"

    @staticmethod
    def step_to_bool_list(x1, y1, x2, y2):
        bool_list = [False, False, False, False]
        # up down left right
        if y1 - y2 == 1:
            bool_list[1] = True
        if y1 - y2 == -1:
            bool_list[0] = True
        if x1 - x2 == 1:
            bool_list[3] = True
        if x1 - x2 == -1:
            bool_list[2] = True

        return bool_list

    def make_place(self, size, x, y, last_x=None, last_y=None):
        rm = self.make_room(size)
        paths = self.get_free_place(x, y)

        rm.set_doors(*[path*room for path, room in zip(paths, rm.doors.values())])

        if not rm.get_doors():
            rm.set_doors(*paths)

        if size == 1 or len(rm.get_doors()) == 0:
            rm.set_doors(False, False, False, False)

            if not (last_y is None) and not (last_x is None):
                rm.set_doors(*self.step_to_bool_list(last_x, last_y, x, y))

            if not self.boss:
                self.boss_pos = [x, y]
                rm.type = "Boss"
                self.boss = True

            self.map[y][x] = rm
            return

        self.map[y][x] = rm

        for i in rm.get_doors():
            xi, yi = self.word_to_vect(i)
            self.make_place(size-1, xi+x, yi+y, x, y)

        if not (last_y is None) and not (last_x is None):
            rm.doors[self.vect_to_word([last_x-x, last_y-y])]= True

    # up down left right
    def correct_place(self):
        for y, line in enumerate(self.map):
            for x, block in enumerate(line):
                if block:
                    paths = self.get_inside_place(x, y)
                    if paths[0] and self.map[y-1][x] and self.map[y-1][x].doors["down"]:
                        self.map[y][x].doors["up"] = True
                    if paths[1] and self.map[y+1][x] and self.map[y+1][x].doors["up"]:
                        self.map[y][x].doors["down"] = True
                    if paths[2] and self.map[y][x-1] and self.map[y][x-1].doors["right"]:
                        self.map[y][x].doors["left"] = True
                    if paths[3] and self.map[y][x+1] and self.map[y][x+1].doors["left"]:
                        self.map[y][x].doors["right"] = True

                    if x != self.start_gen[0] and y != self.start_gen[1]:
                        if block.type != "Boss" and random.random() < .25 and self.max_chest >= self.chest_count:
                            block.type = "Chest"
                            self.chest_count += 1

                        if not self.boss:
                            block.type = "Boss"
                            self.boss = True
                            self.boss = [x, y]


if __name__ == "__main__":
    import time
    gen = GENERATOR(int(time.time()), 100, 10, 1)
    import Draw_windows
    import pygame
    display = pygame.display.set_mode((600, 600))
    while True:
        # 1670348597
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gen = GENERATOR(int(time.time()), 100, 991)
                    print("DO")
                    #print(gen.boss)
                    #print([[j.type if j else None for j in i] for i in gen.map])

        display.fill((0, 0, 0))
        surf = Draw_windows.DRAW().draw_map(gen.map, *gen.start_gen, 1010)
        surf = pygame.transform.scale(surf, (600, 600))
        display.blit(surf, (0, 0))
        pygame.display.flip()
