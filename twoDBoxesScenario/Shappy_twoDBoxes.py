from World import *
import math
from itertools import *


def get_center(sprite):
    return sprite.rect.x + sprite.rect.width / 2, sprite.rect.y + sprite.rect.height / 2


class Shappy_twoDBoxes(pygame.sprite.Sprite):
    auto = -1
    size = 30

    def __init__(self, ID, name, x_pos, y_pos, x_speed, y_speed, world, color, terrain_matrix, screen_width,
                 screen_height,
                 auto):

        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.old_x_pos = x_pos
        self.old_y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.world = world
        self.terrain_matrix = terrain_matrix
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type = None
        self.auto = auto

        self.color = color

        self.dir_vector = []

        self.calculate = False
        self.next_boxes = []
        self.current_box = math.inf
        self.next_box = []

        if self.color == 0:
            self.image = pygame.image.load("../Images/30_30_Red_Square.png")
            self.type = "NonCollaborative"
        elif self.color == 1:
            self.image = pygame.image.load("../Images/30_30_Blue_Square.png")
            self.type = "Collaborative"
        else:
            print("Unknown colour number: ", self.color)

        x_size, y_size = self.image.get_rect().size
        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.ID = ID
        self.name = name
        self.dir = (x_pos, y_pos)

        self.collided = False

        self.time_interval = time.time()

    def update(self, delta_t):
        if time.time() - self.time_interval > 0.001:
            if not self.auto:
                self.calculate = False
                keys = pygame.key.get_pressed()
                if self.color == 0:
                    if keys[pygame.K_LEFT]:
                        # self.x_pos -= self.x_speed * delta_t
                        self.x_pos -= 1
                    if keys[pygame.K_RIGHT]:
                        # self.x_pos += self.x_speed * delta_t
                        self.x_pos += 1
                    if keys[pygame.K_UP]:
                        self.y_pos -= 1
                    if keys[pygame.K_DOWN]:
                        self.y_pos += 1
                elif self.color == 1:
                    if keys[pygame.K_a]:
                        # self.x_pos -= self.x_speed * delta_t
                        self.x_pos -= 1
                    if keys[pygame.K_d]:
                        # self.x_pos += self.x_speed * delta_t
                        self.x_pos += 1
                    if keys[pygame.K_w]:
                        self.y_pos -= 1
                    if keys[pygame.K_s]:
                        self.y_pos += 1
            elif self.auto:
                self.auto_movement(delta_t)

            self.wall_collision_check()
            self.time_interval = time.time()

        if self.collided:
            self.x_pos = self.old_x_pos
            self.y_pos = self.old_y_pos
        else:
            self.rect.x = self.x_pos
            self.rect.y = self.y_pos

            self.dir = (self.x_pos - self.old_x_pos, self.y_pos - self.old_y_pos)

            self.old_x_pos = self.x_pos
            self.old_y_pos = self.y_pos

    def wall_collision_check(self):

        normalized_new_x_pos = round((self.x_pos * len(self.terrain_matrix[0])) / self.screen_width)
        normalized_new_y_pos = round((self.y_pos * len(self.terrain_matrix)) / self.screen_height)

        # Verifica se a nova posiçao está livre
        if self.terrain_matrix[normalized_new_y_pos][normalized_new_x_pos] == 1 \
                or self.terrain_matrix[normalized_new_y_pos][normalized_new_x_pos + 1] == 1 \
                or self.terrain_matrix[normalized_new_y_pos][normalized_new_x_pos + 2] == 1 \
                or self.terrain_matrix[normalized_new_y_pos + 1][normalized_new_x_pos] == 1 \
                or self.terrain_matrix[normalized_new_y_pos + 2][normalized_new_x_pos] == 1:
            self.collided = True
        else:
            self.collided = False

    def check_closest_box(self):
        closest_box = []
        minimum_distance = math.inf
        for box in self.world.box_group:
            if abs(math.sqrt(math.pow(box.x_pos - self.x_pos, 2) +
                             math.pow(box.y_pos - self.y_pos, 2))) < minimum_distance:
                minimum_distance = abs(math.sqrt(math.pow(box.x_pos - self.x_pos, 2) +
                                                 math.pow(box.y_pos - self.y_pos, 2)))
                closest_box = [box.x_pos, box.y_pos]
        return closest_box

    # isto só funciona com 2 agentes, não está otimizado para mais
    def calculate_all_possible_paths(self, boxes_group):
        paths_combinations = list()
        paths_permutations = list()
        paths_combinations.append([math.inf, boxes_group])

        if len(boxes_group) > 1:
            for i in range(1, int(len(boxes_group) / 2) + 1):
                combinations_list = list(combinations(boxes_group, i))
                for ind_combination in combinations_list:
                    temp_boxes_group_list = list(boxes_group)
                    for a in ind_combination:
                        temp_boxes_group_list.remove(a)
                    paths_combinations.append([ind_combination, temp_boxes_group_list])

            for path_comb in paths_combinations:
                if path_comb[0] == math.inf or len(path_comb[0]) == 1:  # aqui faz se o primeiro for inf ou só 1 posição
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

    def calculate_best_possible_paths(self, agent1_pos, agent2_pos, my_box_group):
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
                distance_agent_2 = abs(math.sqrt(math.pow(path[1][0][0] - agent2_pos[0], 2) +
                                                 math.pow(path[1][0][1] - agent2_pos[1], 2)))
                for i in range(1, len(path[1])):
                    distance_agent_2 += abs(math.sqrt(math.pow(path[1][i][0] - path[1][i - 1][0], 2) +
                                                      math.pow(path[1][i][1] - path[1][i - 1][1], 2)))
                if distance_agent_2 < minimum_distance_agent_2:
                    minimum_total_distance = distance_agent_1 + distance_agent_2
                    minimum_distance_agent_1 = distance_agent_1
                    minimum_path_agent_1 = path[0]
                    minimum_distance_agent_2 = distance_agent_2
                    minimum_path_agent_2 = path[1]
                    best_possible_path = path
            elif len(path[0]) == 1 and path[0][0] != math.inf:
                distance_agent_1 = abs(math.sqrt(math.pow(path[0][0][0] - agent1_pos[0], 2) +
                                                 math.pow(path[0][0][1] - agent1_pos[1], 2)))
                distance_agent_2 = abs(math.sqrt(math.pow(path[1][0][0] - agent2_pos[0], 2) +
                                                 math.pow(path[1][0][1] - agent2_pos[1], 2)))
                for i in range(1, len(path[1])):
                    distance_agent_2 += abs(math.sqrt(math.pow(path[1][i][0] - path[1][i - 1][0], 2) +
                                                      math.pow(path[1][i][1] - path[1][i - 1][1], 2)))
                if distance_agent_2 < minimum_distance_agent_2:
                    minimum_total_distance = distance_agent_1 + distance_agent_2
                    minimum_distance_agent_1 = distance_agent_1
                    minimum_path_agent_1 = path[0]
                    minimum_distance_agent_2 = distance_agent_2
                    minimum_path_agent_2 = path[1]
                    best_possible_path = path
            else:
                distance_agent_1 = abs(math.sqrt(math.pow(path[0][0][0] - agent1_pos[0], 2) +
                                                 math.pow(path[0][0][1] - agent1_pos[1], 2)))
                for i in range(1, len(path[0])):
                    distance_agent_1 += abs(math.sqrt(math.pow(path[0][i][0] - path[0][i - 1][0], 2) +
                                                      math.pow(path[0][i][1] - path[0][i - 1][1], 2)))
                    distance_agent_2 = abs(math.sqrt(math.pow(path[1][0][0] - agent2_pos[0], 2) +
                                                     math.pow(path[1][0][1] - agent2_pos[1], 2)))
                    for j in range(1, len(path[1])):
                        distance_agent_2 += abs(math.sqrt(math.pow(path[1][j][0] - path[1][j - 1][0], 2) +
                                                          math.pow(path[1][j][1] - path[1][j - 1][1], 2)))
                    if (distance_agent_1 + distance_agent_2) < minimum_total_distance:
                        minimum_total_distance = distance_agent_1 + distance_agent_2
                        minimum_distance_agent_1 = distance_agent_1
                        minimum_path_agent_1 = path[0]
                        minimum_distance_agent_2 = distance_agent_2
                        minimum_path_agent_2 = path[1]
                        best_possible_path = path

        return [minimum_total_distance, best_possible_path]

    def next_box_pos(self):
        if self.calculate:
            self.next_boxes = []
            my_box_group = []
            for box in self.world.box_group:
                my_box_group.append([box.x_pos, box.y_pos])

            agent2_pos = []
            for agent in self.world.shappy_group:
                if agent.x_pos != self.x_pos and agent.y_pos != self.y_pos:
                    agent2_pos = [agent.x_pos, agent.y_pos]

            if len(my_box_group) == 1:
                if abs(math.sqrt(math.pow(my_box_group[0][0] - self.x_pos, 2) +
                                 math.pow(my_box_group[0][1] - self.y_pos, 2))) \
                        < abs(math.sqrt(math.pow(my_box_group[0][0] - agent2_pos[0], 2) +
                                        math.pow(my_box_group[0][1] - agent2_pos[1], 2))):
                    self.next_box = my_box_group[0]
                else:
                    self.next_box = []
            else:
                best_possible_path_1 = self.calculate_best_possible_paths([self.x_pos, self.y_pos], agent2_pos, my_box_group)
                best_possible_path_2 = self.calculate_best_possible_paths(agent2_pos, [self.x_pos, self.y_pos], my_box_group)

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
                self.next_box = self.next_boxes[0]
                if abs(math.sqrt(math.pow(self.next_box[0] - self.x_pos, 2) +
                                 math.pow(self.next_box[1] - self.y_pos, 2))) < 20:
                    self.next_boxes = self.next_boxes[1: len(self.next_boxes)]
                    self.calculate = True  # PARA O AGENTE RECALCULAR CADA VEZ QUE APANHA UMA CAIXA, PODE-SE MUDAR PARA ELE TOMAR A DECISAO DAS CAIXAS APENAS NO INICIO
            except IndexError:
                pass

        return self.next_box

    def box_exists_in_world(self, next_box):
        if len(next_box) == 0:
            return True
        for box in self.world.box_group:
            if box.x_pos == next_box[0] and box.y_pos == next_box[1]:
                return True
        return False

    def auto_movement(self, delta_t):
        direction_vector = [self.y_pos, self.x_pos]
        if self.type == "NonCollaborative":
            exists = False
            closest_box = []
            while not exists and len(self.world.box_group) > 0:
                closest_box = self.check_closest_box()
                exists = self.box_exists_in_world(closest_box)
            if len(closest_box) != 0 and exists:
                direction_vector[0] = closest_box[1] - self.y_pos
                direction_vector[1] = closest_box[0] - self.x_pos
        elif self.type == "Collaborative":
            exists = False
            next_box = []
            while not exists and len(self.world.box_group) > 0:
                next_box = self.next_box_pos()
                exists = self.box_exists_in_world(next_box)
                if not exists:
                    self.calculate = True
            if len(next_box) != 0 and exists:
                direction_vector[0] = next_box[1] - self.y_pos
                direction_vector[1] = next_box[0] - self.x_pos

            # move
        # if direction_vector[0] != self.y_pos:
        if direction_vector[0] != 0:
            if (direction_vector[0] / abs(direction_vector[0]) * self.y_speed * delta_t) > 0:
                self.y_pos += 1
            else:
                self.y_pos -= 1

        #        if direction_vector[1] != self.x_pos:
        if direction_vector[1] != 0:
            if (direction_vector[1] / abs(direction_vector[
                                              1]) * self.x_speed * delta_t) > 0:  # self.x_pos += direction_vector[1] / abs(direction_vector[1]) * self.x_speed * delta_t
                self.x_pos += 1
            else:
                self.x_pos -= 1
