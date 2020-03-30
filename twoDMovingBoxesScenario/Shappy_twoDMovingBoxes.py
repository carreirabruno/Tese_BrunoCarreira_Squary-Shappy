from World import *
import math
from itertools import *
import sys
import numpy
import copy

numpy.set_printoptions(threshold=sys.maxsize)


def get_center(sprite):
    return sprite.rect.x + sprite.rect.width / 2, sprite.rect.y + sprite.rect.height / 2


class Shappy_twoDMovingBoxes(pygame.sprite.Sprite):

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
        self.type = None
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

        self.current_state = []

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
                if keys[pygame.K_w]:
                    self.upy()
                if keys[pygame.K_s]:
                    self.downy()
            elif self.color == 4:
                if keys[pygame.K_LEFT]:
                    self.lefty()
                if keys[pygame.K_RIGHT]:
                    self.righty()
                if keys[pygame.K_UP]:
                    self.upy()
                if keys[pygame.K_DOWN]:
                    self.downy()
        elif self.auto:
            self.auto_movement()

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

        self.old_x_pos = self.x_pos
        self.old_y_pos = self.y_pos

        #if self.color == 3:
            #self.print_array(self.current_state)
        return self.current_state

    def lefty(self):
        if self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                             self.world.screen_ratio) - 1] != 1:
            self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                              self.world.screen_ratio)] = 0
            self.x_pos -= 1 * self.world.screen_ratio

            if self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                                 self.world.screen_ratio)] == 2:
                self.world.box_group_remove(self.x_pos, self.y_pos)

            self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                              self.world.screen_ratio)] = self.color

    def righty(self):
        if self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                             self.world.screen_ratio) + 1] != 1:
            self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                              self.world.screen_ratio)] = 0
            self.x_pos += 1 * self.world.screen_ratio

            if self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                                 self.world.screen_ratio)] == 2:
                self.world.box_group_remove(self.x_pos, self.y_pos)

            self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                              self.world.screen_ratio)] = self.color

    def upy(self):

        if self.current_state[int(self.y_pos / self.world.screen_ratio) - 1][int(self.x_pos /
                                                                             self.world.screen_ratio)] != 1:
            self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                              self.world.screen_ratio)] = 0
            self.y_pos -= 1 * self.world.screen_ratio

            if self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                                 self.world.screen_ratio)] == 2:
                self.world.box_group_remove(self.x_pos, self.y_pos)

            self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                              self.world.screen_ratio)] = self.color

    def downy(self):
        if self.current_state[int(self.y_pos / self.world.screen_ratio) + 1][int(self.x_pos /
                                                                             self.world.screen_ratio)] != 1:
            self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                              self.world.screen_ratio)] = 0

            self.y_pos += 1 * self.world.screen_ratio

            if self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                                 self.world.screen_ratio)] == 2:
                self.world.box_group_remove(self.x_pos, self.y_pos)

            self.current_state[int(self.y_pos / self.world.screen_ratio)][int(self.x_pos /
                                                                              self.world.screen_ratio)] = self.color

    def auto_movement(self):
        if self.type_of_policy == "centralized":
            actions = 0

            for state in self.policy:
                equal = True
                for i in range(len(state[0])):
                    for j in range(len(self.current_state[i])):
                        if self.current_state[i][j] != state[0][i][j]:
                            equal = False
                if equal:
                    self.print_array(self.current_state)
                    actions = np.argmax(state[1])
                    break
            print(actions)

            action3, action4 = self.get_centralized_stringed_actions(actions)
            
            if self.color == 3:
                if action3 == "STAY":
                    pass
                elif action3 == "LEFT":
                    self.lefty()
                elif action3 == "RIGHT":
                    self.righty()
                elif action3 == "UP":
                    self.upy()
                elif action3 == "DOWN":
                    self.downy()
            elif self.color == 4:
                if action4 == "STAY":
                    pass
                elif action4 == "LEFT":
                    self.lefty()
                elif action4 == "RIGHT":
                    self.righty()
                elif action4 == "UP":
                    self.upy()
                elif action4 == "DOWN":
                    self.downy()

        elif self.type_of_policy == "decentralized":
            for i in range(len(self.current_state)):
                for j in range(len(self.current_state[i])):
                    if self.current_state[i][j] == 7:
                        self.current_state[i][j] = 3
                    elif self.color == 3:
                        if self.current_state[i][j] == 4:
                            self.current_state[i][j] = 0
                    elif self.color == 4:
                        if self.current_state[i][j] == 4:
                            self.current_state[i][j] = 3
                        elif self.current_state[i][j] == 3:
                            self.current_state[i][j] = 0

            actions = 0
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
            elif actions == 3:
                self.upy()
            elif actions == 4:
                self.downy()

    def get_centralized_stringed_actions(self, action):
        stringed_actions = ""
        if action == 0:
            stringed_actions = "STAY_STAY"
        elif action == 1:
            stringed_actions = "STAY_LEFT"
        elif action == 2:
            stringed_actions = "STAY_RIGHT"
        elif action == 3:
            stringed_actions = "STAY_UP"
        elif action == 4:
            stringed_actions = "STAY_DOWN"

        elif action == 5:
            stringed_actions = "LEFT_STAY"
        elif action == 6:
            stringed_actions = "LEFT_LEFT"
        elif action == 7:
            stringed_actions = "LEFT_RIGHT"
        elif action == 8:
            stringed_actions = "LEFT_UP"
        elif action == 9:
            stringed_actions = "LEFT_DOWN"

        elif action == 10:
            stringed_actions = "RIGHT_STAY"
        elif action == 11:
            stringed_actions = "RIGHT_LEFT"
        elif action == 12:
            stringed_actions = "RIGHT_RIGHT"
        elif action == 13:
            stringed_actions = "RIGHT_UP"
        elif action == 14:
            stringed_actions = "RIGHT_DOWN"

        elif action == 15:
            stringed_actions = "UP_STAY"
        elif action == 16:
            stringed_actions = "UP_LEFT"
        elif action == 17:
            stringed_actions = "UP_RIGHT"
        elif action == 18:
            stringed_actions = "UP_UP"
        elif action == 19:
            stringed_actions = "UP_DOWN"

        elif action == 20:
            stringed_actions = "DOWN_STAY"
        elif action == 21:
            stringed_actions = "DOWN_LEFT"
        elif action == 22:
            stringed_actions = "DOWN_RIGHT"
        elif action == 23:
            stringed_actions = "DOWN_UP"
        elif action == 24:
            stringed_actions = "DOWN_DOWN"

        stringed_actions = stringed_actions.split("_")

        return stringed_actions[0], stringed_actions[1]

    def print_array(self, array):
        for line in array:
            print(line)