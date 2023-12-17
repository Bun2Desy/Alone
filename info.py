import pygame

# color_rgb
RED = (204, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)
YELLOW = (255, 255, 153)
BLACK=(0,0,0)

# screen
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
FPS = 60

# background-menu, icon, game-name
game_name='Alone'
icon = pygame.image.load('menu/icon2.png')
main_background = pygame.image.load('menu/background-menu.png')


#map
block_size = 60
fence_size = (720, 720)
indent = (80, 20)
# enemy
enemi = []
ghost_timer = pygame.USEREVENT + 1

# items
Items = []

# bullets
bullets = []
bullet_radius = 5
# room
open_door = False

# move_button_status
click_status = {pygame.K_w: 0, pygame.K_s: 0, pygame.K_d: 0, pygame.K_a: 0}
move = (0, 0)
walkcount = 0

# move_sprites_lists_hero
walkRight = [pygame.transform.scale(pygame.image.load('right/Sprite1.png'), (80, 80)),
             pygame.transform.scale(pygame.image.load(
                 'right/Sprite2.png'), (80, 80)),
             pygame.transform.scale(pygame.image.load('right/Sprite3.png'), (80, 80)),
             pygame.transform.scale(pygame.image.load(
                 'right/Sprite4.png'), (80, 80))]
walkLeft = [pygame.transform.scale(pygame.image.load('left/LSprite1.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'left/LSprite2.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('left/LSprite3.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load(
                'left/LSprite4.png'), (80, 80))]
walkUP = [pygame.transform.scale(pygame.image.load('up/UpSprite1.png'), (80, 80)),
          pygame.transform.scale(pygame.image.load(
              'up/UpSprite2.png'), (80, 80)), pygame.transform.scale(pygame.image.load('up/UpSprite3.png'), (80, 80)),
          pygame.transform.scale(pygame.image.load(
              'up/UpSprite4.png'), (80, 80)), pygame.transform.scale(pygame.image.load('up/UpSprite5.png'), (80, 80)),
          pygame.transform.scale(pygame.image.load(
              'up/UpSprite6.png'), (80, 80)), pygame.transform.scale(pygame.image.load('up/UpSprite7.png'), (80, 80)),
          pygame.transform.scale(pygame.image.load(
              'up/UpSprite8.png'), (80, 80))]
walkDOWN = [pygame.transform.scale(pygame.image.load('down/DoSprite1.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('down/DoSprite2.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('down/DoSprite3.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('down/DoSprite4.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('down/DoSprite5.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('down/DoSprite6.png'), (80, 80))]
stand = pygame.transform.scale(pygame.image.load('stand/Sprite-0003.png'), (80, 80))

# move_sprites_lists_ghost
ghost_sprite = pygame.transform.scale(pygame.image.load('enemy/ghostmove4.png'), (80, 80))
