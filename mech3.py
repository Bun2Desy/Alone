import random
import time

import pygame
from Units2 import *
from random import randint
from info import *

pygame.init()

screen=pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
last_shoot_time = time.time() + 2000000000

hero = Hero(100, 3, 10, 1, 100, 50, 50, 45, 75)

enemi=[]
ghost_timer=pygame.USEREVENT+1
pygame.time.set_timer(ghost_timer,3000)

while True:
    if time.time() - last_shoot_time >= 1 and hero.mana < 100:
        hero.restore_mana()
        last_shoot_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key in click_status:
                click_status[event.key] = 1
            if event.key == pygame.K_SPACE:
                if hero.mana >= 5:
                    hero.do_shoot()
                    last_shoot_time = time.time()
        if event.type == pygame.KEYUP:
            if event.key in click_status:
                click_status[event.key] = 0
#ghost spawn
        if event.type == ghost_timer:
            enemi.append(Ghost(50,2,5,2,randint(0,WIDTH), randint(0,HEIGHT)))
    move = (hero.speed * (click_status[pygame.K_d] - click_status[pygame.K_a]), hero.speed * (click_status[pygame.K_s] - click_status[pygame.K_w]))
    hero.step_fence(move)

    #chase_ghosts
    for angry in enemi:
        angry.chase(hero.x+random.choice([0,25,50]), hero.y+random.choice([0,25,50]))

    screen.fill(GREY)

    #move_sprite_draw
    hero.redrawgamehero()

    pygame.draw.rect(screen, (255, 255, 255), hero.hitbox, 1)


    for angry in enemi:
        screen.blit(ghost_sprites[3],angry.hitbox)
        #pygame.draw.rect(screen, (255, 0, 0), angry.hitbox, 1)

    pygame.display.update()

    clock.tick(FPS)