import numpy as np
import random
import pygame
import sys
from pygame.locals import *

SIZE = (600, 600)

DIRT_COLOR = [0, 0, 0]
TREE_COLOR = [0, 255, 0]
FIRE_COLOR = [255, 0, 0]
CENDER_COLOR = [255, 255, 255]

INIT_TREE_PROBA = "GAUSS"  # ou RAND


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return


def initialisation_forest(map, dim_map, nb_tree_init):
    if INIT_TREE_PROBA == "GAUSS":
        print('GAUSS INIT')
    elif INIT_TREE_PROBA == "RAND":
        print('RAND INIT')
    for tree in range(nb_tree_init):
        if INIT_TREE_PROBA == "GAUSS":
            x = -1
            y = -1
            while not (0 <= x <= dim_map[0]-1 and 0 <= y <= dim_map[1]-1):
                x = int(random.gauss(dim_map[0]/2, dim_map[0]/5))
                y = int(random.gauss(dim_map[1]/2, dim_map[1]/5))
        elif INIT_TREE_PROBA == "RAND":
            x = random.randint(0, dim_map[0]-1)
            y = random.randint(0, dim_map[1]-1)
        pos_tree = (x, y)
        map[pos_tree[0], pos_tree[1]] = TREE_COLOR
    return map


def initialisation_fire(map, dim_map):
    pos_fire = (random.randint(0, dim_map[0] - 1), random.randint(0, dim_map[1] - 1))
    map[pos_fire[0], pos_fire[1]] = FIRE_COLOR
    return map


def nb_voisin_in_fire(map, pos_cell, dim_map):
    voisin_in_fire = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if [i, j] != [0, 0]:
                if 0 <= pos_cell[0]+i < dim_map[0] and 0 <= pos_cell[1]+j < dim_map[1]:
                    if np.array_equal(map[pos_cell[0]+i, pos_cell[1]+j], FIRE_COLOR):
                        voisin_in_fire += 1
    return voisin_in_fire


def create_map_voisin_in_fire(map, dim_map):
    map_voisin_in_fire = np.zeros((dim_map[0], dim_map[1]))
    for i in range(dim_map[0]):
        for j in range(dim_map[1]):
            pos_cell = (i, j)
            map_voisin_in_fire[i, j] = nb_voisin_in_fire(map, pos_cell, dim_map)
    return map_voisin_in_fire


def update(map, dim_map):
    map_voisin_in_fire = create_map_voisin_in_fire(map, dim_map)
    for i in range(dim_map[0]):
        for j in range(dim_map[1]):
            if np.array_equal(map[i, j], TREE_COLOR):
                if map_voisin_in_fire[i, j] > 0:
                    map[i, j] = FIRE_COLOR
            elif np.array_equal(map[i, j], FIRE_COLOR):
                map[i, j] = CENDER_COLOR
    return map


if __name__ == "__main__":

    T = 100
    DIM_MAP = (10, 10, 3)
    NB_TREE_INIT = 70
    MAP = np.zeros(DIM_MAP, np.uint8)

    pygame.init()
    fenetre = pygame.display.set_mode(SIZE)

    MAP = initialisation_forest(MAP, DIM_MAP, NB_TREE_INIT)

    MAP_IMAGE = pygame.surfarray.make_surface(MAP)
    MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, SIZE)
    fenetre.blit(MAP_IMAGE, (0, 0))
    pygame.display.update()

    wait()

    MAP = initialisation_fire(MAP, DIM_MAP)

    MAP_IMAGE = pygame.surfarray.make_surface(MAP)
    MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, SIZE)
    fenetre.blit(MAP_IMAGE, (0, 0))
    pygame.display.update()

    wait()

    t = 0
    running = True

    while t < T and running is True:

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False
                pygame.quit()

        MAP = update(MAP, DIM_MAP)

        MAP_IMAGE = pygame.surfarray.make_surface(MAP)
        MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, SIZE)
        fenetre.blit(MAP_IMAGE, (0, 0))
        pygame.time.delay(100)
        pygame.display.update()

        t += 1

        print('t = ', t)


