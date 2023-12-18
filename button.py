import pygame
from pygame import *
from info import *

class Button:
    """Button object
    :param image: button image
    :type image: pygame.surface.Surface
    :param rect: rect for button
    :type rect: pygame.rect.Rect
    :param is_hovered: status of hover for button
    :type is_hovered: bool
    """
    def __init__(self, x, y, width, height, text, image_path, difficulty=None):
        """Creates button object
        :param x: x coordinate top-left
        :type x: int
        :param y: y coordinate top-left
        :type y: int
        :param width: button width
        :type width: int
        :param height: button height
        :type height: int
        :param text: name of button
        :type text: str
        :param image_path: image_path for button image
        :type image_path: str
        :param difficulty: game difficulty
        :type difficulty: str
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hovered = False
        if difficulty != None:
            self.difficulty = difficulty

    def draw(self, screen):
        """Draws button on display of game
        :param screen: display of game
        :type screen: pygame.surface.Surface
        :returns: None
        """
        screen.blit(self.image, self.rect.topleft)

        font = pygame.font.SysFont('Corbel', 32)
        text_view = font.render(self.text, True, RED) if self.is_hovered else font.render(self.text, True,
                                                                                                  WHITE)
        text_rect = text_view.get_rect(center=self.rect.center)
        screen.blit(text_view, text_rect)

    def draw2(self, screen, clickbutton, difficulty):
        """Draws button on display of game with click condition
        :param screen: display of game
        :type screen: pygame.surface.Surface
        :param clickbutton: pressed button
        :type clickbutton: int
        :param difficulty: difficulty of game
        :type difficulty: str
        :returns: None
        """
        screen.blit(self.image, self.rect.topleft)

        font = pygame.font.SysFont('Corbel', 32)
        text_view = font.render(self.text, True,
                                (204, 0, 0)) if clickbutton == 1 or difficulty == self.difficulty else font.render(
            self.text, True, WHITE)
        text_rect = text_view.get_rect(center=self.rect.center)
        screen.blit(text_view, text_rect)

    def check_hover(self, mouse_pos):
        """Checks the mouse posing on the button
        :param mouse_pos: position of mouse
        :type mouse_pos: tuple
        :returns: None
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        """Places a new event on the queue
        :param event: event
        :type event: pygame.event.Event
        :returns: None
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
