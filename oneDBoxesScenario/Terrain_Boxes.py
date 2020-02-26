import pygame
from game import *
import numpy as np
import time
import random
import string


class Terrain_Boxes(object):
    shappy_letters = list(string.ascii_uppercase)
    shappy_colours = range(0, 26)

    def __init__(self, file_name):
        self.initial_shappy_list = []
        self.initial_boxes_list = []

        f = open(file_name, "r")
        lines = f.readlines()

        self.height = len(lines[0]) - 1
        self.width = len(lines)

        self.matrix = np.zeros((self.width, self.height))
        # a = np.array([[1,2,3], [4,5,6]])

        y = 0
        for line in lines:
            x = 0
            for letter in line:
                if letter == '\n':
                    pass
                if letter == '1':
                    self.matrix[y][x] = 1
                if letter in self.shappy_letters:
                    self.initial_shappy_list.append(
                        [letter, y, x, self.shappy_colours[self.shappy_letters.index(letter)]])
                if letter == '2':
                    self.matrix[y][x] = 2
                # if letter == 'x':
                # 	self.initial_boxes_list.append([j, i])
                x += 1
            y += 1
        f.close()
    # self.inverted_matrix = self.matrix

    # def invert_matrix(self):
    #     for i in range(self.width):
    #         for j in range(self.height):
    #             self.matrix[i][j] = self.inverted_matrix[self.width - 1 - i][self.height - 1 - j]
