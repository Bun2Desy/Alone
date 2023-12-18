import pygame
from info import *

pygame.init()

pygame.mixer.music.load('menu/! rac.mp3')
pygame.mixer.music.play(-1)

font_type = pygame.font.SysFont('Corbel', 30)
selected = (255, 0, 0)
unselected = (255, 255, 255)
states = {True: selected, False: unselected}


class Slider:
    """Slider object
    :param slider_left_pos: left x coordinate of slider
    :type slider_left_pos: int
    :param slider_right_pos: right x coordinate of slider
    :type slider_right_pos: int
    :param slider_top_pos: top y coordinate of slider
    :type slider_top_pos: int
    :param initial_pos: start position relative length of c
    :type initial_pos: float
    :param container_rect: rect for container
    :type container_rect: RectType
    :param button_rect: slider rect
    :type button_rect: RectType
    :param hovered: status of hover for button
    :type hovered: bool
    :param grabbed: status of grabbed for button
    :type grabbed: bool
    :param text: text of volume value
    :type text: pygame.surface.Surface
    :param label.rect: rect for text
    :type label_rect: RectType
    """
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int):
        """Creates slider object
        :param pos: center position
        :type pos: tuple
        :param size: size of container
        :type size: tuple
        :param initial_val: start value of volume
        :type initial_val: float
        :param min: minimum value of volume
        :type min: int
        :param max: maximum value of volume
        :type max: int
        """
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_pos = (self.slider_right_pos - self.slider_left_pos) * initial_val
        self.initial_val=initial_val


        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_pos - 5, self.slider_top_pos, 10,
                                       self.size[1])




    def move_slider(self, mouse_pos):
        """Changes position of slider
        :param mouse_pos: position of mouse
        :type mouse_pos: tuple
        :returns: None
        """
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self):
        """Changes hover status
        :returns: None
        """
        self.hovered = True

    def render(self):
        """Draws all detail of slider
        :returns: None
        """
        pygame.draw.rect(screen, (104, 106, 113), self.container_rect)
        pygame.draw.rect(screen, states[self.hovered], self.button_rect)

    def get_value(self):
        """Gives volume_val
        :returns: volume_val
        :rtype: float
        """
        len_container = self.slider_right_pos - self.slider_left_pos
        button_pos = self.button_rect.centerx - self.slider_left_pos
        self.initial_val = (self.button_rect.centerx - self.slider_left_pos) / (self.slider_right_pos - self.slider_left_pos)
        volume_val=(button_pos / len_container) * (self.max - self.min) + self.min
        return volume_val

    def display_value(self):
        """Draws text of volume_value
        :returns: None
        """
        self.text = font_type.render(str(int(self.get_value())), True, WHITE)
        self.label_rect = self.text.get_rect(center=(self.pos[0], self.slider_top_pos - 15))
        screen.blit(self.text, self.label_rect)
        pygame.mixer.music.set_volume(self.get_value() * 0.01)

