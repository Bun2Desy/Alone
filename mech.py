import random
import time
import pygame
from Units import *
from random import randint
from info import *
from Maps import maps_generation
from sqll import *

pygame.init()
clock = pygame.time.Clock()

game_over = False

maxi = 5
time_spawn = 3000
pygame.time.set_timer(ghost_timer, time_spawn)

last_damage = time.time()

countghost = 0
killghost = 0
kills = 0
number_room = 0

change = True


def hero_game(hero):
    """Game play
    :param hero: hero object
    :type hero: __main__.Hero
    :return: True
    :rtype: bool
    """
    global game_over, open_door, countghost, change, blocks, blocks_without_door, enter_door, exit_door, number_room, \
        maxi, time_spawn, killghost, kills, last_damage
    if game_over:
        game_over = False
        bullets.clear()
        enemi.clear()
        Items.clear()
        number_room = 0
        time_spawn = 3000
        change = True
        maxi = 5
        killghost = 0
        for key in click_status:
            click_status[key] = 0
        create_table(hero.difficulty)
        set_score_database(hero.name, kills, hero.difficulty)
        kills = 0
        return True
    else:
        if change:
            blocks, blocks_without_door, enter_door, exit_door = maps_generation()
            hero.start_pos(enter_door.door_box.x, enter_door.door_box.y)
            countghost = 0
            number_room += 1
            maxi = number_room + maxi
            if time_spawn != 200:
                time_spawn -= 200
            pygame.time.set_timer(ghost_timer, time_spawn)
            hero.mana = 5
            change = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key in click_status:
                    click_status[event.key] = 1
            if event.type == pygame.KEYUP:
                if event.key in click_status:
                    click_status[event.key] = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hero.mana != 0:
                bullet = Bullet(hero.get_pos()[0], hero.get_pos()[1], pygame.mouse.get_pos()[0],
                                pygame.mouse.get_pos()[1])
                bullets.append(bullet)
                bullet.culc_function()
                if hero.mana != 0:
                    hero.do_shoot()
            if exit_door.openy(hero, open_door) and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen.fill(GREY)
                enemi.clear()
                bullets.clear()
                Items.clear()
                open_door = False
                countghost = 0
                killghost = 0
                change = True

            if event.type == ghost_timer and countghost < maxi:
                x = randint(indent[0], fence_size[0])
                y = randint(indent[1], fence_size[1])
                if not (pygame.Rect(x, y, 35, 35).colliderect(
                        pygame.Rect(hero.x, hero.y, hero.hitbox.height + 10, hero.hitbox.width + 10))):
                    enemi.append(Ghost(x, y, 35, 35))
                    countghost += 1

        move = (hero.speed * (click_status[pygame.K_d] - click_status[pygame.K_a]),
                hero.speed * (click_status[pygame.K_s] - click_status[pygame.K_w]))
        move_x = move[0]
        move_y = move[1]
        hero.hitbox.move_ip((move_x, move_y))
        hero.set_pos(move_x, move_y)
        hero.step_fence(move, blocks_without_door)

        for angry in enemi:
            angry.chase(hero.x + random.choice([0, 25, 50]), hero.y + random.choice([0, 25, 50]))

        for angry in enemi:
            if angry.hitbox.colliderect(hero.hitbox) and time.time() - last_damage >= 1:
                hero.health -= 1
                last_damage = time.time()
        if hero.health <= 0:
            game_over = True

        enter_door.draw(hero, open_door)
        exit_door.draw(hero, open_door)

        for i in blocks_without_door:
            pygame.draw.rect(screen, WHITE, i, 1)

        for angry in enemi:
            screen.blit(ghost_sprite, (angry.x - 23, angry.y - 23))

        hero.redrawgamehero(screen)

        for bull in bullets:
            pygame.draw.circle(screen, YELLOW, (bull.x, bull.y), bullet_radius)
            bull.change_coord()
            for ghost in enemi:
                if bull.collide_with_unit(ghost):
                    bullets.remove(bull)
                    ghost.is_dead = True
                    killghost += 1
                    kills += 1
                    if killghost == maxi:
                        item_no = 'key'
                        item = Item(item_no, ghost.x, ghost.y)
                        Items.append(item)
                    else:
                        item_no = 'chakra'
                        item = Item(item_no, ghost.x, ghost.y)
                        if item.casino() == [True]:
                            Items.append(item)

                    break
            if bull.collide_with_wall(blocks):
                bullets.remove(bull)

        for ghost in enemi:
            if ghost.is_dead:
                enemi.remove(ghost)

        for i in Items:
            i.render(screen)
            if i.hitbox.colliderect(hero.hitbox) and i.type == "key":
                open_door = i.collision(hero)
            elif i.hitbox.colliderect(hero.hitbox):
                i.collision(hero)

        Score(kills, number_room).kill_and_room_count(screen)
        hero.draw_health(screen)
        hero.draw_mana(screen)

    clock.tick(FPS)
