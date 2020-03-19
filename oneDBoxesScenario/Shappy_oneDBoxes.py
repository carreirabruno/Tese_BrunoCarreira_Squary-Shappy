from World import *
import math
from itertools import *
import sys
import numpy
import copy

numpy.set_printoptions(threshold=sys.maxsize)


def get_center(sprite):
    return sprite.rect.x + sprite.rect.width / 2, sprite.rect.y + sprite.rect.height / 2


class Shappy_oneDBoxes(pygame.sprite.Sprite):

    def __init__(self, name, x_pos, y_pos, world, color, terrain_matrix, screen_width, screen_height,
                 auto, policy):

        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.old_x_pos = x_pos
        self.old_y_pos = y_pos
        # self.x_speed = x_speed
        # self.y_speed = y_speed
        self.world = world
        self.terrain_matrix = terrain_matrix
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type = None
        self.auto = auto
        self.policy = policy

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
        self.name = name
        self.dir = (x_pos, y_pos)

        # self.collided = False
        self.time_interval = time.time()

        self.go_ahead = False
        self.current_state = []

        self.my_number = color
        if self.my_number == 3:
            self.other_number = 4
        else:
            self.other_number = 3

    def update(self, current_state, action_to_do):

        self.current_state = copy.deepcopy(current_state)
        for i in range(len(self.current_state)):
            if self.color == 3 and self.current_state[i] == 4:
                self.current_state[i] = 0
            if self.color == 4 and self.current_state[i] == 3:
                self.current_state[i] = 0

        # if time.time() - self.time_interval > 0.2:
        # if self.go_ahead:
        if not self.auto:
            self.calculate = False
            keys = pygame.key.get_pressed()
            if self.color == 3:
                if keys[pygame.K_a]:
                    # self.x_pos -= self.x_speed * delta_t
                    # self.x_pos -= 1
                    self.lefty()
                if keys[pygame.K_d]:
                    # self.x_pos += self.x_speed * delta_t
                    self.righty()
            elif self.color == 4:
                if keys[pygame.K_LEFT]:
                    # self.x_pos -= self.x_speed * delta_t
                    # self.x_pos -= 1 * self.world.screen_ratio
                    self.lefty()
                if keys[pygame.K_RIGHT]:
                    # self.x_pos += self.x_speed * delta_t
                    # self.x_pos += 1 * self.world.screen_ratio
                    self.righty()
        elif self.auto:
            # self.auto_movement(delta_t)
            self.auto_movement2(action_to_do)

        # self.wall_collision_check()
        self.time_interval = time.time()

        self.go_ahead = False

        # if self.collided:
        #     self.x_pos = self.old_x_pos
        #     self.y_pos = self.old_y_pos
        # else:
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

        self.dir = (self.x_pos - self.old_x_pos, self.y_pos - self.old_y_pos)

        self.old_x_pos = self.x_pos
        self.old_y_pos = self.y_pos

        return self.current_state

    def move_left(self):
        if not self.wall_collision_check(int(self.y_pos / self.world.screen_ratio),
                                         int(self.x_pos / self.world.screen_ratio) - 1):

            if self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio) - 1] == 2:
                self.world.box_group_remove(int(self.y_pos / self.world.screen_ratio),
                                            int(self.x_pos / self.world.screen_ratio) - 1)
                self.world.score += 1

            if self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio)] != self.other_number:
                self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio)] = 0

            self.x_pos -= 1 * self.world.screen_ratio

            if self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio)] != self.other_number:
                self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio)] = self.my_number

    def lefty(self):
        if not self.wall_collision_check(int(self.x_pos / self.world.screen_ratio) - 1):
            self.current_state[int(self.x_pos / self.world.screen_ratio)] = 0
            self.x_pos -= 1 * self.world.screen_ratio

            if self.current_state[int(self.x_pos / self.world.screen_ratio)] == 2:
                self.world.box_group_remove(int(self.x_pos / self.world.screen_ratio),
                                            int(self.y_pos / self.world.screen_ratio))
                self.world.score += 1

            self.current_state[int(self.x_pos / self.world.screen_ratio)] = self.color

    def move_right(self):
        if not self.wall_collision_check(int(self.y_pos / self.world.screen_ratio),
                                         int(self.x_pos / self.world.screen_ratio) + 1):

            if self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio) + 1] == 2:
                self.world.box_group_remove(int(self.y_pos / self.world.screen_ratio),
                                            int(self.x_pos / self.world.screen_ratio) + 1)
                self.world.score += 1

            if self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio)] != self.other_number:
                self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio)] = 0

            self.x_pos += 1 * self.world.screen_ratio

            if self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio)] != self.other_number:
                self.terrain_matrix[int(self.y_pos / self.world.screen_ratio)] \
                    [int(self.x_pos / self.world.screen_ratio)] = self.my_number

    def righty(self):
        if not self.wall_collision_check(int(self.x_pos / self.world.screen_ratio) + 1):
            self.current_state[int(self.x_pos / self.world.screen_ratio)] = 0
            self.x_pos += 1 * self.world.screen_ratio

            if self.current_state[int(self.x_pos / self.world.screen_ratio)] == 2:
                self.world.box_group_remove(int(self.x_pos / self.world.screen_ratio),
                                            int(self.y_pos / self.world.screen_ratio))
                self.world.score += 1

            self.current_state[int(self.x_pos / self.world.screen_ratio)] = self.color



    def wall_collision_check(self, pos_x):
        # Verifica se a nova posiçao está livre
        if self.current_state[pos_x] == 1:
            # or self.terrain_matrix[normalized_new_y_pos][normalized_new_x_pos + 1] == 1 \
            # or self.terrain_matrix[normalized_new_y_pos][normalized_new_x_pos + 2] == 1:
            return True
        else:
            return False

    def check_closest_box(self):
        closest_box_x = math.inf
        minimum_distance = math.inf
        for box in self.world.box_group:
            if abs(box.x_pos - self.x_pos) < minimum_distance:
                minimum_distance = abs(box.x_pos - self.x_pos)
                closest_box_x = box.x_pos
        return closest_box_x

    # isto só funciona com 2 agentes, não está otimizado para mais
    def calculate_all_possible_paths(self, boxes_group):
        paths_combinations = list()
        paths_permutations = list()
        paths_combinations.append([math.inf, boxes_group])

        if len(boxes_group) >= 2:
            for i in range(1, int(len(boxes_group) / 2) + 1):
                combinations_list = list(combinations(boxes_group, i))

                for ind_combination in combinations_list:
                    temp_boxes_group_list = list(boxes_group)
                    for a in ind_combination:
                        temp_boxes_group_list.remove(a)
                    paths_combinations.append([ind_combination, temp_boxes_group_list])

            for path_comb in paths_combinations:
                if path_comb[0] == math.inf or len(path_comb[0]) == 1:  # aqui faz se o primeiro for inf ou 1 só numero
                    ind_path_1 = path_comb[0]
                    temp_ind_list = list(permutations(path_comb[1], len(path_comb[1])))
                    for ind_path_2 in temp_ind_list:
                        paths_permutations.append([ind_path_1, ind_path_2])
                else:  # aqui faz se derem os dois para serem permutaveis
                    temp_ind_list_1 = list(permutations(path_comb[0], len(path_comb[0])))
                    temp_ind_list_2 = list(permutations(path_comb[1], len(path_comb[1])))

                    for ind_path_1 in temp_ind_list_1:
                        for ind_path_2 in temp_ind_list_2:
                            paths_permutations.append([ind_path_1, ind_path_2])

        return paths_permutations

    def calculate_best_possible_paths(self, agent1_pos_x, agent2_pos_x, my_box_group):
        best_possible_path = []
        possible_paths = self.calculate_all_possible_paths(my_box_group)

        minimum_distance_agent_1 = math.inf
        minimum_path_agent_1 = []
        minimum_distance_agent_2 = math.inf
        minimum_path_agent_2 = []
        minimum_total_distance = math.inf
        for path in possible_paths:
            if path[0] == math.inf:
                distance_agent_1 = 0
                distance_agent_2 = abs(path[1][0] - agent2_pos_x)
                for i in range(1, len(path[1])):
                    distance_agent_2 += abs(path[1][i] - path[1][i - 1])
                if distance_agent_2 < minimum_distance_agent_2:
                    minimum_total_distance = distance_agent_1 + distance_agent_2
                    minimum_distance_agent_1 = distance_agent_1
                    minimum_path_agent_1 = path[0]
                    minimum_distance_agent_2 = distance_agent_2
                    minimum_path_agent_2 = path[1]
                    best_possible_path = path
            elif len(path[0]) == 1 and path[0][0] != math.inf:
                distance_agent_1 = abs(path[0][0] - agent1_pos_x)
                distance_agent_2 = abs(path[1][0] - agent2_pos_x)
                for i in range(1, len(path[1])):
                    distance_agent_2 += abs(path[1][i] - path[1][i - 1])
                if distance_agent_2 < minimum_distance_agent_2:
                    minimum_total_distance = distance_agent_1 + distance_agent_2
                    minimum_distance_agent_1 = distance_agent_1
                    minimum_path_agent_1 = path[0]
                    minimum_distance_agent_2 = distance_agent_2
                    minimum_path_agent_2 = path[1]
                    best_possible_path = path
            else:
                distance_agent_1 = abs(path[0][0] - agent1_pos_x)
                for i in range(1, len(path[0])):
                    distance_agent_1 += abs(path[0][i] - path[0][i - 1])
                    distance_agent_2 = abs(path[1][0] - agent2_pos_x)
                    for j in range(1, len(path[1])):
                        distance_agent_2 += abs(path[1][j] - path[1][j - 1])
                    if (distance_agent_1 + distance_agent_2) < minimum_total_distance:
                        minimum_total_distance = distance_agent_1 + distance_agent_2
                        minimum_distance_agent_1 = distance_agent_1
                        minimum_path_agent_1 = path[0]
                        minimum_distance_agent_2 = distance_agent_2
                        minimum_path_agent_2 = path[1]
                        best_possible_path = path

        return [minimum_total_distance, best_possible_path]

    def next_box(self):
        if self.calculate:
            self.next_boxes = []
            my_box_group = []
            for box in self.world.box_group:
                my_box_group.append(box.x_pos)

            agent2_x_pos = 0
            for agent in self.world.shappy_group:
                if agent.x_pos != self.x_pos:
                    agent2_x_pos = agent.x_pos

            if len(my_box_group) == 1:
                if abs(my_box_group[0] - self.x_pos) < abs(my_box_group[0] - agent2_x_pos):
                    self.next_box_x = my_box_group[0]
                else:
                    self.next_box_x = math.inf
            else:
                best_possible_path_1 = self.calculate_best_possible_paths(self.x_pos, agent2_x_pos, my_box_group)
                best_possible_path_2 = self.calculate_best_possible_paths(agent2_x_pos, self.x_pos, my_box_group)

                if best_possible_path_1[0] < best_possible_path_2[0]:
                    if len(best_possible_path_1[1]) == 0:
                        self.next_boxes = []
                    else:
                        self.next_boxes = best_possible_path_1[1][0]
                else:
                    if len(best_possible_path_2[1]) == 0:
                        self.next_boxes = []
                    else:
                        self.next_boxes = best_possible_path_2[1][1]

                self.calculate = False
            try:
                self.next_box_x = self.next_boxes[0]
                if abs(self.next_box_x - self.x_pos) < 20:
                    self.next_boxes = self.next_boxes[1: len(self.next_boxes)]

                    self.calculate = True  # PARA O AGENTE RECALCULAR CADA VEZ QUE APANHA UMA CAIXA, PODE-SE MUDAR PARA ELE TOMAR A DECISAO DAS CAIXAS APENAS NO INICIO
            except IndexError:
                pass

        return self.next_box_x

    def box_exists_in_world(self, next_box_x):
        if next_box_x == math.inf:
            return True
        for box in self.world.box_group:
            if box.x_pos == next_box_x:
                return True
        return False

    def auto_movement(self, delta_t):
        direction_vector = [self.y_pos, self.x_pos]
        if self.type == "NonCollaborative":
            exists = False
            closest_box_x = math.inf
            while not exists and len(self.world.box_group) > 0:
                closest_box_x = self.check_closest_box()
                exists = self.box_exists_in_world(closest_box_x)
            if closest_box_x != math.inf and exists:
                direction_vector[1] = closest_box_x - self.x_pos
        elif self.type == "Collaborative":
            exists = False
            next_box_x = math.inf
            while not exists and len(self.world.box_group) > 0:
                next_box_x = self.next_box()
                exists = self.box_exists_in_world(next_box_x)
                if not exists:
                    self.calculate = True
            if next_box_x != math.inf and exists:
                direction_vector[1] = next_box_x - self.x_pos

        if direction_vector[1] != self.x_pos:
            # self.x_pos += direction_vector[1] / abs(direction_vector[1]) * self.x_speed * delta_t
            if (direction_vector[1] / abs(direction_vector[1]) * delta_t) > 0:
                if self.type == "NonCollaborative":
                    self.move_right(3, 4)
                else:
                    self.move_right(4, 3)
            else:
                if self.type == "NonCollaborative":
                    self.move_left(3, 4)
                else:
                    self.move_left(4, 3)

    def auto_movement2(self, action_to_do):

        #print(self.color, " ", action_to_do)

        if action_to_do == "STAY":
            pass
        elif action_to_do == "LEFT":
            self.lefty()
        elif action_to_do == "RIGHT":
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
        #
        # other_agent_pos = int(self.x_pos / self.world.screen_ratio)
        # for i in range(len(self.current_state)):
        #     if self.current_state[i] == 3 and i != self.x_pos / self.world.screen_ratio \
        #             or self.current_state[i] == 4 and i != self.x_pos / self.world.screen_ratio:
        #         other_agent_pos = i
        # 
        # policy_state = []
        # for state in self.policy:
        #     comparison = self.current_state == state[0]
        #     if comparison.all():
        #         policy_state = state
        #         break
        #     # elif self.current_state == state[0] and other_agent_pos == state[1][0] \
        #     #         and (self.x_pos / self.world.screen_ratio) == state[1][1]:
        #     #     policy_state = state
        #     #     break
        # 
        # if int(self.x_pos / self.world.screen_ratio) <= other_agent_pos and self.color == 3:
        #     if policy_state[1] == STAY_LEFT or policy_state[1] == STAY_RIGHT:
        #         pass
        #     elif policy_state[1] == LEFT_STAY or policy_state[1] == LEFT_LEFT or policy_state[1] == LEFT_RIGHT:
        #         self.move_left(3, 4)
        #     elif policy_state[1] == RIGHT_STAY or policy_state[1] == RIGHT_LEFT or policy_state[1] == RIGHT_RIGHT:
        #         self.move_right(3, 4)
        # elif int(self.x_pos / self.world.screen_ratio) <= other_agent_pos and self.color == 4:
        #     if policy_state[1] == STAY_LEFT or policy_state[1] == STAY_RIGHT:
        #         pass
        #     elif policy_state[1] == LEFT_STAY or policy_state[1] == LEFT_LEFT or policy_state[1] == LEFT_RIGHT:
        #         self.move_left(4, 3)
        #     elif policy_state[1] == RIGHT_STAY or policy_state[1] == RIGHT_LEFT or policy_state[1] == RIGHT_RIGHT:
        #         self.move_right(4, 3)
        # 
        # if int(self.x_pos / self.world.screen_ratio) > other_agent_pos and self.color == 3:
        #     if policy_state[1] == LEFT_STAY or policy_state[1] == RIGHT_STAY:
        #         pass
        #     elif policy_state[1] == STAY_LEFT or policy_state[1] == LEFT_LEFT or policy_state[1] == RIGHT_LEFT:
        #         self.move_left(3, 4)
        #     elif policy_state[1] == STAY_RIGHT or policy_state[1] == LEFT_RIGHT or policy_state[1] == RIGHT_RIGHT:
        #         self.move_right(3, 4)
        # elif int(self.x_pos / self.world.screen_ratio) > other_agent_pos and self.color == 4:
        #     if policy_state[1] == LEFT_STAY or policy_state[1] == RIGHT_STAY:
        #         pass
        #     elif policy_state[1] == STAY_LEFT or policy_state[1] == LEFT_LEFT or policy_state[1] == RIGHT_LEFT:
        #         self.move_left(4, 3)
        #     elif policy_state[1] == STAY_RIGHT or policy_state[1] == LEFT_RIGHT or policy_state[1] == RIGHT_RIGHT:
        #         self.move_right(4, 3)

        # if self.color == 3:
        #     if policy_state[1] == STAY_LEFT or policy_state[1] == STAY_RIGHT:
        #         pass
        #     elif policy_state[1] == LEFT_STAY or policy_state[1] == LEFT_LEFT or policy_state[1] == LEFT_RIGHT:
        #         self.move_left(3, 4)
        #     elif policy_state[1] == RIGHT_STAY or policy_state[1] == RIGHT_LEFT or policy_state[1] == RIGHT_RIGHT:
        #         self.move_right(3, 4)
        # elif self.color == 4:
        #     if policy_state[1] == LEFT_STAY or policy_state[1] == RIGHT_STAY:
        #         pass
        #     elif policy_state[1] == STAY_LEFT or policy_state[1] == LEFT_LEFT or policy_state[1] == RIGHT_LEFT:
        #         self.move_left(4, 3)
        #     elif policy_state[1] == STAY_RIGHT or policy_state[1] == LEFT_RIGHT or policy_state[1] == RIGHT_RIGHT:
        #         self.move_right(4, 3)

#         if self.x_pos/self.world.screen_ratio == policy_state[1][0]:
#             if policy_state[2] == STAY_LEFT or policy_state[2] == STAY_RIGHT:
# #            if policy_state[2] == STAY_STAY or policy_state[2] == STAY_LEFT or policy_state[2] == STAY_RIGHT:
#                 pass
#             elif policy_state[2] == LEFT_STAY or policy_state[2] == LEFT_LEFT or policy_state[2] == LEFT_RIGHT:
#                 if self.type == "NonCollaborative":
#                     self.move_left(3, 4)
#                 else:
#                     self.move_left(4, 3)
#             elif policy_state[2] == RIGHT_STAY or policy_state[2] == RIGHT_LEFT or policy_state[2] == RIGHT_RIGHT:
#                 if self.type == "NonCollaborative":
#                     self.move_right(3, 4)
#                 else:
#                     self.move_right(4, 3)
#         elif self.x_pos/self.world.screen_ratio == policy_state[1][1]:
#             if policy_state[2] == LEFT_STAY or policy_state[2] == RIGHT_STAY:
# #            if policy_state[2] == STAY_STAY or policy_state[2] == LEFT_STAY or policy_state[2] == RIGHT_STAY:
#                 pass
#             elif policy_state[2] == STAY_LEFT or policy_state[2] == LEFT_LEFT or policy_state[2] == RIGHT_LEFT:
#                 if self.type == "NonCollaborative":
#                     self.move_left(3, 4)
#                 else:
#                     self.move_left(4, 3)
#             elif policy_state[2] == STAY_RIGHT or policy_state[2] == LEFT_RIGHT or policy_state[2] == RIGHT_RIGHT:
#                 if self.type == "NonCollaborative":
#                     self.move_right(3, 4)
#                 else:
#                     self.move_right(4, 3)
