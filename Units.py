from random import randint
import pygame
from info import *

class Unit():
    def __init__(self, health, speed, damage, agility, x, y):
        self.health = health
        self.speed = speed
        self.damage = damage
        self.agility = agility
        self.is_dead = False
        self.x = x
        self.y = y

    def is_alive(self):
        if self.health <= 0:
            self.is_dead = True

    def get_damage(self, damage):
        self.health -= damage

    def set_pos(self, x, y):
        self.x += x
        self.y += y

    def get_pos(self):
        return (self.x, self.y)


class Ghost(Unit):
    def __init__(self, health, speed, damage, agility, x, y, hitbox_width, hitbox_height):
        Unit.__init__(self, health, speed, damage, agility, x, y)
        self.hitbox = pygame.Rect(x, y, hitbox_width, hitbox_height)

    def chase(self, hero_x, hero_y):
        ghost_x = self.x
        ghost_y = self.y
        change_x = 0
        change_y = 0
        if ghost_x < hero_x:
            change_x = 1
        elif ghost_x > hero_x:
            change_x = -1
        if ghost_y < hero_y:
            change_y = 1
        elif ghost_y > hero_y:
            change_y = -1
        change_pos = (self.speed * change_x, self.speed * change_y)
        self.hitbox.move_ip(change_pos)
        self.set_pos(change_pos[0], change_pos[1])




class Hero(Unit):
    def __init__(self, health, speed, damage, agility,  mana, x, y, hitbox_width, hitbox_heigth):
        Unit.__init__(self, health, speed, damage, agility, x, y)
        self.mana = mana
        self.hitbox = pygame.Rect(x, y, hitbox_width, hitbox_heigth)


    def do_shoot(self):
        self.mana -= 5

    def restore_mana(self):
        point_mana = randint(2, 4)
        if self.mana + point_mana > 100:
            self.mana = 100
        else:
            self.mana += point_mana

    def redrawgamehero(self):
        global walkcount
        if walkcount + 1 >= 12:
            walkcount = 0
        if click_status[pygame.K_d] == 1:
            screen.blit(walkRight[walkcount // 3], (self.x - 17, self.y - 7))
            walkcount += 1
        elif click_status[pygame.K_a] == 1:
            screen.blit(walkLeft[walkcount // 3], (self.x - 17, self.y - 7))
            walkcount += 1
        elif click_status[pygame.K_w] == 1 and click_status[pygame.K_d] == 0 and click_status[pygame.K_a] == 0:
            screen.blit(walkUP[walkcount // 3], (self.x - 17, self.y - 7))
            walkcount += 1
        elif click_status[pygame.K_s] == 1 and click_status[pygame.K_d] == 0 and click_status[pygame.K_a] == 0:
            screen.blit(walkDOWN[walkcount // 3], (self.x - 17, self.y - 7))
            walkcount += 1
        else:
            screen.blit(stand, (self.x - 17, self.y - 7))

    def step_fence(self, move, W=WIDTH, H=HEIGHT):
        if self.get_pos()[0] + move[0] < -1:
            move_x = 1
        elif self.get_pos()[0] + move[0] > W - self.hitbox.width:
            move_x = -1
        else:
            move_x = move[0]
        if self.get_pos()[1] + move[1] < -1:
            move_y = 1
        elif self.get_pos()[1] + move[1] > H - self.hitbox.height:
            move_y = -1
        else:
            move_y = move[1]
        self.hitbox.move_ip((move_x, move_y))
        self.set_pos(move_x, move_y)


class Bullet():
    def __init__(self, hero_pos_x, hero_pos_y, mouse_pos_x, mouse_pos_y):
        self.x = hero_pos_x + 20
        self.y = hero_pos_y + 30
        self.target_x = mouse_pos_x
        self.target_y = mouse_pos_y
        self.speed = 3
        self.radius = 5

    # calculate function using coordinates
    def culc_function(self):
        self.delta_y = self.target_y - self.y
        self.delta_x = self.target_x - self.x
        if self.delta_x == 0:
            self.delta_x = 1
        self.k = self.delta_y / self.delta_x
        self.b = self.y - self.k * self.x
        self.speed_of_change = (self.speed ** 2 / (1 + self.k ** 2)) ** 0.5

    def change_coord(self):
        if self.delta_x >= 0:
            self.x += self.speed_of_change
        else:
            self.x -= self.speed_of_change
        self.y = self.k * self.x + self.b

    def collide_with_unit(self, ghost):
        if self.x + self.radius > ghost.x and self.x - self.radius < ghost.x + ghost.hitbox.size[0]:
            if self.y + self.radius > ghost.y and self.y - self.radius < ghost.y + ghost.hitbox.size[1]:
                return True
