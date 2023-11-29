import random
import time

import pygame
from Units import *
from random import randint


pygame.init()

screen = pygame.display.set_mode((400, 400))

FPS = 60
clock = pygame.time.Clock()
move = (0, 0)
hero = Hero(100, 3, 10, 1, 100, 50, 50, 45, 75)
#hero_hitbox = pygame.Rect(hero.x, hero.y, 50, 50)
click_status = {pygame.K_w: 0, pygame.K_s: 0, pygame.K_d: 0, pygame.K_a: 0}
last_shoot_time = time.time() + 2000000000

ghost = Ghost(50, 1, 5, 2, randint(0,400), randint(0,400))#20,20
#ghost_hitbox = pygame.Rect(ghost.x, ghost.y, 40, 40)


enemi=[]
maxenemies = 1
for i in range(maxenemies):
    enemi.append(Ghost(50,2,5,2,randint(0,400), randint(0,400)))
ghost_timer=pygame.USEREVENT+1
pygame.time.set_timer(ghost_timer,1000)



walkRight=[pygame.transform.scale(pygame.image.load('right/Sprite1.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
    'right/Sprite2.png'), (80, 80)), pygame.transform.scale(pygame.image.load('right/Sprite3.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
    'right/Sprite4.png'), (80, 80))]
walkLeft=[pygame.transform.scale(pygame.image.load('left/LSprite1.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
    'left/LSprite2.png'), (80, 80)), pygame.transform.scale(pygame.image.load('left/LSprite3.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
    'left/LSprite4.png'), (80, 80))]
walkUP=[pygame.transform.scale(pygame.image.load('up/UpSprite1.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
    'up/UpSprite2.png'), (80, 80)), pygame.transform.scale(pygame.image.load('up/UpSprite3.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
    'up/UpSprite4.png'), (80, 80)),pygame.transform.scale(pygame.image.load('up/UpSprite5.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
        'up/UpSprite6.png'), (80, 80)), pygame.transform.scale(pygame.image.load('up/UpSprite7.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
        'up/UpSprite8.png'), (80, 80))]
walkDOWN=[pygame.transform.scale(pygame.image.load('down/DoSprite1.png'),(80,80)),pygame.transform.scale(pygame.image.load('down/DoSprite2.png'),(80,80)),pygame.transform.scale(pygame.image.load('down/DoSprite3.png'),(80,80)),pygame.transform.scale(pygame.image.load('down/DoSprite4.png'),(80,80)),
        pygame.transform.scale(pygame.image.load('down/DoSprite5.png'),(80,80)),pygame.transform.scale(pygame.image.load('down/DoSprite6.png'),(80,80))]
stand=pygame.transform.scale(pygame.image.load('stand/Sprite-0003.png'), (80, 80))
ghost_sprites=[pygame.transform.scale(pygame.image.load('enemy/ghostmove1.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
    'enemy/ghostmove2.png'), (80, 80)), pygame.transform.scale(pygame.image.load('enemy/ghostmove3.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
    'enemy/ghostmove4.png'), (80, 80)),pygame.transform.scale(pygame.image.load('enemy/ghostmove5.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
        'enemy/ghostmove6.png'), (80, 80)), pygame.transform.scale(pygame.image.load('enemy/ghostmove7.png'), (80, 80)), pygame.transform.scale(pygame.image.load(
        'enemy/ghostmove8.png'), (80, 80))]
#hero_size = pygame.Rect(50,50, 50, 50)




right=False
left=False
up=False
down=False
walkcount=0


def redrawgamehero():
    global walkcount
    screen.fill((100, 100, 100))
    if walkcount+1>=12:
        walkcount=0
    if right:
        screen.blit(walkRight[walkcount//3],(hero.x - 17, hero.y - 7))
        walkcount+=1
    elif left:
        screen.blit(walkLeft[walkcount // 3], (hero.x - 17, hero.y - 7))
        walkcount += 1
    elif up and not(right) and not(left):
        screen.blit(walkUP[walkcount // 3], (hero.x - 17, hero.y - 7))
        walkcount += 1
    elif down and not(right) and not(left):
        screen.blit(walkDOWN[walkcount // 3], (hero.x - 17, hero.y - 7))
        walkcount += 1
    else:
        screen.blit(stand, (hero.x - 17, hero.y - 7))

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

        if event.type == ghost_timer:
            enemi.append(Ghost(50,2,5,2,randint(0,400), randint(0,400)))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        right = True
        left = False
        up = False
        down = False
    elif keys[pygame.K_a]:
        right = False
        left = True
        up = False
        down = False
    elif keys[pygame.K_w] and not (keys[pygame.K_d] or keys[pygame.K_a]):
        right = False
        left = False
        up = True
        down = False
    elif keys[pygame.K_s] and not (keys[pygame.K_d] or keys[pygame.K_a]):
        right = False
        left = False
        up = False
        down = True
    else:
        right = False
        left = False
        up = False
        down = False
        walkcount = 0
    move = (hero.speed * (click_status[pygame.K_d] - click_status[pygame.K_a]), hero.speed * (click_status[pygame.K_s] - click_status[pygame.K_w]))
    hero.hitbox.move_ip(move)
    hero.set_pos(move[0], move[1])
    #hero.hitbox.move_ip(move)

    for angry in enemi:
        angry.chase(hero.x+random.choice([0,25,50]), hero.y+random.choice([0,25,50]))

    #ghost.chase(hero.x, hero.y)


    screen.fill((200, 200, 200))
    redrawgamehero()
    pygame.draw.rect(screen, (255, 255, 255), hero.hitbox, 1)
    #print(hero.x, hero.y, hero.hitbox.x, hero.hitbox.y)

    for angry in enemi:
        #for sprite in ghost_sprites:
        screen.blit(ghost_sprites[3],angry.hitbox)
        #pygame.draw.rect(screen, (255, 0, 0), angry.hitbox, 1)


    #pygame.draw.rect(screen, (255, 0, 0), ghost.hitbox, 1)
    #pygame.draw.rect(screen, (255, 255, 255), hero.hitbox, 1)
    pygame.display.update()

    clock.tick(FPS)