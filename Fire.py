import pygame
import perceptron
from World import *
import numpy as np
import time
import math



class Fire(pygame.sprite.Sprite):

    hp_provided = -10

    def __init__(self, x_pos, y_pos):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/20-20_wine_square.png")
        x_size, y_size = self.image.get_rect().size
        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
        self.mask = pygame.mask.from_surface(self.image)

    def collided(self):
        self.kill()

