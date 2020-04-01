from World import *
import math
from itertools import *
import sys
import numpy
import copy

numpy.set_printoptions(threshold=sys.maxsize)


def get_center(sprite):
    return sprite.rect.x + sprite.rect.width / 2, sprite.rect.y + sprite.rect.height / 2


class Shappy_oneDBoxes2(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, world, color, terrain_matrix, screen_width, screen_height,
                 auto, policy, type_of_policy):

        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.old_x_pos = x_pos
        self.old_y_pos = y_pos
        self.world = world
        self.terrain_matrix = terrain_matrix
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.auto = auto
        self.policy = policy
        self.type_of_policy = type_of_policy

        self.color = color

        self.dir_vector = []

        self.calculate = False
        self.next_boxes = []
        self.current_box = math.inf
        self.next_box_x = math.inf

        if self.color == 3:
            self.image = pygame.image.load("../Images/20_20_Blue_Square.png")
        elif self.color == 4:
            self.image = pygame.image.load("../Images/20_20_Red_Square.png")
        else:
            print("Unknown colour number: ", self.color)

        x_size, y_size = self.image.get_rect().size
        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.dir = (x_pos, y_pos)

        self.time_interval = time.time()

        self.current_state = []

        self.my_number = color
        if self.my_number == 3:
            self.other_number = 4
        else:
            self.other_number = 3

    def update(self, current_state):
        self.current_state = copy.deepcopy(current_state)
        if not self.auto:
            self.calculate = False
            keys = pygame.key.get_pressed()
            if self.color == 3:
                if keys[pygame.K_a]:
                    self.lefty()
                if keys[pygame.K_d]:
                    self.righty()
            elif self.color == 4:
                if keys[pygame.K_LEFT]:
                    self.lefty()
                if keys[pygame.K_RIGHT]:
                    self.righty()
        elif self.auto:
            self.auto_movement(self.type_of_policy)

        self.time_interval = time.time()

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

        self.dir = (self.x_pos - self.old_x_pos, self.y_pos - self.old_y_pos)

        self.old_x_pos = self.x_pos
        self.old_y_pos = self.y_pos

        return self.current_state

    def lefty(self):
        if self.current_state[(int(self.x_pos / self.world.screen_ratio) - 1)] != 1:
            self.current_state[int(self.x_pos / self.world.screen_ratio)] = 0
            self.x_pos -= 1 * self.world.screen_ratio

            if self.current_state[int(self.x_pos / self.world.screen_ratio)] == 2:
                self.world.box_group_remove(int(self.x_pos / self.world.screen_ratio),
                                            int(self.y_pos / self.world.screen_ratio))

            self.current_state[int(self.x_pos / self.world.screen_ratio)] = self.color


    def righty(self):
        if self.current_state[(int(self.x_pos / self.world.screen_ratio) + 1)] != 1:
            self.current_state[int(self.x_pos / self.world.screen_ratio)] = 0
            self.x_pos += 1 * self.world.screen_ratio

            if self.current_state[int(self.x_pos / self.world.screen_ratio)] == 2:
                self.world.box_group_remove(int(self.x_pos / self.world.screen_ratio),
                                            int(self.y_pos / self.world.screen_ratio))

            self.current_state[int(self.x_pos / self.world.screen_ratio)] = self.color

    def auto_movement(self, type):
        if type == "Centralized":
            actions = -1
            for state in self.policy:
                equal = True
                for i in range(len(state[0])):
                    if self.current_state[i] != state[0][i]:
                        equal = False
                if equal:
                    actions = np.argmax(state[1])
                    break

            if self.color == 3:
                if actions == 0 or actions == 1:
                    pass
                elif actions == 2 or actions == 3 or actions == 4:
                    self.lefty()
                elif actions == 5 or actions == 6 or actions == 7:
                    self.righty()
            elif self.color == 4:
                if actions == 2 or actions == 5:
                    pass
                elif actions == 0 or actions == 3 or actions == 6:
                    self.lefty()
                elif actions == 1 or actions == 4 or actions == 7:
                    self.righty()
        elif type == "Decentralized":

            for i in range(len(self.current_state)):
                if self.current_state[i] == 4:
                    self.current_state[i] = 0
                elif self.current_state[i] == 7:
                    self.current_state[i] = 3

            actions = -1
            for state in self.policy:
                equal = True
                for i in range(len(state[0])):
                    if self.current_state[i] != state[0][i]:
                        equal = False
                if equal:
                    actions = np.argmax(state[1])
                    break
            if actions == 0:
                pass
            elif actions == 1:
                self.lefty()
            elif actions == 2:
                self.righty()

        # # Actions
        # STAY_LEFT = 0
        # STAY_RIGHT = 1
        # LEFT_STAY = 2
        # LEFT_LEFT = 3
        # LEFT_RIGHT = 4
        # RIGHT_STAY = 5
        # RIGHT_LEFT = 6
        # RIGHT_RIGHT = 7
