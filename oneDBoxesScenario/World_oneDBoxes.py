import pygame
from oneDBoxesScenario.Terrain_oneDBoxes import *
from oneDBoxesScenario.Box_oneDBoxes import *
from oneDBoxesScenario.Shappy_oneDBoxes import *
from copy import *
import pickle


class World_oneDBoxes(object):

    def __init__(self, terrain, policy_file):

        self.last_update = None

        self.screen_ratio = 30

        self.terrain = terrain

        self.policy = self.get_policy(policy_file)

        self.screen_width = len(self.terrain.matrix[0]) * self.screen_ratio
        self.screen_height = len(self.terrain.matrix) * self.screen_ratio

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        self.fov_radius = 100

        self.font = pygame.font.SysFont("Times New Roman", 20)

        self.score = 0

        self.shappy_speed = 100  # não faz nada, eles mexem-se sempre 1 casa

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
        # for box_var in self.terrain.initial_boxes_list:
        #     box = Box(box_var[0] * self.screen_ratio, box_var[1] * self.screen_ratio, self)
        #     self.box_group.add(box)

        # #create boxes
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 2:
                    box = Box_oneDBoxes(column * self.screen_ratio, line * self.screen_ratio)
                    self.box_group.add(box)

        # #create shappys
        for column in range(len(self.terrain.matrix[0])):
            for line in range(len(self.terrain.matrix)):
                if self.terrain.matrix[line][column] == 3:
                    shappy = Shappy_oneDBoxes('A', column * self.screen_ratio, line * self.screen_ratio, self, 3,
                                              self.terrain.matrix, self.screen_width, self.screen_height,
                                              False, self.policy)
                    self.shappy_group.add(shappy)
                if self.terrain.matrix[line][column] == 4:
                    shappy = Shappy_oneDBoxes('B', column * self.screen_ratio, line * self.screen_ratio, self,
                                              4, self.terrain.matrix, self.screen_width, self.screen_height,
                                              False, self.policy)
                    self.shappy_group.add(shappy)

        # #create shappys
        # for shappy_var in self.terrain.initial_shappy_list:
        #
        #     shappy = Shappy_oneDBoxes(shappy_var[0],shappy_var[1], shappy_var[3] * self.screen_ratio, shappy_var[2] * self.screen_ratio,
        #                         self.shappy_speed, self.shappy_speed, self, shappy_var[4],
        #                         self.terrain.matrix, self.screen_width, self.screen_height, False)
        #     self.shappy_group.add(shappy)

        self.current_state = []
        for line in self.terrain.matrix:
            # if 2 in line:
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

    # def check_collisions(self):
    #
    #     for shappy in self.shappy_group:
    #         normalized_x_pos = round((shappy.x_pos * len(self.terrain.matrix[0])) / self.screen_width)
    #         normalized_y_pos = round((shappy.y_pos * len(self.terrain.matrix)) / self.screen_height)
    #
    #         if self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos] == 2:
    #             self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos] = 0
    #             self.box_group_remove(normalized_x_pos * self.screen_ratio,
    #                                   (normalized_y_pos + 1) * self.screen_ratio)
    #             self.score += 1
    #         # elif self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos + 1] == 2:
    #         #     self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos + 1] = 0
    #         #     self.box_group_remove((normalized_x_pos + 1) * self.screen_ratio,
    #         #                           (normalized_y_pos + 1) * self.screen_ratio)
    #         #     self.score += 1
    #         # elif self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos - 1] == 2:
    #         #     self.terrain.matrix[normalized_y_pos + 1][normalized_x_pos - 1] = 0
    #         #     self.box_group_remove((normalized_x_pos - 1) * self.screen_ratio,
    #         #                           (normalized_y_pos + 1) * self.screen_ratio)
    #         #     self.score += 1

    def box_group_remove(self, input_x_pos, input_y_pos):
        x_pos = input_x_pos * self.screen_ratio
        y_pos = input_y_pos * self.screen_ratio
        for box in self.box_group:
            if box.x_pos == x_pos and box.y_pos == y_pos:
                self.box_group.remove(box)

    def update(self):

        if time.time() - self.time_interval > 1:
            self.time_interval = time.time()
            # if self.last_update is None:
            #     self.last_update = time.time()
            #     return

            # delta_t = time.time() - self.last_update

            actions_to_do = self.get_current_action_to_do()

            shappy3_state = []
            shappy4_state = []
            for shappy in self.shappy_group:
                if shappy.color == 3:
                    shappy3_state = shappy.update(self.current_state, actions_to_do[0])
                if shappy.color == 4:
                    shappy4_state = shappy.update(self.current_state, actions_to_do[1])
            self.set_new_terrain_matrix(shappy3_state, shappy4_state)

            # self.check_collisions()

            self.simulation_run_states.append(self.current_state)

            self.score = abs(self.initial_number_of_boxes - len(self.box_group))

            self.last_update = time.time()

    # def get_policy(self, policy_file):
    #     policy = []
    #
    #     f = open(policy_file, "r")
    #     save = True
    #     appended_line = ""
    #
    #     lines = f.readlines()
    #     print(len(lines))
    #
    #     for line in lines:
    #         if line == lines[-1]:
    #             phrase = ""
    #             for letter in line:
    #                 phrase += letter
    #             appended_line += phrase
    #
    #         if "State" in line or line == lines[-1]:
    #             state = []
    #             pos = []
    #             save = True
    #             if len(appended_line) > 0:
    #                 temp_appended_line = str(appended_line).replace('\'', '')
    #                 temp_appended_line = str(temp_appended_line).replace(',', '')
    #                 temp_appended_line = str(temp_appended_line).replace('[S t a t e ( m a p = [', '')
    #                 temp_appended_line = str(temp_appended_line).replace('\\n', '')
    #                 temp_appended_line = str(temp_appended_line).replace(')', '')
    #                 temp_appended_line = str(temp_appended_line).replace('   ]', '')
    #
    #                 # Criar o state
    #                 split1 = str(temp_appended_line).split("]")
    #                 state_string = split1[0].replace(' ', '')
    #                 state_string = state_string.replace('.', '')
    #                 print(line)
    #                 print(state_string)
    #                 for letter in state_string:
    #                     state.append(int(letter))
    #
    #                 split2 = str(split1[1]).split("[")
    #                 split3 = str(split2[0]).split('        ')
    #
    #                 pos_string = str(split3[0]).replace(' ', '')
    #                 pos_string = str(pos_string).replace('first_shappy_pos=', '')
    #                 pos_string = str(pos_string).split('second_shappy_pos=')
    #                 pos.append(int(pos_string[0]))
    #                 pos.append(int(pos_string[1]))
    #
    #                 action = int(split3[1])
    #
    #                 # if 2 in state and action == 0:
    #                 #     print(appended_line)
    #
    #                 policy.append([state, pos, action])
    #             appended_line = []
    #
    #         if save:
    #             phrase = ""
    #             for letter in line:
    #                 phrase += letter
    #             appended_line += phrase
    #
    #     f.close()
    #     # print("before ", len(policy))
    #     #
    #     # temp_policy = []
    #     # trash_policy = []
    #     # for line in policy:
    #     #     temp_policy.append(line[0])
    #     #
    #     # #for line in temp_policy:
    #     # for i in range(len(temp_policy)):
    #     #     if temp_policy[i] in trash_policy:
    #     #         for line in policy:
    #     #             if line[0] == temp_policy[i]:
    #     #                 policy.remove(line)
    #     #     else:
    #     #         trash_policy.append(temp_policy[i])
    #     #
    #     #
    #     # print("after ", len(policy))
    #
    #     return policy

    def get_policy(self, policy_file):
        fp = open(policy_file, "rb")  # Unpickling
        policy, states_numbered, P_table = pickle.load(fp)
        fp.close()
        return policy

        # policy = []
        #
        # f = open(policy_file, "r")
        #
        # save = True
        # appended_line = ""
        #
        # lines = f.readlines()
        #
        # for line in lines:
        #     # if line is lines[-1]:
        #     #     phrase = ""
        #     #     for letter in line:
        #     #         phrase += letter
        #     #     appended_line += phrase
        #
        #     if "State" in line or "Q_table" in line:  # line == lines[-1]:
        #         state = []
        #         pos = []
        #         save = True
        #         if len(appended_line) > 0:
        #
        #             temp_appended_line = str(appended_line).replace('\'', '')
        #
        #             temp_appended_line = str(temp_appended_line).replace(',', '')
        #             split_appended_line = str(temp_appended_line).split('& &')
        #
        #             # Criar o state
        #             state_appended_line = split_appended_line[0]
        #             state_appended_line = state_appended_line.replace(' ', '')
        #             state_appended_line = state_appended_line.replace('[State(map=[', '')
        #             state_appended_line = state_appended_line.replace('.', '')
        #             state_appended_line = state_appended_line.replace(')', '')
        #             state_appended_line = state_appended_line.replace(']', '')
        #             state_appended_line = state_appended_line.replace('[', '')
        #             state_appended_line = state_appended_line.replace('\\n', '')
        #
        #             state_items = state_appended_line.split('&')
        #
        #             map = []
        #
        #             for item in state_items[0]:
        #                 if item == "[":
        #                     pass
        #                 else:
        #                     map.append(int(item))
        #
        #             # Criar a action
        #             action_appended_line = split_appended_line[1]
        #             action_appended_line = action_appended_line.replace(' ', '')
        #             action = int(action_appended_line)
        #
        #             policy.append([map, action])
        #
        #         appended_line = []
        #
        #     if save:
        #         phrase = ""
        #         for letter in line:
        #             phrase += letter
        #         appended_line += phrase
        #
        # f.close()
        #
        # return policy

    def get_current_action_to_do(self):

        # current_state = np.array(current_state)
        # if 3 not in current_state:
        #     current_state = np.where(current_state == 4, 7, current_state)
        # if 4 not in current_state:
        #     current_state = np.where(current_state == 3, 7, current_state)
        actions = -1
        for state in self.policy:
            equal = True
            # comparison = current_state == state[0]
            for i in range(len(state[0])):
                if self.current_state[i] != state[0][i]:
                    equal = False
            # if comparison.all():
            if equal:
                actions = state[1]
                break

        if actions == 0:
            actions = "STAY_LEFT"
        elif actions == 1:
            actions = "STAY_RIGHT"
        elif actions == 2:
            actions = "LEFT_STAY"
        elif actions == 3:
            actions = "LEFT_LEFT"
        elif actions == 4:
            actions = "LEFT_RIGHT"
        elif actions == 5:
            actions = "RIGHT_STAY"
        elif actions == 6:
            actions = "RIGHT_LEFT"
        elif actions == 7:
            actions = "RIGHT_RIGHT"

        actions = str(actions).split("_")

        return actions

    def set_new_terrain_matrix(self, shappy3_state, shappy4_state):
        self.current_state = []
        for i in range(len(shappy3_state)):
            if shappy3_state[i] == shappy4_state[i]:
                self.current_state.append(shappy3_state[i])
            elif shappy3_state[i] == 2 and shappy4_state[i] != 2 or shappy3_state[i] == 0 and shappy4_state[i] == 4:
                self.current_state.append(shappy4_state[i])
            elif shappy3_state[i] != 2 and shappy4_state[i] == 2 or shappy3_state[i] == 3 and shappy4_state[i] == 0:
                self.current_state.append(shappy3_state[i])
            elif shappy3_state[i] == 3 and shappy4_state[i] == 4:
                self.current_state.append(7)

