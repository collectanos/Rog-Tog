class ROOM:
    def __init__(self, size=1, _type="Enemy", count_enemy=10):
        self.doors = {"up": False, "down": False, "left": False, "right": False}
        self.plyer_in = False
        self.type = _type
        self.value_enemy = count_enemy//size
        self.save_item = None
        self.save_weapon = None
        self.open_chest = False
        self.dead_boss = False

    def set_doors(self, up, down, left, right):
        self.doors = {"up": up, "down": down, "left": left, "right": right}

    def get_doors(self):
        doors_vect = []

        for key, val in zip(self.doors.keys(), self.doors.values()):
            if val:
                doors_vect.append(key)

        return doors_vect
