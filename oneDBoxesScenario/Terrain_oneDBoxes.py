import pygame
from game import *
import numpy as np
import time
import random
import string


class Terrain_oneDBoxes(object):
    shappy_letters = list(string.ascii_uppercase)
    shappy_colours = range(0, 26)

    # def __init__(self, file_name):
    #     self.initial_shappy_list = []
    #     self.initial_boxes_list = []
    #
    #     f = open(file_name, "r")
    #     lines = f.readlines()
    #
    #     self.height = len(lines[0]) - 1
    #     self.width = len(lines)
    #
    #     self.matrix = np.zeros((self.width, self.height))
    #
    #     y = 0
    #     for line in lines:
    #         x = 0
    #         for letter in line:
    #             if letter == '\n':
    #                 pass
    #             if letter == '1':
    #                 self.matrix[y][x] = 1
    #             # if letter in self.shappy_letters:
    #             #     newID = self.get_random_ID()
    #             #     self.initial_shappy_list.append(
    #             #         [newID, letter, y, x, self.shappy_colours[self.shappy_letters.index(letter)]])
    #             if letter == '2':
    #                 self.matrix[y][x] = 2
    #             if letter == '3':
    #                 self.matrix[y][x] = 3
    #             if letter == '4':
    #                 self.matrix[y][x] = 4
    #             # if letter == 'x':
    #             # 	self.initial_boxes_list.append([j, i])
    #             x += 1
    #         y += 1
    #     f.close()

    # self.inverted_matrix = self.matrix

    # def invert_matrix(self):
    #     for i in range(self.width):
    #         for j in range(self.height):
    #             self.matrix[i][j] = self.inverted_matrix[self.width - 1 - i][self.height - 1 - j]

    def __init__(self, file_name):
        self.initial_shappy_list = []
        self.initial_boxes_list = []

        f = open(file_name, "r")
        lines = f.readlines()

        self.height = len(lines[0]) - 1
        self.width = len(lines)

        self.matrix = np.zeros((self.width, self.height))

        y = 0
        for line in lines:
            x = 0
            for letter in line:
                if letter == '\n':
                    pass
                elif letter == '1':
                    self.matrix[y][x] = 1
                elif letter == '2':
                    self.matrix[y][x] = 2
                elif letter == '3':
                    self.matrix[y][x] = 3
                elif letter == '4':
                    self.matrix[y][x] = 4
                elif letter == '7':
                    self.matrix[y][x] = 7
                x += 1
            y += 1
        f.close()

    # def get_random_ID(self):
    #     differentID = False
    #     randomID = -1
    #     while not differentID:
    #         #randomID = random.randint(0, 100)
    #         randomID = ''.join(random.choice("0123456789" + string.ascii_uppercase) for x in range(5))
    #         if len(self.initial_shappy_list) > 0:
    #             for shappy in self.initial_shappy_list:
    #                 if shappy[0] == randomID:
    #                     differentID = False
    #                     break
    #                 else:
    #                     differentID = True
    #         else:
    #             differentID = True
    #
    #     return randomID
