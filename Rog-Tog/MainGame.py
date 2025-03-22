import random
import pygame
import Chest
import GLOBALS
import ItemWeapon
import Level
import Player
import Draw_windows
import Door
import Enemy
import Boss
import Table
import Weapon
import ShootEnemy
import MainMenu
from GLOBALS import FPS, WIDTH, HEIGHT, WIDTH_M, HEIGHT_M
from Hint import Hint

pygame.init()

Ww, Hh, = WIDTH_M / WIDTH, HEIGHT_M / HEIGHT

screen = pygame.Surface((WIDTH_M, HEIGHT_M))

arr_enemy = [Enemy.ENEMY, ShootEnemy.SHOOTENEMY]

clock = pygame.time.Clock()

space_hint = Hint()

group_player = pygame.sprite.Group()
group_enemy = pygame.sprite.Group()
group_bullet = pygame.sprite.Group()
group_door = pygame.sprite.Group()
group_item = pygame.sprite.Group()
group_enemy_bullet = pygame.sprite.Group()
group_chest = pygame.sprite.Group()
group_item_use = pygame.sprite.Group()
group_pause_menu = pygame.sprite.Group()

can_pressed_key_E = True
can_pressed_key_R = True
can_pressed_key_P = True
can_pressed_key_C = True

stop_time = False


def resume():
    global stop_time
    stop_time = False


def exit_to_menu():
    MainMenu.game_status = "Menu"
    resume()


pause_menu = pygame.Surface((840, 600))
pause_menu.fill((60, 60, 60))

hud = Table.TABLE(size=(380, 50), color=(60, 60, 60), text="Pause", pos=(320, 150), font_size=50)
group_pause_menu.add(hud)

hud = Table.TABLE(size=(380, 50), color=(120, 120, 120), text="Resume", pos=(240, 250), command=resume, font_size=40)
group_pause_menu.add(hud)

hud = Table.TABLE(size=(380, 50), color=(120, 120, 120), text="Exit", pos=(240, 350), command=exit_to_menu, font_size=40)
group_pause_menu.add(hud)

boss = None
pl = Player.PLAYER(pygame.math.Vector2(WIDTH//2, HEIGHT//2), Weapon.WEAPON())
group_player.add(pl)

lvl = Level.LEVEL()
lvl.make_new_level()


def next_lvl():
    lvl.dif += 1
    lvl.make_new_level()
    group_enemy.empty()
    group_bullet.empty()
    group_item.empty()
    group_door.empty()
    group_enemy_bullet.empty()


def init():
    global pl, lvl
    lvl = Level.LEVEL()
    lvl.make_new_level()
    group_enemy.empty()
    group_bullet.empty()
    group_player.empty()
    group_item.empty()
    group_door.empty()
    group_item_use.empty()
    group_enemy_bullet.empty()
    group_enemy_bullet.empty()
    pl = Player.PLAYER(pygame.math.Vector2(WIDTH // 2, HEIGHT // 2), Weapon.WEAPON())
    group_player.add(pl)


def update(delta, width, height):
    global can_pressed_key_E, can_pressed_key_P, can_pressed_key_R, group_item, stop_time,\
        group_item, group_item_use, boss, can_pressed_key_C, space_hint, WIDTH, HEIGHT
    
    WIDTH, HEIGHT = width, height
    Ww, Hh, = WIDTH_M / WIDTH, HEIGHT_M / HEIGHT

    group_door.empty()

    for event in pygame.event.get():
        if event.type == pygame.WINDOWRESIZED:
            WIDTH = event.x
            HEIGHT = event.y
            Ww, Hh, = WIDTH_M / WIDTH, HEIGHT_M / HEIGHT

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o or event.key == 1097:
                init()

            if event.key == pygame.K_e or event.key == 1091:
                collision = pygame.sprite.spritecollide(pl, group_item_use, False)

                if collision and can_pressed_key_E:
                    collision[0].pick_up_effect(pl)

                can_pressed_key_E = False

            if event.key == pygame.K_r or event.key == 1082:
                can_pressed_key_R = False

                if pl.get_active_weapon().can_reload() and pl.get_active_weapon().can_switch_clip() and\
                        pl.get_active_weapon().clip_now < pl.get_active_weapon().bullets_per_clip:
                    pl.get_active_weapon().clip_now = 0
                    pl.get_active_weapon().time_to_reload = pygame.time.get_ticks() + pl.get_active_weapon().reload

            if (event.key == pygame.K_p or event.key == 1079) and can_pressed_key_P:
                stop_time = not stop_time
                can_pressed_key_P = False

            if event.key == pygame.K_c and can_pressed_key_C:
                can_pressed_key_C = False
                group_chest.add(Chest.Chest((random.randint(20, WIDTH_M-20), random.randint(20, HEIGHT_M-20))))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e or event.key == 1091:
                can_pressed_key_E = True

            if event.key == pygame.K_r or event.key == 1082:
                can_pressed_key_R = True

            if event.key == pygame.K_p or event.key == 1079:
                can_pressed_key_P = True

            if event.key == pygame.K_c:
                can_pressed_key_C = True

    screen.fill((50, 50, 50))

    for i in lvl.get_doors():
        if i == "up":
            group_door.add(Door.DOOR([0, -1], [WIDTH_M // 2 - 20, 20]))
        if i == "down":
            group_door.add(Door.DOOR([0, 1], [WIDTH_M // 2 - 20, HEIGHT_M - 20]))
        if i == "left":
            group_door.add(Door.DOOR([-1, 0], [20, HEIGHT_M // 2 - 20]))
        if i == "right":
            group_door.add(Door.DOOR([1, 0], [WIDTH_M - 20, HEIGHT_M // 2 - 20]))

    if lvl.get_room().dead_boss:
        d = Door.DOOR([0, 0], [WIDTH_M // 2 - 20, HEIGHT_M // 2 - 20])
        d.next_lvl = True
        group_door.add(d)

    collision = pygame.sprite.spritecollide(pl, group_door, dokill=False)

    if collision and lvl.open_doors:
        collision = collision[0]

        if collision.next_lvl:
            next_lvl()

        if len(group_item):
            lvl.get_room().save_item = group_item.copy()

        if len(group_item_use):
            lvl.get_room().save_weapon = group_item_use.copy()

        group_item.empty()
        group_chest.empty()
        group_item_use.empty()

        lvl.add_pos(*collision.move_in_map)

        if not lvl.get_room().save_item is None and len(lvl.get_room().save_item):
            group_item = lvl.get_room().save_item.copy()

        if not lvl.get_room().save_weapon is None and len(lvl.get_room().save_weapon):
            group_item_use = lvl.get_room().save_weapon.copy()

        if lvl.get_room().type == "Chest" and not lvl.get_room().open_chest:
            group_chest.add(Chest.Chest((WIDTH_M // 2, HEIGHT_M // 2)))

        if collision.move_in_map[0] == 1:
            pl.rect.left = 40
        if collision.move_in_map[0] == -1:
            pl.rect.right = WIDTH_M-40
        if collision.move_in_map[1] == 1:
            pl.rect.top = 40
        if collision.move_in_map[1] == -1:
            pl.rect.bottom = HEIGHT_M - 40

        group_bullet.empty()
        group_enemy_bullet.empty()
        pl.set_new_pos()

        if lvl.state == "Fight":
            for _ in range(lvl.count_enemy()):
                group_enemy.add(random.choice(arr_enemy)([random.randint(20, WIDTH_M-20),
                 random.randint(20, HEIGHT_M-20)]))

        if lvl.state == "Boss" and not lvl.get_room().dead_boss:
            boss = Boss.BOSS((WIDTH_M // 2, HEIGHT_M // 2))
            group_enemy.add(boss)

    collision = pygame.sprite.groupcollide(group_bullet, group_enemy, False, False)

    for bullet, enemy in zip(collision.keys(), collision.values()):
        enemy[0].get_dmg(bullet.dmg)
        bullet.kill()

    collision = pygame.sprite.spritecollide(pl, group_enemy, False)

    if collision and collision[0].can_move():
        pl.get_dmg(collision[0].dmg)

    collision = pygame.sprite.spritecollide(pl, group_item, False)

    if collision and pl.hp < pl.max_hp:
        collision[0].pick_up_effect(pl)
        collision[0].kill()

    if lvl.state == "Fight" and not len(group_enemy):
        lvl.room_clear()

    collision = pygame.sprite.spritecollide(pl, group_enemy_bullet, False)

    if collision:
        collision = collision[0]
        pl.get_dmg(collision.dmg)
        collision.kill()

    collision = pygame.sprite.spritecollide(pl, group_chest, False)

    if collision:
        collision = collision[0]
        lvl.get_room().open_chest = True
        weapon = collision.gen_weapon()
        group_item_use.add(ItemWeapon.ItemWeapon(pl.pos, weapon))
        collision.kill()

    if not stop_time:
        group_bullet.update(delta)
        group_enemy_bullet.update(delta)
        group_player.update(delta, group_bullet, Ww, Hh, WIDTH_M, HEIGHT_M)
        group_enemy.update(delta, pl.pos, group_item, group_enemy_bullet, WIDTH_M, HEIGHT_M)
        group_door.draw(screen)
        group_item.draw(screen)
        group_item_use.draw(screen)
        group_enemy_bullet.draw(screen)
        group_chest.draw(screen)
        group_bullet.draw(screen)
        group_player.draw(screen)
        group_enemy.draw(screen)
        
    collision = pygame.sprite.spritecollide(pl, group_enemy, False)
    if collision:
        space_hint.show()
    else:
        space_hint.hide()

    surf = Draw_windows.DRAW().draw_map(lvl.map, lvl.x, lvl.y, size=50)
    surf.set_alpha(190)
    surf = pygame.transform.scale(surf, (100, 100))
    screen.blit(surf, (WIDTH_M-115, 15))

    screen.blit(Draw_windows.DRAW().draw_heal_bar(pl.hp, pl.max_hp), (20, 20))
    level_text = GLOBALS.FONT_TEXT.render(f"Level: {lvl.dif}", False, (255, 255, 255))
    level_rect = level_text.get_rect()
    level_rect.topleft = (20, 45)
    pygame.draw.rect(screen, (90, 90, 90), (level_rect.left - 5, level_rect.top - 5, level_rect.width + 10, level_rect.height + 10))
    screen.blit(level_text, level_rect)

    surf = Draw_windows.DRAW().draw_weapon_interface(pl.get_active_weapon())
    surf.set_alpha(190)
    screen.blit(surf, (WIDTH_M - 120, HEIGHT_M - 70))

    if pl.non_active_weapon():
        surf = Draw_windows.DRAW().draw_weapon_interface(pl.non_active_weapon())
        surf.set_alpha(100)
        screen.blit(surf, (WIDTH_M - 120, HEIGHT_M - 120))

    if lvl.state == "Boss" and not lvl.get_room().dead_boss:
        screen.blit(pygame.transform.scale(Draw_windows.DRAW().draw_heal_bar(boss.HP, boss.hp_max), (WIDTH_M-40, 12)),
                    (20, HEIGHT_M-20))
        if boss.HP < 0:
            lvl.state = "Null"
            lvl.open_doors = True
            lvl.get_room().dead_boss = True

    if stop_time:
        Mpos = pygame.mouse.get_pos()
        Mpos = (Mpos[0] * Ww - 240, Mpos[1] * Hh - 100)

        for btn in group_pause_menu:
            if btn.command:
                if btn.pos_in(Mpos):
                    btn.change_color((120, 120, 120))
                    btn.image = pygame.transform.scale(btn.image, (520, 55))
                    btn.rect = btn.image.get_rect(center=(btn.rect.center))
                    if pygame.mouse.get_pressed()[0]:
                        btn.do_click()
                else:
                    btn.change_color((90, 90, 90))
                    btn.image = pygame.transform.scale(btn.image, (520, 55))
                    btn.rect = btn.image.get_rect(center=(btn.rect.center))

        group_pause_menu.draw(pause_menu)
        screen.blit(pause_menu, (190, 100))

    if not pl.live():
        init()
        
    space_hint.update()
    space_hint.draw(screen)
    
    surf = pygame.Surface((5, 5))
    surf.fill((255, 255, 255))
    Mpos = pygame.mouse.get_pos()
    Mpos = (Mpos[0] * Ww, Mpos[1] * Hh)
    screen.blit(surf, (Mpos))

    clock.tick(FPS)
    
    return pygame.transform.scale(screen, (WIDTH, HEIGHT)), WIDTH, HEIGHT
