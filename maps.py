import random
from units import Door
import pygame


def maps_generation():
    """Creates randomly blocks for map, chooses randomly places for 2 doors
    :returns: blocks, blocks_without_door, enter_door, exit_door
    :rtypes: list, list, pygame.rect.Rect, pygame.rect.Rect
    """
    # fence
    indent = (80, 20)
    fence_size = (720, 720)  # fence_size // block_size
    fence = pygame.Rect(indent[0], indent[1], fence_size[0], fence_size[1])

    start_x = indent[0]
    start_y = indent[1]

    checkpoint = (0, 0, 0)
    block_size = 60
    end_x = start_x + block_size
    end_y = start_y

    box = pygame.Rect(start_x, start_y, block_size, block_size)
    blocks = []
    blocks = blocks + [box]
    blocks.append(pygame.Rect(end_x, end_y, block_size, block_size))

    cannt_be_door = []
    box = pygame.Rect(start_x, start_y, block_size, block_size)
    cannt_be_door.append(box)

    while (end_x, end_y) != (start_x, start_y + block_size):
        if end_x == (fence.width + fence.x) - block_size:
            checkpoint = (1, 0, 0)
            if blocks[-2] == pygame.Rect(end_x - block_size, end_y, block_size, block_size):
                cannt_be_door.append(pygame.Rect(end_x, end_y, block_size, block_size))
                end_x = end_x
                end_y += block_size
                blocks.append(pygame.Rect(end_x, end_y, block_size, block_size))
                continue
            if blocks[-3] == pygame.Rect(end_x - 2 * block_size, end_y, block_size, block_size):
                cannt_be_door.append(blocks[-2])
        if end_y == (fence.height + fence.y) - block_size:
            checkpoint = (0, 1, 0)
            if blocks[-2] == pygame.Rect(end_x, end_y - block_size, block_size, block_size):
                cannt_be_door.append(pygame.Rect(end_x, end_y, block_size, block_size))
        if end_x == start_x and end_y != start_y:
            checkpoint = (0, 0, 1)
            if blocks[-2] == pygame.Rect(end_x + block_size, end_y, block_size, block_size):
                cannt_be_door.append(pygame.Rect(end_x, end_y, block_size, block_size))
        if checkpoint == (0, 0, 0):
            end_x += block_size
            end_y += random.choice([0, block_size])
        elif checkpoint == (1, 0, 0):
            end_x += random.choice([0, -block_size])
            end_y += block_size
        elif checkpoint == (0, 1, 0):
            flag = False
            for box in blocks:
                if box.colliderect(pygame.Rect(end_x - 2 * block_size, end_y - 3 * block_size, 3 * block_size,
                                               3 * block_size)):
                    flag = True
                    break
            if flag:
                end_x -= block_size
                end_y = end_y
            else:
                end_x -= block_size
                end_y += random.choice([0, -block_size])
        elif checkpoint == (0, 0, 1):
            end_x = end_x
            end_y -= block_size

        if pygame.Rect(end_x, end_y, block_size, block_size).colliderect(fence) and pygame.Rect(end_x, end_y,
                                                                                                block_size,
                                                                                                block_size) not in \
                blocks:
            blocks.append(pygame.Rect(end_x, end_y, block_size, block_size))
    no_enter_door = True
    no_exit_door = True
    while no_enter_door:
        i = random.choice(blocks)
        if i not in cannt_be_door:
            door1_x = i.x
            door1_y = i.y
            no_enter_door = False
    while no_exit_door:
        i = random.choice(blocks)
        if i not in cannt_be_door:
            door2_x = i.x
            door2_y = i.y
            if door2_x != door1_x and door2_y != door1_y:
                no_exit_door = False
    doors = [(door1_x, door1_y), (door2_x, door2_y)]
    block_for_door = []
    for d in doors:
        right = 0
        left = 0
        up = 0
        down = 0
        for b in blocks:
            if b.y == d[1] and b.x < d[0]:
                left += 1
            if b.y == d[1] and b.x > d[0]:
                right += 1
            if b.x == d[0] and b.y < d[1]:
                up += 1
            if b.x == d[0] and b.y > d[1]:
                down += 1
        if left == 0:
            block_for_door.append(pygame.Rect(d[0] - block_size, d[1], block_size, block_size))
        if right == 0:
            block_for_door.append(pygame.Rect(d[0] + block_size, d[1], block_size, block_size))
        if up == 0:
            block_for_door.append(pygame.Rect(d[0], d[1] - block_size, block_size, block_size))
        if down == 0:
            block_for_door.append(pygame.Rect(d[0], d[1] + block_size, block_size, block_size))
        blocks = blocks + block_for_door
        blocks_without_door = [x for x in blocks]
        blocks_without_door.remove(
            pygame.Rect(door1_x, door1_y, block_size, block_size))
        blocks_without_door.remove(pygame.Rect(door2_x, door2_y, block_size, block_size))

        enter_door = Door('enter_door',
                          pygame.Rect(door1_x, door1_y, block_size, block_size))
        exit_door = Door('exit_door',
                         pygame.Rect(door2_x, door2_y, block_size, block_size))

    return blocks, blocks_without_door, enter_door, exit_door