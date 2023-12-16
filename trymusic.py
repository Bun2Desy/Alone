import pygame
import sys
pygame.init()

WIDTH,HEIGHT=1013,555
screen=pygame.display.set_mode([WIDTH, HEIGHT])

main_background=pygame.image.load('background-menu.png')

pygame.mixer.music.load('! rac.mp3')
pygame.mixer.music.play(-1)

font_type=pygame.font.SysFont('Corbel', 30)
selected=(255,0,0)
unselected=(255, 255, 255)
Buttonstates={True: selected, False: unselected}

class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10,
                                       self.size[1])

        # label
        self.text =font_type.render(str(int(self.get_value())), True, (255,255,255))
        self.label_rect = self.text.get_rect(center=(self.pos[0], self.slider_top_pos - 15))

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self):
        self.hovered = True

    def render(self):
        pygame.draw.rect(screen, (104, 106, 113), self.container_rect)
        pygame.draw.rect(screen, Buttonstates[self.hovered], self.button_rect)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min

    def display_value(self):
        self.text = font_type.render(str(int(self.get_value())), True, (255, 255, 255))
        screen.blit(self.text, self.label_rect)
        pygame.mixer.music.set_volume(self.get_value()*0.01)

