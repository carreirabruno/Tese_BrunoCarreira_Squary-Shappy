import pygame
from twoDBoxes2Scenario.Box_twoDBoxes2 import *
from twoDBoxes2Scenario.Shappy_twoDBoxes2 import *
from twoDBoxes2Scenario.Wall_twoDBoxes2 import *
from copy import *
import pickle
import time


class World_twoDBoxes2(object):

    def __init__(self, terrain, policy_file):

        self.last_update = None

        self.screen_ratio = 30

        self.terrain = terrain

        self.speed = 0.1

        temp_type = policy_file.replace("twoDBoxes2_MDP_", "")
        temp_type = temp_type.replace("_policy_map1.pickle", "")
        temp_type = temp_type.replace("_policy_map2.pickle", "")
        temp_type = temp_type.replace("_policy_map3.pickle", "")
        self.type_of_policy = temp_type

        if self.type_of_policy == "individual_decentralized_split_rewards" or self.type_of_policy == "individual_decentralized_joint_rewards":
            self.type_of_policy = "individual_decentralized"
        # elif self.type_of_policy == "peer_aware_decentralized_split_rewards" or self.type_of_policy == "peer_aware_decentralized_joint_rewards":
        #     self.type_of_policy = "peer_aware_decentralized"
        # elif self.type_of_policy == "peer_communication_decentralized_split_rewards" or self.type_of_policy == "peer_communication_decentralized_joint_rewards":
        #     self.type_of_policy = "peer_communication_decentralized"
        # elif self.type_of_policy == "peer_listen_decentralized_split_rewards" or self.type_of_policy == "peer_listen_decentralized_joint_rewards":
        #     self.type_of_policy = "peer_listen_decentralized"

        self.policy = []
        self.policy2 = []
        self.get_policy(policy_file)

        # for line in self.policy:
        #     print("3 - ", line)
        # print()
        #
        # for line in self.policy2:
        #     print("4 - ", line)
        #
        # quit()

        self.screen_width = len(self.terrain.matrix[0]) * self.screen_ratio
        self.screen_height = len(self.terrain.matrix) * self.screen_ratio

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        self.font = pygame.font.SysFont("Times New Roman", 20)

        self.score = 0

        self.shappy_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()

        self.show_automatic = False

        self.blue_communicated = False
        self.blue_message = "teste"
        self.blue_timer = time.time()
        self.red_communicated = False
        self.red_message = "teste"
        self.red_timer = time.time()

        self.time_interval = time.time()

        self.current_map = []
        for line in terrain.matrix:
            temp_array = []
            for letter in line:
                temp_array.append(int(letter))
            self.current_map.append(temp_array)

        self.current_state = []
        for i in range(len(self.current_map)):
            for j in range(len(self.current_map[i])):
                if int(self.current_map[i][j]) == 7:
                    self.current_state.append([i, j])
                    self.current_state.append([i, j])
                    break
                if int(self.current_map[i][j]) == 3:
                    self.current_state.append([i, j])
                    break
        for i in range(len(self.current_map)):
            for j in range(len(self.current_map[i])):
                if int(self.current_map[i][j]) == 4:
                    self.current_state.append([i, j])
                    break
        for i in range(len(self.current_map)):
            for j in range(len(self.current_map[i])):
                if int(self.current_map[i][j]) == 2:
                    self.current_state.append([i, j])

        # create walls
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 1:
                    wall = Wall_twoDBoxes2("Wall", self.screen, column * self.screen_ratio, line * self.screen_ratio,
                                           self.screen_ratio, self.screen_ratio)
                    self.wall_group.add(wall)

        # #create boxes
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 2:
                    box = Box_twoDBoxes2(column * self.screen_ratio, line * self.screen_ratio)
                    self.box_group.add(box)

        # #create shappys
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 3:
                    shappy = Shappy_twoDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self, 3,
                                               self.current_map, self.screen_width, self.screen_height,
                                               True, self.policy, self.type_of_policy, self.current_state)
                    self.shappy_group.add(shappy)
                if self.terrain.matrix[line][column] == 4:
                    if self.type_of_policy != "centralized":
                        shappy = Shappy_twoDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self, 4,
                                                   self.current_map, self.screen_width, self.screen_height,
                                                   True, self.policy2, self.type_of_policy, self.current_state)
                    else:
                        shappy = Shappy_twoDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self, 4,
                                                   self.current_map, self.screen_width, self.screen_height,
                                                   True, self.policy, self.type_of_policy, self.current_state)
                    self.shappy_group.add(shappy)

        self.initial_number_of_boxes = len(self.box_group)

    def render(self):
        # add background over all past images
        self.screen.fill((255, 255, 255))

        # pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen_width, self.screen_ratio-5))
        # pygame.draw.rect(self.screen, (0, 0, 0), (0, self.screen_height-self.screen_ratio, self.screen_width,
        #                                           self.screen_ratio))
        # pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen_ratio-5, self.screen_height))
        # pygame.draw.rect(self.screen, (0, 0, 0), (self.screen_width-self.screen_ratio, 0, self.screen_ratio,
        #                                           self.screen_height))

        self.shappy_group.draw(self.screen)
        self.box_group.draw(self.screen)
        self.wall_group.draw(self.screen)

        # score_rend = self.font.render("Score: " + str(self.score), 1, (255, 255, 255))
        # self.screen.blit(score_rend, (30, 0))

        if self.show_automatic:
            automatic_rend = self.font.render("Automatic", 1, (255, 255, 255))
            self.screen.blit(automatic_rend, (self.screen_width / 2 - 30, 5))

        if self.blue_communicated:
            automatic_rend = self.font.render(self.blue_message, 1, (0, 0, 255))
            self.screen.blit(automatic_rend, (50, self.screen_height / 3))
        if self.red_communicated:
            automatic_rend = self.font.render(self.red_message, 1, (255, 0, 0))
            self.screen.blit(automatic_rend, (self.screen_width / 2 + 30, self.screen_height / 3))

        pygame.display.flip()

    def box_group_remove(self, input_x_pos, input_y_pos):
        x_pos = input_x_pos * self.screen_ratio
        y_pos = input_y_pos * self.screen_ratio
        for box in self.box_group:
            if box.x_pos == x_pos and box.y_pos == y_pos:
                self.box_group.remove(box)

    def update(self):
        if time.time() - self.time_interval > self.speed:
            self.blue_communicated = False
            self.red_communicated = False
            self.time_interval = time.time()
            shappy3_state = []
            shappy4_state = []
            for shappy in self.shappy_group:
                if shappy.color == 3:
                    shappy3_state = shappy.update(self.current_state)
                if shappy.color == 4:
                    shappy4_state = shappy.update(self.current_state)

            self.set_new_terrain_matrix(shappy3_state, shappy4_state)

            self.score = abs(self.initial_number_of_boxes - len(self.box_group))

            self.last_update = time.time()

            return self.current_state

        return None

    def get_policy(self, policy_file):
        fp = open(policy_file, "rb")  # Unpickling
        if self.type_of_policy == "centralized":
            self.policy = pickle.load(fp)
        else:
            self.policy, self.policy2 = pickle.load(fp)

        fp.close()

    def set_new_terrain_matrix(self, shappy3_state, shappy4_state):

        if len(shappy3_state) == len(self.current_state) and len(shappy4_state) == len(self.current_state):
            equal = True
            for i in range(len(self.current_state)):
                if shappy3_state[i] != shappy4_state[i] or shappy3_state[i] != self.current_state[i]:
                    equal = False
            if equal:
                return

        auto_movement = False
        for shappy in self.shappy_group:
            if shappy.auto:
                auto_movement = True
            else:
                auto_movement = False

        min_range = 2
        # if self.type_of_policy == "centralized" or self.type_of_policy == "peer_aware_decentralized" or \
        #         self.type_of_policy == "peer_communication_decentralized" or not auto_movement:
        #     self.current_state = shappy3_state
        #     for i in range(2, len(shappy3_state)):
        #         if self.compare_arrays(shappy4_state[1], self.current_state[i]):
        #             self.current_state.remove(self.current_state[i])
        #             break
        #     self.current_state[1] = shappy4_state[1]

        if self.type_of_policy == "individual_decentralized" and auto_movement:
            self.current_state = [0]
            for item in shappy4_state:
                self.current_state.append(item)

            for i in range(min_range, len(self.current_state)):
                if self.compare_arrays(shappy3_state[0], self.current_state[i]):
                    self.current_state.remove(self.current_state[i])
                    break
            self.current_state[0] = shappy3_state[0]

        else:
            self.current_state = shappy3_state
            for i in range(2, len(shappy3_state)):
                if self.compare_arrays(shappy4_state[1], self.current_state[i]):
                    self.current_state.remove(self.current_state[i])
                    break
            self.current_state[1] = shappy4_state[1]

        for i in range(len(self.current_map)):
            for j in range(len(self.current_map[i])):
                if self.current_map[i][j] == 3 or self.current_map[i][j] == 4:
                    self.current_map[i][j] = 0

        if self.type_of_policy == "individual_decentralized":
            if self.compare_arrays(shappy3_state[0], shappy4_state[0]):
                self.current_map[shappy3_state[0][0]][shappy3_state[0][1]] = 7
            else:
                self.current_map[shappy3_state[0][0]][shappy3_state[0][1]] = 3
                self.current_map[shappy4_state[0][0]][shappy4_state[0][1]] = 4
        else:
            if self.compare_arrays(shappy3_state[0], shappy4_state[1]):
                self.current_map[shappy3_state[0][0]][shappy3_state[0][1]] = 7
            else:
                self.current_map[shappy3_state[0][0]][shappy3_state[0][1]] = 3
                self.current_map[shappy4_state[1][0]][shappy4_state[1][1]] = 4

        for i in range(min_range, len(self.current_state)):
            self.current_map[self.current_state[i][0]][self.current_state[i][1]] = 2

    def message_blue(self, message):
        self.blue_communicated = True
        self.blue_message = message

    def message_red(self, message):
        self.red_communicated = True
        self.red_message = message

    def compare_arrays(self, array1, array2):
        if len(array1) != len(array2):
            return False
        else:
            for i in range(len(array1)):
                if array1[i] != array2[i]:
                    return False
        return True