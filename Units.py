from random import randint, choices
import pygame
from info import *


class Unit():
    '''Unit object
    :param x: unit x-axis coordinate
    :type x: int
    :param y: unit y-axis coordinate
    :type y: int
    :param speed: unit speed
    :type speed: int
    :param is_dead: death status of unit
    :type is_dead: bool
    '''
    def __init__(self, x, y):
        '''Assigns coordinate values and create unit objects
        :param x: x-axis coordinate
        :type x: int
        :param y: y-axis coordinate
        :type y: int
        :returns: None
        :raises InvalidCoordinatesError: if x or y out of screen size
        '''
        self.speed = 3
        self.is_dead = False
        self.x = x
        self.y = y

    def set_pos(self, x, y):
        '''Changes coordinates due to using move_vector=(x,y)
        :param x: x-axis coordinate of vector
        :type x: int
        :param y: y-axis coordinate of vector
        :type y: int
        :returns: None
        '''
        self.x += x
        self.y += y

    def get_pos(self):
        '''Gives Unit position
        :returns: (self.x,self.y)
        :rtype: tuple
        '''
        return (self.x, self.y)


class Ghost(Unit):
    '''Enemy object
    :param hitbox: enemy hitbox
    :type hitbox: pygame.rect.Rect
    '''
    def __init__(self, x, y, hitbox_width, hitbox_height):
        '''Assigns coordinate values and create unit objects
        :param x: x-axis coordinate
        :type x: int
        :param y: y-axis coordinate
        :type y: int
        :param hitbox_width: hitbox width
        :type hitbox_width: int
        :param hitbox_height: hitbox height
        :type hitbox_height: int
        :returns: None
        '''
        Unit.__init__(self, x, y)
        self.speed = 1
        self.hitbox = pygame.Rect(x, y, hitbox_width, hitbox_height)

    def chase(self, hero_x, hero_y):
        '''Changes ghost position relative to hero_x and hero_y
        :param hero_x: x-axis hero coordinate
        :type hero_x: int
        :param hero_y: y-axis hero coordinate
        :type hero_y: int
        :returns: None
        '''
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
    '''Hero object
    :param hitbox: hero hitbox
    :type hitbox: pygame.rect.Rect
    :param mana: hero mana
    :type mana: int
    :param name: hero name
    :type name: str
    :param difficulty: game difficulty
    :type difficulty: str
    '''
    def __init__(self, x, y, hitbox_width, hitbox_heigth, name, difficulty):
        '''Create hero object
        :param x: x-axis coordinate
        :type x: int
        :param y: y-axis coordinate
        :type y: int
        :param hitbox_width: width hero hitbox
        :type hitbox_width: int
        :param hitbox_heigth: heigth hero hitbox
        :type hitbox_heigth: int
        :param name: hero name
        :type name: str
        :param difficulty: game difficulty
        :type difficulty: str
        '''
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
        self.difficulty = difficulty

    def start_pos(self, x, y):
        '''Changes hero position to (x,y)
        :param x: x-axis coordinate
        :type x: int
        :param y: y-axis coordinate
        :type y: int
        :returns: None
        :raises InvalidCoordinatesError: if x or y out of display size
        '''
        self.x = x
        self.y = y
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def do_shoot(self):
        '''Subtracts one point from mana
        :returns: None
        '''
        self.mana -= 1

    def restore_mana(self):
        '''Adds points to mana
        :returns: None
        '''
        self.mana += 2
        if self.mana > 5:
            self.mana = 5

    def redrawgamehero(self, screen):
        '''Draws moving sprites of hero on display of game
        :param screen: display of game
        :type screen: pygame.surface.Surface
        :returns: None
        '''
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
        '''Draws hearts sprites of hero on display of game
        :param screen: display of game
        :type screen: pygame.surface.Surface
        :returns: None
        '''
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
        '''Draws mana points on display of game
        :param screen: display of game
        :type screen: pygame.surface.Surface
        :returns: None
        '''
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
        '''Checks for contact with walls and prohibition to enter them
        :param move: coordinates of hero
        :type move: tuple
        :param blocks: map blocks
        :type blocks: list
        :returns: None
        '''
        for i in blocks:
            if i.colliderect(self.hitbox):
                move_x = -move[0]
                move_y = -move[1]
                self.hitbox.move_ip((move_x, move_y))
                self.set_pos(move_x, move_y)
                break


class Bullet():
    '''Bullet object
    :param x: generation bullet x position
    :type x: int
    :param y: generation bullet y position
    :type y: int
    :param target_x: target x position
    :type target_x: int
    :param target_y: target y position
    :type target_y: int
    :param speed: bullet speed
    :type speed: int
    :param radius: bullet radius
    :type radius: int
    '''
    def __init__(self, hero_pos_x, hero_pos_y, mouse_pos_x, mouse_pos_y):
        '''Create bullet object
        :param hero_pos_x: x hero position
        :type hero_pos_x: int
        :param hero_pos_y: y hero position
        :type hero_pos_y: int
        :param mouse_pos_x: mouse x position
        :type mouse_pos_x: int
        :param mouse_pos_y: mouse y position
        :type mouse_pos_y: int
        '''
        self.x = hero_pos_x + 20
        self.y = hero_pos_y + 30
        self.target_x = mouse_pos_x
        self.target_y = mouse_pos_y
        self.speed = 3
        self.radius = 5

    # calculate function using coordinates
    def culc_function(self):
        '''Culculate function of bullet movement
        :returns: None
        '''
        self.delta_y = self.target_y - self.y
        self.delta_x = self.target_x - self.x
        if self.delta_x == 0:
            self.delta_x = 1
        self.k = self.delta_y / self.delta_x
        self.b = self.y - self.k * self.x
        self.speed_of_change = (self.speed ** 2 / (1 + self.k ** 2)) ** 0.5

    def change_coord(self):
        '''Change bullet coordinate using function of bullet movement
        :returns: None
        '''
        if self.delta_x >= 0:
            self.x += self.speed_of_change
        else:
            self.x -= self.speed_of_change
        self.y = self.k * self.x + self.b

    def collide_with_unit(self, ghost):
        '''Check collision bullet with unit
        :param ghost: enemy object
        :type ghost: Ghost
        :returns: detect collision
        :rtype: bool
        '''
        if self.x + self.radius > ghost.x and self.x - self.radius < ghost.x + ghost.hitbox.size[0]:
            if self.y + self.radius > ghost.y and self.y - self.radius < ghost.y + ghost.hitbox.size[1]:
                return True
        return False

    def collide_with_wall(self, blocks):
        '''Check collision bullet with wall
        :param blocks: blocks wall
        :type blocks:
        :returns: detect collision
        :rtype: bool
        '''
        for b in blocks:
            if b.collidepoint(self.x, self.y):
                return True
        return False


class Item():
    '''Item object
    :param x: item x position
    :type x: int
    :param y: item y position
    :type y: int
    :param image: item image
    :type image: pygame.surface.Surface
    :param rect: image hitbox
    :type rect: pygame.rect.Rect
    :param type: chakra or key
    :type type: str
    :param hitbox: item hitbox
    :type hitbox: pygame.rect.Rect
    '''
    def __init__(self, item_type, x, y):
        '''Create Item object
        :param item_type: chakra or key
        :type item_type: str
        :param x: item x position
        :type x: int
        :param y: item y position
        :type y: int
        :returns: None
        '''
        if item_type == 'key':
            self.image = pygame.image.load("objects/key.png")
        elif item_type == 'chakra':
            self.image = pygame.image.load("objects/chakra.png")
        self.rect = self.image.get_rect()
        self.type = item_type
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

    def render(self, screen):
        '''Draws objects from class Item
        :param screen: display of game
        :type screen: pygame.surface.Surface
        :returns: None
        '''
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)

    def casino(self):
        '''Calculates the probability of a drop
        :returns: chance
        :rtype: list
        '''
        chance = choices([True, False], weights=[50, 50])
        return chance

    def collision(self, hero):
        '''Return True if type=='key' and removes items from display
        :param hero: hero object
        :type hero: Hero
        :returns: True
        :rtype: bool
        '''
        if self.hitbox.colliderect(hero.hitbox):
            if self.type == 'chakra':
                hero.restore_mana()
                Items.remove(self)
            if self.type == 'key':
                Items.remove(self)
                return True


class Door:
    '''Door object
    :param type_door: exit or enter
    :type type_door: str
    :param door_box: door hitbox
    :type door_box: pygame.rect.Rect
    :param image: door image
    :param image: pygame.surface.Surface
    '''
    def __init__(self, type_door, door_box):
        '''Create Door object
        :param type_door: exit or enter
        :type type_door: str
        :param door_box: door hitbox
        :type door_box: pygame.rect.Rect
        '''
        self.type_door = type_door
        self.door_box = door_box

    def draw(self, hero, open_door):
        '''Draws door sprites on display of game
        :param hero: hero object
        :type hero: Hero
        :param open_door: door openness
        :type open_door: bool
        :returns: None
        '''
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
        '''Returns True if collision between hero hitbox and door object
        :param hero: hero object
        :type hero: Hero
        :param open_door: door openness
        :type open_door: bool
        :returns: True
        :rtype: bool
        '''
        if self.door_box.colliderect(hero.hitbox) and open_door:
            return True


class Score:
    '''Score counter
    :param kills: killed ghosts count
    :type kills: int
    :param room_number: room number
    :type room_number: int
    :param smallfont: text font
    :type smallfont: pygame.font.Font
    '''
    def __init__(self, kills, room_number):
        '''Create Score object
        :param kills: killed ghosts count
        :type kills: int
        :param room_number: room number
        :type room_number: int
        :returns: None
        '''
        self.kills = kills
        self.room_number = room_number
        self.smallfont = pygame.font.SysFont('Corbel', 20)

    def kill_and_room_count(self, screen):
        '''Draws count of kills and room number on display of game
        :param screen: display of game
        :type screen: pygame.surface.Surface
        :returns: None
        '''
        screen.blit(self.smallfont.render('kills:' + str(self.kills), True, (0, 0, 0)), (WIDTH - 100, 90))
        screen.blit(self.smallfont.render('room' + ' №' + str(self.room_number), True, (0, 0, 0)), (WIDTH - 100, 110))
