import pygame
from World import *


class Box_twoDBoxes2(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../Images/30_30_Green_Square.png")
        self.x_size, self.y_size = self.image.get_rect().size
        self.rect = pygame.Rect(x_pos, y_pos, self.x_size, self.y_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_pos = x_pos
        self.y_pos = y_pos
