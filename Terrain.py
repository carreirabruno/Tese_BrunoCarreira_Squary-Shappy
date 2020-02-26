import pygame
from game import *
import numpy as np
import time
import random
import string



class Terrain(object):

	shappy_letters = list(string.ascii_uppercase)
	shappy_colours = range(0,26)
	initial_shappy_list = []
	initial_squary_list = []

	def __init__(self, file_name):

		f = open(file_name, "r")
		lines = f.readlines()

		self.height = len(lines) - 1
		self.width = len(lines[1]) - 1

		self.matrix = np.zeros((self.width, self.height))

		counter = 0
		for line in lines:
			mini_count = 0
			for letter in line:

				if letter == '1':
					self.matrix[counter - 1][mini_count] = 1
				if letter == '\n':
					pass
				if letter in self.shappy_letters:
					# give information about a new shappy
					self.initial_shappy_list.append([letter, counter - 1, mini_count, self.shappy_colours[self.shappy_letters.index(letter)]])
				if letter == 'x':
					self.initial_squary_list.append([counter - 1, mini_count])

				mini_count += 1
			counter += 1

		#print(self.matrix)





































