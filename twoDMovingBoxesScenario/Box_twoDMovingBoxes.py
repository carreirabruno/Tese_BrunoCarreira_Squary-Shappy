import pygame
from twoDMovingBoxesScenario.World_twoDMovingBoxes import *


class Box_twoDMovingBoxes(pygame.sprite.Sprite):
    score_provided = 10
    size = 20

    def __init__(self, x_pos, y_pos, world):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../Images/20-20_green_square.png")
        self.x_size, self.y_size = self.image.get_rect().size
        self.rect = pygame.Rect(x_pos, y_pos, self.x_size, self.y_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.world = world

    def update(self):
        random.seed()
        box_action = random.randint(0,3)
        if box_action == 0:  # LEFT
            if self.world.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos / self.world.screen_ratio) - 1] == 0:
                self.world.current_state[int(self.y_pos / self.world.screen_ratio)][
                    int(self.x_pos / self.world.screen_ratio)] = 0
                self.x_pos -= self.world.screen_ratio
                self.rect = pygame.Rect(self.x_pos, self.y_pos, self.x_size, self.y_size)
                self.world.current_state[int(self.y_pos / self.world.screen_ratio)][
                    int(self.x_pos / self.world.screen_ratio)] = 2
        elif box_action == 1:  # RIGHT
            if self.world.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos / self.world.screen_ratio) + 1] == 0:
                self.world.current_state[int(self.y_pos / self.world.screen_ratio)][
                    int(self.x_pos / self.world.screen_ratio)] = 0
                self.x_pos += self.world.screen_ratio
                self.rect = pygame.Rect(self.x_pos, self.y_pos, self.x_size, self.y_size)
                self.world.current_state[int(self.y_pos / self.world.screen_ratio)][
                    int(self.x_pos / self.world.screen_ratio)] = 2
        elif box_action == 2:  # UP
            if self.world.current_state[int(self.y_pos / self.world.screen_ratio) - 1][int(self.x_pos / self.world.screen_ratio)] == 0:
                self.world.current_state[int(self.y_pos / self.world.screen_ratio)][
                    int(self.x_pos / self.world.screen_ratio)] = 0
                self.y_pos -= self.world.screen_ratio
                self.rect = pygame.Rect(self.x_pos, self.y_pos, self.x_size, self.y_size)
                self.world.current_state[int(self.y_pos / self.world.screen_ratio)][
                    int(self.x_pos / self.world.screen_ratio)] = 2
        elif box_action == 3:  # DOWN
            if self.world.current_state[int(self.y_pos / self.world.screen_ratio) + 1][int(self.x_pos / self.world.screen_ratio)] == 0:
                self.world.current_state[int(self.y_pos / self.world.screen_ratio)][
                    int(self.x_pos / self.world.screen_ratio)] = 0
                self.y_pos += self.world.screen_ratio
                self.rect = pygame.Rect(self.x_pos, self.y_pos, self.x_size, self.y_size)
                self.world.current_state[int(self.y_pos / self.world.screen_ratio)][
                    int(self.x_pos / self.world.screen_ratio)] = 2
