import pygame

class Wall_twoDBoxes2(pygame.sprite.Sprite):

    def __init__(self, name, display, x_pos, y_pos, x_width, y_height):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_width = x_width
        self.y_height = y_height
        self.image = pygame.Surface((x_width, y_height)).convert_alpha()
        black = (0, 0, 0)
        self.image.fill(black)
        self.rect = pygame.draw.rect(display, black, [x_pos, y_pos, x_width, y_height])
        self.mask = pygame.mask.from_surface(self.image)
