import pygame
import GLOBALS
import os


class DRAW:
    @staticmethod
    def draw_room(rm, bright=False, room_type="Null"):
        room = pygame.Surface((10, 10))
        room.fill((150, 160, 255))
        color = 120 + 40 * int(bright)
        if bright:
            pygame.draw.rect(room, (color, color, color), (2, 2, 6, 6))
        else:
            pygame.draw.rect(room, (color, color, color), (2, 2, 6, 6))

        if rm.doors["up"]:
            pygame.draw.rect(room, (color, color, color), (4, 0, 2, 2))

        if rm.doors["down"]:
            pygame.draw.rect(room, (color, color, color), (4, 8, 2, 2))

        if rm.doors["left"]:
            pygame.draw.rect(room, (color, color, color), (0, 4, 2, 2))

        if rm.doors["right"]:
            pygame.draw.rect(room, (color, color, color), (8, 4, 2, 2))

        if room_type == "Boss":
            pygame.draw.rect(room, (255, 0, 0), (4, 4, 2, 2))

        if room_type == "Chest":
            pygame.draw.rect(room, (255, 255, 0), (4, 4, 2, 2))
            return room

        if rm.save_item:
            pygame.draw.rect(room, (0, 255, 0), (4, 4, 2, 2))

        return room

    def draw_map(self, locate, xi, yi, size=60):
        surf = pygame.Surface((size, size))
        surf.fill((150, 160, 255))
        for y, line in enumerate(locate):
            for x, block in enumerate(line):
                if block and block.plyer_in:
                    surf.blit(self.draw_room(block, bright=xi == x and yi == y, room_type=block.type), (x*10+4, y*10+6))

        return surf

    @staticmethod
    def draw_heal_bar(hp, max_hp):
        surf = pygame.Surface((100, 12))
        surf.fill((255, 255, 255))
        if hp >= max_hp*0.75:
            pygame.draw.rect(surf, (255, 0, 0), (2, 2, 96*(hp/max_hp), 8))
        elif hp >= max_hp*0.5:
            pygame.draw.rect(surf, (255, 165, 0), (2, 2, 96*(hp/max_hp), 8))
        elif hp >= max_hp*0.25:
            pygame.draw.rect(surf, (255, 255, 0), (2, 2, 96*(hp/max_hp), 8))
        else:
            pygame.draw.rect(surf, (255, 255, 153), (2, 2, 96*(hp/max_hp), 8))
    
        return surf

    @staticmethod
    def draw_weapon_interface(weapon):
        surf = pygame.Surface((100, 40))
        if weapon.race == "green":
            surf.fill((90, 204, 105))
        elif weapon.race == "blue":
            surf.fill((90, 189, 204))
        elif weapon.race == "red":
            surf.fill((201, 60, 60))
        elif weapon.race == "gold":
            surf.fill((207, 209, 54))
        else:
            surf.fill(())
        surf.blit(GLOBALS.FONT_TEXT.render(f"{weapon.clip_now}/{weapon.bullets_per_clip} {weapon.count_clip}",
                                           False, (0, 0, 0)), (25, 13))
        surf.blit(pygame.transform.scale(weapon.image, (20, 20)), (2, 10))
        return surf

    @staticmethod
    def table(size, color, text, font_size):
        f = pygame.font.Font(os.path.dirname(__file__) + "/Data/fonts/game_font.ttf", font_size)
        surf = pygame.Surface(size)
        surf.fill(color)
        surf.blit(f.render(text, False, (0, 0, 0)), (5, 5))
        return surf
