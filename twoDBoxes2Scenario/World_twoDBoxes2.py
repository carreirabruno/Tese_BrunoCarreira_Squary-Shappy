import pygame
from twoDBoxes2Scenario.Terrain_twoDBoxes2 import *
from twoDBoxes2Scenario.Box_twoDBoxes2 import *
from twoDBoxes2Scenario.Shappy_twoDBoxes2 import *
from copy import *
import pickle


class World_twoDBoxes2(object):

    def __init__(self, terrain, policy_file):

        type_of_policy = policy_file.replace("twoDBoxes2_MDP_", '')
        type_of_policy = type_of_policy.replace("_policy_map1.pickle", '')

        self.last_update = None

        self.screen_ratio = 30

        self.terrain = terrain
        terrain_matrix = copy(self.terrain.matrix)
        terrain_matrix = terrain_matrix[:-2]

        self.policy = self.get_policy(policy_file)
        #self.policy = policy_file

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

        self.message_from_4 = ""
        self.time_out_message_from_4 = 0
        self.message_from_3 = ""
        self.time_out_message_from_3 = 0

        self.fov_radius = 1.5

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
                    box = Box_twoDBoxes2(column * self.screen_ratio, line * self.screen_ratio)
                    self.box_group.add(box)

        # #create shappys
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 3:
                    shappy = Shappy_twoDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self, 3,
                                              terrain_matrix, self.screen_width, self.screen_height,
                                              False, self.policy, type_of_policy, self.fov_radius)
                    self.shappy_group.add(shappy)
                if self.terrain.matrix[line][column] == 4:
                    shappy = Shappy_twoDBoxes2(column * self.screen_ratio, line * self.screen_ratio, self,
                                              4, terrain_matrix, self.screen_width, self.screen_height,
                                              False, self.policy, type_of_policy, self.fov_radius)
                    self.shappy_group.add(shappy)

        self.current_state = []
        for line in terrain_matrix:
            temp_array = []
            for letter in line:
                temp_array.append(int(letter))
            self.current_state.append(temp_array)

        self.simulation_run_states = [self.current_state]

        self.initial_number_of_boxes = len(self.box_group)

    def render(self):
        # add background over all past images
        self.screen.fill((255, 255, 255))

        self.shappy_group.draw(self.screen)
        for shappy in self.shappy_group:
            color = (0, 0, 0)
            if shappy.color == 3:
                color = (0, 0, 255)
            elif shappy.color == 4:
                color = (255, 0, 0)
            pygame.draw.rect(self.screen, color,
                             (shappy.get_center()[0] - (self.fov_radius * self.screen_ratio), shappy.get_center()[1] - (self.fov_radius * self.screen_ratio),
                              self.fov_radius*2 * self.screen_ratio, self.fov_radius*2 * self.screen_ratio), 2)

        self.box_group.draw(self.screen)
        self.wall_group.draw(self.screen)

        score_rend = self.font.render("Score: " + str(self.score), 1, (255, 255, 255))
        self.screen.blit(score_rend, (30, 5))

        if self.show_automatic:
            automatic_rend = self.font.render("Automatic", 1, (255, 255, 255))
            self.screen.blit(automatic_rend, (self.screen_width / 2 - 30, 5))

        if time.time() < self.time_out_message_from_3:
            message_rend = self.font.render(str(self.message_from_3), 1, (0, 0, 255))
            self.screen.blit(message_rend, (10, self.screen_height-55))

        if time.time() < self.time_out_message_from_4:
            message_rend = self.font.render(str(self.message_from_4), 1, (255, 0, 0))
            self.screen.blit(message_rend, (10, self.screen_height-25))

        pygame.display.flip()

    def box_group_remove(self, input_x_pos, input_y_pos):
        for box in self.box_group:
            if box.x_pos == input_x_pos and box.y_pos == input_y_pos:
                self.box_group.remove(box)

    def update(self):

        if time.time() - self.time_interval > 3:
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
        #policy, states_numbered, P_table = pickle.load(fp)
        policy = pickle.load(fp)
        fp.close()

        return policy

    def set_new_terrain_matrix(self, shappy3_state, shappy4_state):
        self.current_state = shappy3_state

        for i in range(len(self.current_state)):
            for j in range(len(self.current_state[i])):
                if self.current_state[i][j] == shappy4_state[i][j]:
                    pass
                elif self.current_state[i][j] == 3 and shappy4_state[i][j] == 4:
                    self.current_state[i][j] = 7
                elif self.current_state[i][j] != 3 and shappy4_state[i][j] == 4:
                    self.current_state[i][j] = 4
                elif self.current_state[i][j] == 4 and shappy4_state[i][j] != 4:
                    self.current_state[i][j] = shappy4_state[i][j]
                for box in self.box_group:
                    if i == box.x_pos/self.screen_ratio and j == box.y_pos/self.screen_ratio:
                        self.current_state[i][j] = 2


    def print_array(self, array):
        for line in array:
            print(line)

    def send_message(self, _from, message):
        if _from == 4:
            self.message_from_4 = message
            self.time_out_message_from_4 = time.time() + 2
        if _from == 3:
            self.message_from_3 = message
            self.time_out_message_from_3 = time.time() + 2

