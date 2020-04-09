import pygame
from oneDBoxes2Scenario.Box_oneDBoxes2 import *
from oneDBoxes2Scenario.Shappy_oneDBoxes2 import *
from copy import *
import pickle


class World_oneDBoxes2(object):

    def __init__(self, terrain, policy_file):

        self.last_update = None

        self.screen_ratio = 30

        self.terrain = terrain

        temp_type = policy_file.replace("oneDBoxes2_MDP_", "")
        temp_type = temp_type.replace("_policy_map1.pickle", "")
        temp_type = temp_type.replace("_policy_map2.pickle", "")
        temp_type = temp_type.replace("_policy_map3.pickle", "")
        self.type_of_policy = temp_type

        self.policy = []
        self.policy2 = []
        self.get_policy(policy_file)

        self.screen_width = len(self.terrain.matrix[0]) * self.screen_ratio
        self.screen_height = len(self.terrain.matrix) * self.screen_ratio

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        self.font = pygame.font.SysFont("Times New Roman", 20)

        self.score = 0

        self.shappy_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()

        self.show_automatic = False
        self.time_interval = time.time()

        self.current_map = []
        for line in self.terrain.matrix:
            for i in range(len(line)):
                if line[i] == 3:
                    for letter in line:
                        self.current_map.append(int(letter))
                    break

        self.current_state = []
        for i in range(len(self.current_map)):
            if int(self.current_map[i]) == 3:
                self.current_state.append(i)
            #if self.type_of_policy == "centralized":
            if int(self.current_map[i]) == 4:
                self.current_state.append(i)
        for i in range(len(self.current_map)):
            if int(self.current_map[i]) == 2:
                self.current_state.append(i)

        # create walls
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 1:
                    wall = Wall("Wall", self.screen, column * self.screen_ratio, line * self.screen_ratio,
                                self.screen_ratio, self.screen_ratio)
                    self.wall_group.add(wall)

        # #create boxes
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 2:
                    box = Box_oneDBoxes2(column * self.screen_ratio, line * self.screen_ratio)
                    self.box_group.add(box)

        # #create shappys
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 3:
                    shappy = Shappy_oneDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self, 3,
                                                self.current_map, self.screen_width, self.screen_height,
                                                True, self.policy, self.type_of_policy, self.current_state)
                    self.shappy_group.add(shappy)
                if self.terrain.matrix[line][column] == 4:
                    if self.type_of_policy == "peer_aware_decentralized" or self.type_of_policy == "peer_communication_decentralized":
                        shappy = Shappy_oneDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self, 4,
                                                    self.current_map, self.screen_width, self.screen_height,
                                                    True, self.policy2, self.type_of_policy, self.current_state)
                    else:
                        shappy = Shappy_oneDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self, 4,
                                                   self.current_map, self.screen_width, self.screen_height,
                                                   True, self.policy, self.type_of_policy, self.current_state)
                    self.shappy_group.add(shappy)

        #self.simulation_run_states = [self.current_state]

        self.initial_number_of_boxes = len(self.box_group)

    def render(self):
        # add background over all past images
        self.screen.fill((255, 255, 255))

        self.shappy_group.draw(self.screen)
        self.box_group.draw(self.screen)
        self.wall_group.draw(self.screen)

        score_rend = self.font.render("Score: " + str(self.score), 1, (255, 255, 255))
        self.screen.blit(score_rend, (30, 5))

        if self.show_automatic:
            automatic_rend = self.font.render("Automatic", 1, (255, 255, 255))
            self.screen.blit(automatic_rend, (self.screen_width / 2 - 30, 5))

        pygame.display.flip()

    def box_group_remove(self, input_x_pos, input_y_pos):
        x_pos = input_x_pos * self.screen_ratio
        y_pos = input_y_pos * self.screen_ratio
        for box in self.box_group:
            if box.x_pos == x_pos and box.y_pos == y_pos:
                self.box_group.remove(box)

    def update(self):
        if time.time() - self.time_interval > 1:

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
        if self.type_of_policy == "peer_aware_decentralized" or self.type_of_policy == "peer_communication_decentralized":
            self.policy, self.policy2 = pickle.load(fp)
        else:
            self.policy = pickle.load(fp)
        fp.close()

    def set_new_terrain_matrix(self, shappy3_state, shappy4_state):

        if len(shappy3_state) == len(self.current_state) and len(shappy4_state) == len(self.current_state):
            equal = True
            for i in range(len(self.current_state)):
                if shappy3_state[i] != shappy4_state[i] or shappy3_state[i] != self.current_state[i]:
                    equal = False
            if equal:
                return

        min_range = 2
        if self.type_of_policy == "centralized" or self.type_of_policy == "peer_aware_decentralized" or self.type_of_policy == "peer_communication_decentralized":
            self.current_state = shappy3_state
            for i in range(2, len(shappy3_state)):
                if shappy4_state[1] == self.current_state[i]:
                    self.current_state.remove(self.current_state[i])
                    break
            self.current_state[1] = shappy4_state[1]

            for i in range(len(self.current_map)):
                if self.current_map[i] == 2 or self.current_map[i] == 3 or self.current_map[i] == 4:
                    self.current_map[i] = 0

            self.current_map[shappy3_state[0]] = 3
            self.current_map[shappy4_state[1]] = 4

        elif self.type_of_policy == "decentralized":
            self.current_state = [0]
            for item in shappy4_state:
                self.current_state.append(item)

            for i in range(2, len(self.current_state)):
                if shappy3_state[0] == self.current_state[i]:
                    self.current_state.remove(self.current_state[i])
                    break
            self.current_state[0] = shappy3_state[0]

            for i in range(len(self.current_map)):
                if self.current_map[i] == 2 or self.current_map[i] == 3 or self.current_map[i] == 4:
                    self.current_map[i] = 0

            self.current_map[shappy3_state[0]] = 3
            self.current_map[shappy4_state[0]] = 4

        #     min_range = 1
        #     self.current_state = shappy3_state
        #     for i in range(1, len(self.current_state)):
        #         if shappy4_state[0] == self.current_state[i]:
        #             self.current_state.remove(self.current_state[i])
        #             break

        for i in range(min_range, len(self.current_state)):
            self.current_map[self.current_state[i]] = 2

