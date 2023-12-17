rom random import randint, choices
import pygame
from info import *



class Unit():
    def __init__(self, x, y):
        '''Assigns coordinate values and create unit objects
        :param x: x-axis coordinate
        :type x: float
        :param y: y-axis coordinate
        :type y: float
        :returns: None
        :raises InvalidCoordinatesError: if x
        '''
        self.speed = 3
        self.is_dead = False
        self.x = x
        self.y = y

    def set_pos(self, x, y):
        self.x += x
        self.y += y

    def get_pos(self):
        return (self.x, self.y)


class Ghost(Unit):
    def __init__(self, x, y, hitbox_width, hitbox_height):
        Unit.__init__(self, x, y)
        self.speed = 1
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
    def __init__(self, x, y, hitbox_width, hitbox_heigth, name, difficulty):
        Unit.__init__(self, x, y)
        if difficulty == "Normal":
            self.health = 3
        elif difficulty == "Hard":
            self.health = 2
        else:
            self.health = 1
        self.mana = 5
        self.hitbox = pygame.Rect(x, y, hitbox_width, hitbox_heigth)
        self.name = name
        self.score = 0
        self.difficulty = difficulty

    def start_pos(self, x, y):
        self.x = x
        self.y = y
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def do_shoot(self):
        self.mana -= 1

    def restore_mana(self):
        self.mana += 2
        if self.mana > 5:
            self.mana = 5

    def redrawgamehero(self):
        global walkcount
        if walkcount + 1 >= 12:
            walkcount = 0
        if click_status[pygame.K_d] == 1:
            screen.blit(walkRight[walkcount // 3], (self.x - 25, self.y - 15))
            walkcount += 1
        elif click_status[pygame.K_a] == 1:
            screen.blit(walkLeft[walkcount // 3], (self.x - 25, self.y - 15))
            walkcount += 1
        elif click_status[pygame.K_w] == 1 and click_status[pygame.K_d] == 0 and click_status[pygame.K_a] == 0:
            screen.blit(walkUP[walkcount // 3], (self.x - 25, self.y - 15))
            walkcount += 1
        elif click_status[pygame.K_s] == 1 and click_status[pygame.K_d] == 0 and click_status[pygame.K_a] == 0:
            screen.blit(walkDOWN[walkcount // 3], (self.x - 25, self.y - 15))
            walkcount += 1
        else:
            screen.blit(stand, (self.x - 25, self.y - 15))

    def draw_health(self, screen):
        if self.difficulty == "Normal":
            if self.health == 3:
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 120, 10))
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 90, 10))
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 60, 10))
            elif self.health == 2:
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 120, 10))
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 90, 10))
                screen.blit(pygame.transform.scale(pygame.image.load('objects/mybroken_heart.png'), (70, 70)),
                            (WIDTH - 60, 10))
            elif self.health == 1:
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 120, 10))
                screen.blit(pygame.transform.scale(pygame.image.load('objects/mybroken_heart.png'), (70, 70)),
                            (WIDTH - 90, 10))
                screen.blit(pygame.transform.scale(pygame.image.load('objects/mybroken_heart.png'), (70, 70)),
                            (WIDTH - 60, 10))
        elif self.difficulty == "Hard":
            if self.health == 2:
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 90, 10))
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 60, 10))
            elif self.health == 1:
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 90, 10))
                screen.blit(pygame.transform.scale(pygame.image.load('objects/mybroken_heart.png'), (70, 70)),
                            (WIDTH - 60, 10))
        else:
            if self.health == 1:
                screen.blit(pygame.transform.scale(pygame.image.load('objects/heart.png'), (70, 70)), (WIDTH - 60, 10))

    def draw_mana(self, screen):
        start_coord = 60
        for i in range(5 - self.mana):
            screen.blit(pygame.transform.scale(pygame.image.load('objects/lack_of_mana_point.png'), (70, 70)),
                        (WIDTH - start_coord, 30))
            start_coord += 30
        for i in range(self.mana):
            screen.blit(pygame.transform.scale(pygame.image.load('objects/mana_point.png'), (70, 70)),
                        (WIDTH - start_coord, 30))
            start_coord += 30

    def step_fence(self, move, blocks):
        for i in blocks:
            if i.colliderect(self.hitbox):
                move_x = -move[0]
                move_y = -move[1]
                self.hitbox.move_ip((move_x, move_y))
                self.set_pos(move_x, move_y)
                break


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
        return False

    def collide_with_wall(self, blocks):
        for b in blocks:
            if b.collidepoint(self.x, self.y):
                return True
        return False


class Item():
    def __init__(self, item_type, x, y):
        if item_type == 'key':
            self.image = pygame.image.load("objects/key.png")
        elif item_type == 'chakra':
            self.image = pygame.image.load("objects/chakra.png")
        self.rect = self.image.get_rect()
        self.type = item_type
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

    def render(self):
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)

    def casino(self):
        chance = choices([True, False], weights=[50, 50])
        return chance

    def collision(self, hero):
        if self.hitbox.colliderect(hero.hitbox):
            if self.type == 'chakra':
                hero.restore_mana()
                Items.remove(self)
            if self.type == 'key':
                Items.remove(self)
                return True


class Door:
    def __init__(self, type_door, door_box):
        self.type_door = type_door
        self.door_box = door_box

    def draw(self, hero, open_door):
        if self.type_door == 'exit_door':
            if self.openy(hero, open_door):
                self.image = pygame.transform.scale(pygame.image.load('objects/open_door.png'),
                                                    (self.door_box.width, self.door_box.height))
                screen.blit(self.image, (self.door_box.x, self.door_box.y))
            else:
                self.image = pygame.transform.scale(pygame.image.load('objects/close_door.png'),
                                                    (self.door_box.width, self.door_box.height))
                screen.blit(self.image, (self.door_box.x, self.door_box.y))
        else:
            self.image = pygame.transform.scale(pygame.image.load('objects/enter_door.png'),
                                                (self.door_box.width, self.door_box.height))
            screen.blit(self.image, (self.door_box.x, self.door_box.y))

    def openy(self, hero, open_door):
        if self.door_box.colliderect(hero.hitbox) and open_door:
            return True


class Score:
    def __init__(self, kills, room_number):
        self.kills = kills
        self.room_number = room_number
        self.smallfont = pygame.font.SysFont('Corbel', 20)

    def kill_and_room_count(self, screen):
        screen.blit(self.smallfont.render('kills:' + str(self.kills), True, (0, 0, 0)), (WIDTH - 100, 90))
        screen.blit(self.smallfont.render('room' + ' №' + str(self.room_number), True, (0, 0, 0)), (WIDTH - 100, 110))
