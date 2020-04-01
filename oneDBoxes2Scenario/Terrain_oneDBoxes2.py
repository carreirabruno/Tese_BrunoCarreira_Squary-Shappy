import pygame
from game import *
import numpy as np
import time
import random
import string


class Terrain_oneDBoxes2(object):
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
