import pygame
import perceptron
from game import *
import numpy as np
import time
from Squary import *
import Shappy as sha
from Terrain import *
from World import *
from Wall import *
import random


class Displayer(object):

    def __init__(self, world):
        self.world = world






    def render(self):
        self.world.render()
        return
