from World import *
import math
from itertools import *
import sys
import numpy
import copy

numpy.set_printoptions(threshold=sys.maxsize)

class Shappy_twoDBoxes2(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, world, color, terrain_matrix, screen_width, screen_height,
                 auto, policy, type_of_policy, fov_radius):

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
        self.fov_radius = int(fov_radius - 0.5)

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

        self.in_my_radius = False
        self.nearby_boxes_pos = []

        self.boxes_positions = []

    def update(self, current_state):
        if self.color == 3:
            self.check_nearby_boxes(current_state)
        self.set_current_state(current_state)

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
                if keys[pygame.K_1]:
                    self.world.send_message(self.color, "Blue pos is [" + str(int(self.x_pos/self.world.screen_ratio)) + "," + str(int(self.y_pos/self.world.screen_ratio)) + "]")

            elif self.color == 4:
                if keys[pygame.K_LEFT]:
                    self.lefty()
                if keys[pygame.K_RIGHT]:
                    self.righty()
                if keys[pygame.K_UP]:
                    self.upy()
                if keys[pygame.K_DOWN]:
                    self.downy()
                if keys[pygame.K_KP1]:
                    self.world.send_message(self.color, "Red pos is [" + str(self.x_pos) + "," + str(self.y_pos) + "]")

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
            actions = -1

            for state in self.policy:
                equal = True
                for i in range(len(state[0])):
                    if self.current_state[i] != state[0][i]:
                        equal = False
                if equal:
                    actions = np.argmax(state[1])
                    break

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

    def check_nearby_boxes(self, current_state):
        converted_x_pos = int(self.x_pos / self.world.screen_ratio)
        converted_y_pos = int(self.y_pos / self.world.screen_ratio)
        print(current_state[1][3], "adeus")
        for i in range(max(0, converted_x_pos - self.fov_radius), min(int(self.screen_height/self.world.screen_ratio), converted_x_pos + self.fov_radius + 1)):
            for j in range(max(0, converted_y_pos - self.fov_radius), min(int(self.screen_width/self.world.screen_ratio), converted_y_pos + self.fov_radius + 1)):

                if current_state[i][j] == 2:
                    print(i, j, "ola")
                    # if len(self.nearby_boxes_pos) == 0:
                    #     self.nearby_boxes_pos.append([i, j])
                    # else:
                    #     for item in self.nearby_boxes_pos:
                    #         print(self.nearby_boxes_pos)
                    #         if item[0] != i and item[1] != j:
                    #             print("add ", i, j)
                    #             self.nearby_boxes_pos.append([i, j])

    def get_center(self):
        return self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2

    # def detect_message(self):
    #     print("ola")
    #     message = ""
    #     while self.writing:
    #         for event in pygame.event.get():
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_RETURN:
    #                     print("adeus")
    #                     self.writing = False
    #                 elif event.key == pygame.K_BACKSPACE:
    #                     message = message[:-1]
    #                 else:
    #                     message += event.unicode
    #                     print(message)
    #
    #     self.world.send_message(self.color, message)

    def set_current_state(self, current_state):
        self.current_state = copy.deepcopy(current_state)

        for i in range(len(self.current_state)):
            for j in range(len(self.current_state[i])):
                if self.current_state[i][j] == 2:
                    self.current_state[i][j] = 0
        for box_pos in self.nearby_boxes_pos:
            self.current_state[box_pos[0]][box_pos[1]] = 2

        if self.color == 3:
            self.print_array(self.current_state)
            print()