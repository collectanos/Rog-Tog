import Item
import pygame

class ItemWeapon(Item.HealingItem):  # Изменено с Item.ITEM на Item.HealingItem
    def __init__(self, pos, weapon):
        super(ItemWeapon, self).__init__(pos, 0)
        self.weapon = weapon
        self.image = pygame.transform.scale(weapon.image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pick_up_effect(self, pl):
        ans = pl.pick_up_weapon(self.weapon)
        if ans:
            self.weapon = ans
        else:
            self.kill()
        self.image = pygame.transform.scale(self.weapon.image, (35, 35))
        self.rect.center = pl.pos