from random import randint
import pygame


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
    def __init__(self, health, speed, damage, agility, x, y):
        Unit.__init__(self, health, speed, damage, agility, x, y)
        self.hitbox = pygame.Rect(x, y, 40, 40)

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



