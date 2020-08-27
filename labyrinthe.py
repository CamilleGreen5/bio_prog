import numpy as np
import random
import cv2 as cv
import sys
import pygame
from pygame.locals import *


SIZE = (600, 600)
WALL_COLOR = [0, 0, 0]
PERSO_COLOR = [0, 255, 0]
PATH_COLOR = [0, 100, 0]
DIRT_COLOR = [50, 50, 50]
MOV = [[0, 1], [1, 0], [0, -1], [-1, 0]]     # droite bas gauche haut

T = 10000
DIM_MAP = (20, 20, 3)
NB_WALL_INIT = 400


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return


def initialisation_path(map, dim_map):
    pos = [0, 0]
    map[pos[0], pos[1]] = DIRT_COLOR
    path = []
    while not (pos[0] == dim_map[0]-1 and pos[1] == dim_map[1]-1):
        dir = random.choices([0, 1, 2, 3], [3, 3, 1, 1], k=1)[0]
        while not (0 <= pos[0] + MOV[dir][0] < dim_map[0] and 0 <= pos[1] + MOV[dir][1] < dim_map[1]):
            dir = random.choices([0, 1, 2, 3], [3, 3, 1, 1], k=1)[0]

        pos = np.add(pos, MOV[dir])
        map[pos[0], pos[1]] = DIRT_COLOR
        path.append(pos)

    return map, path


def initialisation_lab(map, dim_map, nb_wall_init):
    for wall in range(nb_wall_init):
        x = random.randint(0, dim_map[0]-1)
        y = random.randint(0, dim_map[1]-1)
        pos_wall = (x, y)
        map[pos_wall[0], pos_wall[1]] = WALL_COLOR
    map, path = initialisation_path(map, dim_map)
    return map, path


def find_possible_mov_id(map, dim, pos):
    possible_mov_id = []
    for i in range(len(MOV)):
        if np.array_equal(map[pos[0], pos[1]], DIRT_COLOR):
            if 0 <= pos[0]+MOV[i][0] < dim[0] and 0 <= pos[1]+MOV[i][1] < dim[1]:
                if np.array_equal(map[pos[0]+MOV[i][0], pos[1]+MOV[i][1]], DIRT_COLOR):
                    possible_mov_id.append(i)
    return possible_mov_id


def update(map, dim, pos, q_table):
    mov_id = random.choices([i for i in range(4)], q_table[pos[0], pos[1]])
    map[pos[0], pos[1]] = PATH_COLOR
    pos = np.add(pos, MOV[mov_id[0]])
    map[pos[0], pos[1]] = PERSO_COLOR
    # q_table = update_q_table(q_table, pos)
    return map, pos


def initialisation_Q(map, dim):
    q_table = np.zeros((dim[0], dim[1], 4), np.uint8)
    for i in range(dim[0]):
        for j in range(dim[1]):
            pos = [i, j]
            possible_mov_id = find_possible_mov_id(map, dim, pos)
            for id in possible_mov_id:
                q_table[i, j, id] = 1
    for id in range(4):
        q_table[dim[0]-1, dim[1]-1, id] = 255
    return q_table


def update_q_table(q_table):

    return q_table


if __name__ == "__main__":

    MAP = np.ones(DIM_MAP, np.uint8)
    MAP = MAP*50

    pygame.init()
    fenetre = pygame.display.set_mode(SIZE)

    MAP, PATH = initialisation_lab(MAP, DIM_MAP, NB_WALL_INIT)

    MAP_IMAGE = pygame.surfarray.make_surface(np.transpose(MAP, (1, 0, 2)))
    MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, SIZE)
    fenetre.blit(MAP_IMAGE, (0, 0))
    pygame.display.update()

    wait()

    Q_TABLE = initialisation_Q(MAP, DIM_MAP)

    POS_PERSO = [0, 0]
    MAP[0, 0] = PERSO_COLOR

    MAP_IMAGE = pygame.surfarray.make_surface(np.transpose(MAP, (1, 0, 2)))
    MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, SIZE)
    fenetre.blit(MAP_IMAGE, (0, 0))
    pygame.display.update()

    wait()

    t = 0
    running = True
    victory = False

    while t < T and running == True:

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False
                pygame.quit()

        MAP, POS_PERSO = update(MAP, DIM_MAP, POS_PERSO, Q_TABLE)

        MAP_IMAGE = pygame.surfarray.make_surface(np.transpose(MAP, (1, 0, 2)))
        MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, SIZE)
        fenetre.blit(MAP_IMAGE, (0, 0))
        pygame.time.delay(100)
        pygame.display.update()

        if POS_PERSO[0] == DIM_MAP[0]-1 and POS_PERSO[1] == DIM_MAP[1]-1:
            running = False
            victory = True

        t += 1
        print('t = ', t)

    if victory:
        print("VICTORY")
    else:
        print('LOSE')

    wait()
    pygame.quit()
