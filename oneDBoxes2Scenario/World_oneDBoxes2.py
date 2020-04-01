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

        self.policy = self.get_policy(policy_file)
        temp_type = policy_file.replace("oneDBoxes2_MDP_", "")
        temp_type = temp_type.replace("_policy_map1.pickle", "")
        temp_type = temp_type.replace("_policy_map2.pickle", "")
        self.type_of_policy = temp_type

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
                                                self.terrain.matrix, self.screen_width, self.screen_height,
                                                False, self.policy, self.type_of_policy)
                    self.shappy_group.add(shappy)
                if self.terrain.matrix[line][column] == 4:
                    shappy = Shappy_oneDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self, 4,
                                                self.terrain.matrix, self.screen_width, self.screen_height,
                                                False, self.policy, self.type_of_policy)
                    self.shappy_group.add(shappy)

        self.current_state = []
        for line in self.terrain.matrix:
            for i in range(len(line)):
                if line[i] == 2:
                    for letter in line:
                        self.current_state.append(int(letter))
                    break

        self.simulation_run_states = [self.current_state]

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

            self.simulation_run_states.append(self.current_state)

            self.score = abs(self.initial_number_of_boxes - len(self.box_group))

            self.last_update = time.time()

    def get_policy(self, policy_file):
        fp = open(policy_file, "rb")  # Unpickling
        policy = pickle.load(fp)
        fp.close()
        return policy

    def set_new_terrain_matrix(self, shappy3_state, shappy4_state):
        self.current_state = shappy3_state

        for i in range(len(self.current_state)):
            if self.current_state[i] == shappy4_state[i]:
                pass
            elif self.current_state[i] == 3 and shappy4_state[i] == 4:
                self.current_state[i] = 7
            elif self.current_state[i] != 3 and shappy4_state[i] == 4:
                self.current_state[i] = 4
            elif self.current_state[i] == 4 and shappy4_state[i] != 4:
                self.current_state[i] = shappy4_state[i]
