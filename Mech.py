import time

import pygame
from Units import *

pygame.init()

screen = pygame.display.set_mode((400, 400))

FPS = 60
clock = pygame.time.Clock()
move = (0, 0)
hero = Hero(50, 50)
hero_hitbox = pygame.Rect(hero.x, hero.y, 50, 50)
click_status = {pygame.K_w: 0, pygame.K_s: 0, pygame.K_d: 0, pygame.K_a: 0}
last_shoot_time = time.time() + 1000000000

ghost = Ghost(50, 2, 5, 2, 20, 20)
#ghost_hitbox = pygame.Rect(ghost.x, ghost.y, 40, 40)

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
    move = (hero.speed * (click_status[pygame.K_d] - click_status[pygame.K_a]), hero.speed * (click_status[pygame.K_s] - click_status[pygame.K_w]))
    hero.hitbox.move_ip(move)
    hero.set_pos(move[0], move[1])

    ghost.chase(hero.x, hero.y)

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), ghost.hitbox, 1)
    pygame.draw.rect(screen, (255, 255, 255), hero.hitbox, 1)
    pygame.display.update()

    clock.tick(FPS)
