import numpy as np
import random
import pygame
import sys
from pygame.locals import *

SIZE = (600, 600)


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return


def initialisation(map, dim_map, nb_cell_init):
    for c in range(nb_cell_init):
        pos_c = (random.randint(0, dim_map[0]-1), random.randint(0, dim_map[1]-1))
        map[pos_c[0], pos_c[1]] = 255
    return map


def nb_voisin(map, pos_cell, dim_map):
    voisins = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if [i, j] != [0, 0]:
                if 0 <= pos_cell[0]+i < dim_map[0] and 0 <= pos_cell[1]+j < dim_map[1]:
                    if map[pos_cell[0]+i, pos_cell[1]+j] == 255:
                        voisins += 1
    return voisins


def create_map_voisin(map, dim_map):
    map_voisin = np.zeros_like(map)
    for i in range(dim_map[0]):
        for j in range(dim_map[1]):
            pos_cell = (i, j)
            map_voisin[i, j] = nb_voisin(map, pos_cell, dim_map)
    return map_voisin


def update(map, dim_map):
    map_voisin = create_map_voisin(map, dim_map)
    for i in range(dim_map[0]):
        for j in range(dim_map[1]):
            if map_voisin[i, j] == 3:
                map[i, j] = 255
            elif map_voisin[i, j] < 2 or map_voisin[i, j] > 3:
                map[i, j] = 0
    return map


if __name__ == "__main__":

    T = 1000
    DIM_MAP = (20, 20)
    NB_CELL_INIT = 150
    MAP = np.zeros(DIM_MAP, np.uint8)

    pygame.init()
    fenetre = pygame.display.set_mode(SIZE)

    MAP = initialisation(MAP, DIM_MAP, NB_CELL_INIT)
    MAP_IMAGE = pygame.surfarray.make_surface(MAP)
    MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, SIZE)
    fenetre.blit(MAP_IMAGE, (0, 0))
    pygame.display.update()

    wait()

    running = True
    t = 0

    while t < T and running == True:

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False
                pygame.quit()

        MAP_IMAGE = pygame.surfarray.make_surface(MAP)
        MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, SIZE)
        fenetre.blit(MAP_IMAGE, (0, 0))
        pygame.time.delay(100)
        pygame.display.update()

        MAP = update(MAP, DIM_MAP)

        t += 1

        print('t = ', t)

