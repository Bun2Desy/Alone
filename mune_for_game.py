import pygame
import sys
from button import Button
from trymusic import Slider
from mech import hero_game
from info import *
from units import Hero
from settings import load_settings, read_settings
from sqll import get_score_database
from exceptions import InvalidDictionaryError, VolumeError, DifficultyError

pygame.init()

WIDTH, HEIGHT = 1013, 555
screen = pygame.display.set_mode([WIDTH, HEIGHT])

clock = pygame.time.Clock()

pygame.display.set_icon(icon)
pygame.display.set_caption(game_name)

pygame.mixer.music.load('menu/! rac.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(read_settings()['volume'])

USERNAME = ""


def start_the_game():
    """Display of creating a username
    :return: exist_name
    :rtype: bool
    """
    global USERNAME
    back_menu_button = Button(150, 325, 239, 48, 'Back', 'menu/button.png')

    input_name = 'nickname'
    smallfont = pygame.font.SysFont('Corbel', 32)
    exist_name = False

    while not exist_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(input_name) < 10:
                    if input_name == 'nickname' or input_name == 'at least 3 letters':
                        input_name = event.unicode
                    else:
                        input_name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(input_name) > 2 and input_name != 'nickname' and input_name != 'at least 3 letters':
                        USERNAME = input_name
                        exist_name = True
                        play_game()
                        lose_game()
                    else:
                        input_name = 'at least 3 letters'

            if event.type == pygame.USEREVENT and event.button == back_menu_button:
                main_menu()
            back_menu_button.handle_event(event)

        screen.fill((0, 0, 0))
        screen.blit(main_background, (-200, 0))
        text_name = smallfont.render(input_name, True, WHITE)
        screen.blit(text_name, (150, 250))
        back_menu_button.check_hover(pygame.mouse.get_pos())
        back_menu_button.draw(screen)

        pygame.display.update()


def play_game():
    """Displays gameplay
    :return: None
    """
    WIDTH, HEIGHT = 1000, 750
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    try:
        read_settings()
    except (InvalidDictionaryError, VolumeError, DifficultyError):
        default_data = {"volume": 0.5, "difficulty": "Normal"}
        load_settings(default_data)
    finally:
        hero = Hero(0, 0, 30, 60, USERNAME, read_settings()['difficulty'])
        while True:
            screen.fill((120, 120, 120))
            if hero_game(hero):
                break

            pygame.display.update()


def lose_game():
    """Displays game over
    :return: None
    """
    WIDTH, HEIGHT = 1013, 555
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    back_menu_button = Button(380, 450, 239, 48, 'Back', 'menu/button.png')
    while True:
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(fon_game_over, (WIDTH, HEIGHT)), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back_menu_button:
                main_menu()
            back_menu_button.handle_event(event)
        back_menu_button.check_hover(pygame.mouse.get_pos())
        back_menu_button.draw(screen)
        pygame.display.flip()


def main_menu():
    """Displays main menu
    :return: None
    """
    play_button = Button(150, 115, 239, 48, 'Play', 'menu/button.png')
    setting_button = Button(150, 215, 239, 48, 'Settings', 'menu/button.png')
    pedestal_button = Button(150, 315, 239, 48, 'Scoreboard', 'menu/button.png')
    quit_button = Button(150, 415, 239, 48, 'Quit', 'menu/button.png')

    while True:
        for event in pygame.event.get():
            screen.fill(BLACK)
            screen.blit(main_background, (-200, 0))
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == play_button:
                start_the_game()
            if event.type == pygame.USEREVENT and event.button == setting_button:
                setting_menu()
            if event.type == pygame.USEREVENT and event.button == pedestal_button:
                scoreboard_menu()
            if event.type == pygame.USEREVENT and event.button == quit_button:
                pygame.quit()
                sys.exit()

            for but in [play_button, setting_button, pedestal_button, quit_button]:
                but.handle_event(event)

        for but in [play_button, setting_button, pedestal_button, quit_button]:
            but.check_hover(pygame.mouse.get_pos())
            but.draw(screen)

        pygame.display.flip()


def scoreboard_menu():
    """Displays scoreboard  depending on the difficulty of game
    :return: None
    """
    smallfont = pygame.font.SysFont('Corbel', 20)
    back_menu_button = Button(150, 450, 239, 48, 'Back', 'menu/button.png')
    try:
        read_settings()
    except (InvalidDictionaryError, VolumeError, DifficultyError):
        default_data = {"volume": 0.5, "difficulty": "Normal"}
        load_settings(default_data)
    finally:
        table = get_score_database(read_settings()['difficulty'])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == back_menu_button:
                    main_menu()
                back_menu_button.handle_event(event)
            back_menu_button.check_hover(pygame.mouse.get_pos())
            back_menu_button.draw(screen)
            screen.blit(smallfont.render(read_settings()['difficulty'], True, RED), (110, 50))
            next_indent = 0
            for result in range(len(table)):
                screen.blit(smallfont.render(str(result + 1), True, WHITE), (70, 90 + next_indent))
                screen.blit(smallfont.render(str(table[result][0]), True, WHITE), (100, 90 + next_indent))
                screen.blit(smallfont.render(str(table[result][1]), True, WHITE), (200, 90 + next_indent))
                next_indent += 30
            pygame.display.flip()


def setting_menu():
    """Displays setting menu
    :return: None
    """
    music_button = Button(150, 125, 239, 48, 'Music', 'menu/button.png')
    difficulty_button = Button(150, 225, 239, 48, 'Difficulty', 'menu/button.png')
    back_menu_button = Button(150, 325, 239, 48, 'Back', 'menu/button.png')

    screen.fill(BLACK)
    screen.blit(main_background, (-200, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back_menu_button:
                main_menu()
            if event.type == pygame.USEREVENT and event.button == music_button:
                music_settings()
            if event.type == pygame.USEREVENT and event.button == difficulty_button:
                difficulty_settings()
            for but in [music_button, difficulty_button, back_menu_button]:
                but.handle_event(event)
        for but in [music_button, difficulty_button, back_menu_button]:
            but.check_hover(pygame.mouse.get_pos())
            but.draw(screen)

        pygame.display.flip()


def music_settings():
    """Displays music settings and changes volume
    :return: None
    """
    screen.fill(BLACK)
    screen.blit(main_background, (-200, 0))
    try:
        read_settings()
    except (InvalidDictionaryError, VolumeError, DifficultyError):
        default_data = {"volume": 0.5, "difficulty": "Normal"}
        load_settings(default_data)
    data = read_settings()
    volume = data['volume']

    music_slider = Slider((250, 185), (250, 20), volume, 0, 100)
    back_button = Button(150, 325, 239, 48, 'Back', 'menu/button.png')

    smallfont = pygame.font.SysFont('Corbel', 30)
    text = smallfont.render('Volume', True, WHITE)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back_button:
                data['volume'] = music_slider.initial_val
                load_settings(data)
                setting_menu()
            if music_slider.container_rect.collidepoint(mouse_pos):
                if mouse[0]:
                    music_slider.grabbed = True
            if not mouse[0]:
                music_slider.grabbed = False
            if music_slider.button_rect.collidepoint(mouse_pos):
                music_slider.hover()
            if music_slider.grabbed:
                music_slider.move_slider(mouse_pos)
                music_slider.hover()
            else:
                music_slider.hovered = False
            back_button.handle_event(event)
        screen.fill(BLACK)
        screen.blit(main_background, (-200, 0))
        screen.blit(text, (30, 167))
        music_slider.render()
        music_slider.display_value()
        back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(screen)

        pygame.display.flip()


def difficulty_settings():
    """Displays difficulty settings and changes difficulty
    :return: None
    """
    screen.fill(BLACK)
    screen.blit(main_background, (-200, 0))
    Normal_button = Button(150, 125, 239, 48, 'Normal', 'menu/button.png', 'Normal')
    Hard_button = Button(150, 225, 239, 48, 'Hard', 'menu/button.png', 'Hard')
    Hardcore_button = Button(150, 325, 239, 48, 'Hardcore', 'menu/button.png', 'Hardcore')
    back_button = Button(150, 425, 239, 48, 'Back', 'menu/button.png')
    try:
        read_settings()
    except (InvalidDictionaryError, VolumeError, DifficultyError):
        default_data = {"volume": 0.5, "difficulty": "Normal"}
        load_settings(default_data)
    data = read_settings()
    difficulty = data['difficulty']
    clickbut1 = 0
    clickbut2 = 0
    clickbut3 = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back_button:
                data['difficulty'] = difficulty
                load_settings(data)
                main_menu()
            if event.type == pygame.USEREVENT and event.button == Normal_button:
                difficulty = 'Normal'
                clickbut1 = 1
                clickbut2 = 0
                clickbut3 = 0
            if event.type == pygame.USEREVENT and event.button == Hard_button:
                difficulty = 'Hard'
                clickbut1 = 0
                clickbut2 = 1
                clickbut3 = 0
            if event.type == pygame.USEREVENT and event.button == Hardcore_button:
                difficulty = 'Hardcore'
                clickbut1 = 0
                clickbut2 = 0
                clickbut3 = 1
            for but in [Normal_button, Hard_button, Hardcore_button, back_button]:
                but.handle_event(event)
        for but in [(Normal_button, clickbut1), (Hard_button, clickbut2), (Hardcore_button, clickbut3)]:
            but[0].check_hover(pygame.mouse.get_pos())
            but[0].draw2(screen, but[1], difficulty)
        back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
