import random
import time

import pygame
from Units import *
from random import randint
from info import *

pygame.init()

screen=pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
last_shoot_time = time.time() + 2000000000
bullet_radius = 5
game_over = False

hero = Hero(100, 3, 10, 1, 10, 50, 50, 30, 60)



enemi=[]
maxi=5
ghost_timer=pygame.USEREVENT+1
pygame.time.set_timer(ghost_timer,3000)
bullets = []


exitfield=pygame.Rect(300,300,50,50)
open_door=False
color=(255,0,0)

countghost=0

while True:
    if game_over:
        hero = Hero(100, 3, 10, 1, 100, 50, 50, 30, 60)
        bullets.clear()
        enemi.clear()
        for key in click_status:
            click_status[key] = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_over = False

    else:
        # if time.time() - last_shoot_time >= 1 and hero.mana < 100:
        #     hero.restore_mana()
        #     last_shoot_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if exitfield.colliderect(hero.hitbox) and open_door==True:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)

            if event.type == pygame.KEYDOWN:
                if event.key in click_status:
                    click_status[event.key] = 1
            if event.type == pygame.KEYUP:
                if event.key in click_status:
                    click_status[event.key] = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hero.mana!=0:
                bullet = Bullet(hero.get_pos()[0], hero.get_pos()[1], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                bullets.append(bullet)
                bullet.culc_function()
                if hero.mana >= 5:
                    hero.do_shoot()
                    last_shoot_time = time.time()



    #ghost spawn
            if event.type == ghost_timer and countghost<maxi:
                x=randint(0,WIDTH)
                y=randint(0,HEIGHT)
                if pygame.Rect(x, y, 35, 35).colliderect(pygame.Rect(hero.x, hero.y, hero.hitbox.height+10, hero.hitbox.width+10))==False:
                    enemi.append(Ghost(50,1,5,2,x, y, 35, 35))
        move = (hero.speed * (click_status[pygame.K_d] - click_status[pygame.K_a]), hero.speed * (click_status[pygame.K_s] - click_status[pygame.K_w]))
        hero.step_fence(move)

        #chase_ghosts
        for angry in enemi:
            angry.chase(hero.x+random.choice([0,25,50]), hero.y+random.choice([0,25,50]))

        for angry in enemi:
            if angry.hitbox.colliderect(hero.hitbox):
                game_over = True

        screen.fill(GREY)

        #move_sprite_draw
        hero.redrawgamehero()

        pygame.draw.rect(screen, (255, 255, 255), hero.hitbox, 1)

        pygame.draw.rect(screen, color, exitfield)


        #print(pygame.mouse.get_pos())
        for angry in enemi:
            screen.blit(ghost_sprites[3], (angry.x - 23, angry.y - 23))
            pygame.draw.rect(screen, (255, 0, 0), angry.hitbox, 1)

        #move_bullets
        for bull in bullets:
            pygame.draw.circle(screen, YELLOW, (bull.x, bull.y), bullet_radius)
            bull.change_coord()
            for ghost in enemi:
                if bull.collide_with_unit(ghost):
                    bullets.remove(bull)
                    ghost.is_dead = True
                    countghost+=1
                    if countghost==maxi:
                        item_no = 'key'
                        item = Item(item_no, ghost.x, ghost.y)
                        Items.append(item)
                    else:
                        item_no = 'chakra'
                        item = Item(item_no, ghost.x, ghost.y)
                        if item.casino()==[True]:
                            Items.append(item)

                    break
            if bull.collide_with_wall():
                bullets.remove(bull)

        print(len(bullets))

        # check_ghost_alive
        for ghost in enemi:
            if ghost.is_dead:
                enemi.remove(ghost)
        #draw items
        for i in Items:
            i.render()
            pygame.draw.rect(screen, (0, 0, 255), i.hitbox, 1)
            if i.hitbox.colliderect(hero.hitbox):
                if i.type == 'chakra':
                    hero.mana+= 10
                    Items.remove(i)
                if i.type == 'key':
                    open_door=True
                    Items.remove(i)



    pygame.display.update()

    clock.tick(FPS)