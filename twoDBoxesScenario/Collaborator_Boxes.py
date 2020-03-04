import pygame
import math
from itertools import *
import datetime
import os
import time
from twoDBoxesScenario.World_Boxes import *


class Collaborator_Boxes(object):

    def __init__(self, world, simulation):
        self.world = world

        self.agent1_old_distance = math.inf
        self.agent2_old_distance = math.inf

        self.agent1_old_position = math.inf
        self.agent2_old_position = math.inf

        self.behaviour_with_distances = []

        self.agent1_points = 0
        self.agent1_ID = 0
        self.agent2_points = 0
        self.agent2_ID = 0
        self.max_agent1_points = 0
        self.max_agent2_points = 0

        self.freeze_counter1 = 0
        self.freeze_counter2 = 0

        self.write = False
        self.avg_collaborative_total_score = 0
        self.avg_non_collaborative_total_score = 0

        self.box_group = []
        for box in self.world.box_group:
            self.box_group.append(box.x_pos)

        self.agents_current_positions = []
        for agent in self.world.shappy_group:
            self.agents_current_positions.append([agent.ID, agent.x_pos])

        self.best_behaviour = self.get_best_collaboration_behaviour()
        self.agent1_ID = self.best_behaviour[0][0][0]
        self.agent2_ID = self.best_behaviour[1][0][0]
        for item in self.best_behaviour:
            self.agents_current_positions.append(item[0][0])

        if not simulation:
            self.minimum_behaviours()

        self.agent1_old_distance = abs(self.best_behaviour[0][1][0] - self.best_behaviour[0][0][1])
        self.agent2_old_distance = abs(self.best_behaviour[1][1][0] - self.best_behaviour[1][0][1])

        self.time_interval = time.time()

    def update(self):

        if time.time() - self.time_interval > 0.05:
            if len(self.world.box_group) == 0 and self.write:
                self.write_in_txt()
                quit()
            else:
                self.agents_current_positions = []
                for agent in self.world.shappy_group:
                    self.agents_current_positions.append([agent.ID, agent.x_pos])
                changed = self.check_boxes_changes()

                if changed:
                    self.best_behaviour = self.get_best_collaboration_behaviour()
                    self.agent1_old_distance = math.inf
                    self.agent2_old_distance = math.inf
                    self.agent1_old_position = self.best_behaviour[0][0][1]
                    self.agent2_old_position = self.best_behaviour[1][0][1]

            # self.analyse_behaviour1(self.best_behaviour)
                self.analyse_behaviour2()
            self.time_interval = time.time()

    def write_in_txt(self):
        f = open("twoDBoxes_CollaborationResults.txt", "a+")
        agent_list = []
        for agent in self.world.shappy_group:
            agent_list.append([agent.type, agent.ID])

        total_points = self.agent1_points + self.agent2_points
        datetime_object = datetime.datetime.now()
        datetime_object = datetime_object.strftime("DATE_%d-%m-%Y___TIME_%H-%M-%S")
        f.write("%s \n" % datetime_object)
        f.write(("AGENT1 -> %s - %s -> %d\r") % (agent_list[0][1], agent_list[0][0], self.agent1_points))
        f.write(("AGENT2 -> %s - %s -> %d\r") % (agent_list[1][1], agent_list[1][0], self.agent2_points))
        f.write("TOTAL -> %d\r" % total_points)

        # if abs(total_points - self.avg_non_collaborative_total_score) \
        #         < abs(total_points - self.avg_collaborative_total_score):
        #     f.write("NON COLLABORATIVE BEHAVIOUR\r")
        # else:
        #     f.write("COLLABORATIVE BEHAVIOUR\r")

        scaled_zero_to_ten = int(((total_points - self.avg_non_collaborative_total_score) /
                (self.avg_collaborative_total_score - self.avg_non_collaborative_total_score)) * 10)

        if scaled_zero_to_ten > 10:
            scaled_zero_to_ten = 10
        elif scaled_zero_to_ten < 0:
            scaled_zero_to_ten = 0

        f.write("SCALED FROM 0 TO 10 -> %d \r" %scaled_zero_to_ten)

        if scaled_zero_to_ten  < 3:
            f.write("NON COLLABORATIVE BEHAVIOUR\r\n")
        elif scaled_zero_to_ten < 8:
            f.write("NEUTRAL BEHAVIOUR\r\n")
        else:
            f.write("COLLABORATIVE BEHAVIOUR\r\n")

        f.close()

    def get_best_collaboration_behaviour(self):
        best_collaborative_behaviour = []

        self.box_group = []
        for box in self.world.box_group:
            self.box_group.append(box.x_pos)

        agent_list = []
        for agent in self.world.shappy_group:
            agent_list.append([agent.ID, agent.x_pos])

        if len(self.box_group) == 0:
            print("NO MORE BOXES")

        elif len(self.box_group) == 1:
            if abs(self.box_group[0] - self.agents_current_positions[0][1]) < abs(self.box_group[0] - self.agents_current_positions[1][1]):
                best_collaborative_behaviour = [[self.agents_current_positions[0], self.box_group], [self.agents_current_positions[1], math.inf]]
            else:
                best_collaborative_behaviour = [[self.agents_current_positions[0], math.inf], [self.agents_current_positions[1], self.box_group]]
        else:
            best_possible_path_1 = self.calculate_best_possible_paths(self.agents_current_positions[0], self.agents_current_positions[1], self.box_group)
            best_possible_path_2 = self.calculate_best_possible_paths(self.agents_current_positions[1], self.agents_current_positions[0], self.box_group)

            # CRIA-SE AQUI A COMBINAÇÃO AGENTE-BOX PARA ANALISAR OS MOVIMENTOS
            if best_possible_path_1[0] <= best_possible_path_2[0]:
                best_collaborative_behaviour = [[self.agents_current_positions[0], best_possible_path_1[1][0]],
                                                [self.agents_current_positions[1], best_possible_path_1[1][1]]]
            else:
                best_collaborative_behaviour = [[self.agents_current_positions[0], best_possible_path_1[1][1]],
                                                [self.agents_current_positions[1], best_possible_path_1[1][0]]]

        return best_collaborative_behaviour

    def analyse_behaviour1(self, behaviour_array):
        if self.agent1_old_distance == math.inf and self.agent2_old_distance == math.inf:
            if behaviour_array[0][1] != math.inf:
                self.agent1_old_distance = abs(behaviour_array[0][1][0] - behaviour_array[0][0][1])
            else:
                self.agent1_old_distance = behaviour_array[0][0][1]
            if behaviour_array[1][1] != math.inf:
                self.agent2_old_distance = abs(behaviour_array[1][1][0] - behaviour_array[1][0][1])
            else:
                self.agent2_old_distance = behaviour_array[1][0][1]

        else:
            agent_list = []
            for agent in self.world.shappy_group:
                agent_list.append([agent.ID, agent.x_pos])

            if behaviour_array[0][1] != math.inf and abs(                   #tem objetivo mas não se mexe
                    behaviour_array[0][1][0] - agent_list[0][1]) == self.agent1_old_distance:
                self.freeze_counter1 += 1
                # if self.freeze_counter1 == 500:
                #     self.agent1_points -= 3
                #     self.freeze_counter1 = 0
            elif behaviour_array[0][1] != math.inf and abs(
                    behaviour_array[0][1][0] - agent_list[0][1]) < self.agent1_old_distance:   #está a aproximar-se do objetivo
                self.agent1_old_distance = abs(behaviour_array[0][1][0] - agent_list[0][1])
                self.agent1_points += 1
            elif behaviour_array[0][1] != math.inf and abs(behaviour_array[0][1][0] - agent_list[
                0][1]) > self.agent1_old_distance:                                                  #está a afastar-se do objetivo
                # self.agent1_old_distance = abs(behaviour_array[0][1][0] - agent_list[0])
                self.agent1_points -= 1
            elif behaviour_array[0][1] == math.inf and abs(self.agent1_old_distance - agent_list[0][1]) < 50:  #não tem objetivo e está quieto
                self.agent1_points += 1
            elif behaviour_array[0][1] == math.inf and abs(self.agent1_old_distance - agent_list[0][1]) > 50:  #não tem objetivo e está a mover-se (desperdicio de ações e pode estar a ser greedy)
                self.agent1_points -= 1

            if behaviour_array[1][1] != math.inf and abs(
                    behaviour_array[1][1][0] - agent_list[1][1]) == self.agent2_old_distance:
                self.freeze_counter2 += 1
                # if self.freeze_counter2 == 500:
                #     self.agent2_points -= 3
                #     self.freeze_counter2 = 0
            elif behaviour_array[1][1] != math.inf and abs(
                    behaviour_array[1][1][0] - agent_list[1][1]) < self.agent2_old_distance:
                self.agent2_old_distance = abs(behaviour_array[1][1][0] - agent_list[1][1])
                self.agent2_points += 1
            elif behaviour_array[1][1] != math.inf and abs(
                    behaviour_array[1][1][0] - agent_list[1][1]) > self.agent2_old_distance:
                # self.agent2_old_distance = abs(behaviour_array[1][1][0] - agent_list[1])
                self.agent2_points -= 1
            elif behaviour_array[1][1] == math.inf and abs(self.agent2_old_distance - agent_list[1][1]) < 50:
                self.agent2_points += 1
            elif behaviour_array[1][1] == math.inf and abs(self.agent2_old_distance - agent_list[1][1]) > 50:
                self.agent2_points -= 1

    def analyse_behaviour2(self):

        #create the list else update the agents positions
        if len(self.behaviour_with_distances) == 0:
            for item in self.best_behaviour:
                temp_array = []
                for agent in self.agents_current_positions:
                    if agent[0] == item[0][0]:
                        temp_array.append(agent)
                if item[1] != math.inf:
                    for local in item[1]:
                        distance = abs(local - item[0][1])
                        temp_array.append([local, distance])
                else:
                    temp_array.append(math.inf)
                self.behaviour_with_distances.append(temp_array)
        else:
            for item in self.behaviour_with_distances:
                for agent in self.agents_current_positions:
                    if item[0][0] == agent[0]:
                        item[0] = agent

        #---------------------------------Give points according to the movement----------------------------------------
        agent1_closer = False
        agent1_further = False
        agent2_closer = False
        agent2_further = False

        for item in self.behaviour_with_distances:
            if item[1] != math.inf:
                for object in item:
                    if isinstance(object[0], str):
                        pass
                    else:
                        if abs(object[0] - item[0][1]) < object[1]:
                            if item[0][0] == self.agent1_ID:
                                agent1_closer = True
                            elif item[0][0] == self.agent2_ID:
                                agent2_closer = True
                            object[1] = abs(object[0] - item[0][1])
                        elif abs(object[0] - item[0][1]) > (object[1] + 30):
                            if item[0][0] == self.agent1_ID:
                                agent1_further = True
                            elif item[0][0] == self.agent2_ID:
                                agent2_further = True
            else:
                if item[0][0] == self.agent1_ID:
                    if abs(item[0][1] - self.agent1_old_position) > 20:
                        self.agent1_points -= 3
                        self.agent1_old_position = item[0][1]
                elif item[0][0] == self.agent2_ID:

                    if abs(item[0][1] - self.agent2_old_position) > 20:
                        self.agent2_points -= 3
                        self.agent2_old_position = item[0][1]

        if agent1_closer:
            self.agent1_points += 1
        elif not agent1_closer and agent1_further:
            self.agent1_points -= 3

        if agent2_closer:
            self.agent2_points += 1
        elif not agent2_closer and agent2_further:
            self.agent2_points -= 3


        #update the list with the correct distances
        self.behaviour_with_distances = []
        for item in self.best_behaviour:
            temp_array = []
            for agent in self.agents_current_positions:
                if agent[0] == item[0][0]:
                    temp_array.append(agent)
            if item[1] != math.inf:
                for local in item[1]:
                    distance = abs(local - item[0][1])
                    temp_array.append([local, distance])
            else:
                temp_array.append(math.inf)
            self.behaviour_with_distances.append(temp_array)

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

    # isto só funciona com 2 agentes, não está otimizado para mais
    def calculate_best_possible_paths(self, agent1, agent2, boxes_group):
        best_possible_path = []
        possible_paths = self.calculate_all_possible_paths(boxes_group)

        minimum_distance_agent_1 = math.inf
        minimum_path_agent_1 = []
        minimum_distance_agent_2 = math.inf
        minimum_path_agent_2 = []
        minimum_total_distance = math.inf
        for path in possible_paths:
            if path[0] == math.inf:
                distance_agent_1 = 0
                distance_agent_2 = abs(path[1][0] - agent2[1])
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
                distance_agent_1 = abs(path[0][0] - agent1[1])
                distance_agent_2 = abs(path[1][0] - agent2[1])
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
                distance_agent_1 = abs(path[0][0] - agent1[1])
                for i in range(1, len(path[0])):
                    distance_agent_1 += abs(path[0][i] - path[0][i - 1])
                    distance_agent_2 = abs(path[1][0] - agent2[1])
                    for j in range(1, len(path[1])):
                        distance_agent_2 += abs(path[1][j] - path[1][j - 1])
                    if (distance_agent_1 + distance_agent_2) < minimum_total_distance:
                        minimum_total_distance = distance_agent_1 + distance_agent_2
                        minimum_distance_agent_1 = distance_agent_1
                        minimum_path_agent_1 = path[0]
                        minimum_distance_agent_2 = distance_agent_2
                        minimum_path_agent_2 = path[1]
                        best_possible_path = path
        #                 print(agent1_pos_x, " ", agent2_pos_x , " ", path, "  ", distance_agent_1, "  ", distance_agent_2)
        #
        # print("a " , agent1_pos_x, " ", agent2_pos_x, " ", best_possible_path, "  ", distance_agent_1, "  ", distance_agent_2)

        return [minimum_total_distance, best_possible_path]

    def check_boxes_changes(self):
        if len(self.world.box_group) != len(self.box_group):
            return True
        else:
            return False

    def minimum_behaviours(self):  # aqui o algoritmo determina qual é o melhor score possivel tendo em conta colaboração e execução total para depois ser comparado com os resultados de cada agente
        a = open("twoDBoxes_CollaborationResults.txt", "r+")
        line1 = a.readline()
        line2 = a.readline()
        if "C" not in line1 or "NC" not in line2:
            n = 5
            f = open(self.world.terrain_file, "r")
            filenameAA = open("filenameAA.txt", "w+")
            filenameBB = open("filenameBB.txt", "w+")
            lines = f.readlines()
            for line in lines:
                for letter in line:
                    if letter == "B":
                        filenameAA.write("A")
                        filenameBB.write("B")
                    elif letter == "A":
                        filenameAA.write("A")
                        filenameBB.write("B")
                    else:
                        filenameAA.write(letter)
                        filenameBB.write(letter)
            f.close()
            filenameAA.close()
            filenameBB.close()

            for i in range(n):
                scoresAA = self.run_simulation("filenameAA.txt")
                self.avg_non_collaborative_total_score += scoresAA[0] + scoresAA[1]

            for i in range(n):
                scoresBB = self.run_simulation("filenameBB.txt")
                self.avg_collaborative_total_score += scoresBB[0] + scoresBB[1]

            os.remove("filenameAA.txt")
            os.remove("filenameBB.txt")

            self.avg_collaborative_total_score = self.avg_collaborative_total_score / n
            self.avg_non_collaborative_total_score = self.avg_non_collaborative_total_score / n

            a.write("C %d\r" % self.avg_collaborative_total_score)
            a.write("NC %d\r\n" % self.avg_non_collaborative_total_score)
            a.close()

        else:
            self.avg_collaborative_total_score = int(line1.replace("C ", ""))
            self.avg_non_collaborative_total_score = int(line2.replace("NC ", ""))
            a.close()
        self.write = True

    def run_simulation(self, filename):

        # define a variable to control the main loop
        running = True
        # initialize the pygame module
        pygame.init()

        # load and set the logo
        pygame.display.set_caption("oneDBoxes")

        # game window centered on start
        os.environ['SDL_VIDEO_CENTERED'] = '0'

        update_time = 0.1

        # create world
        world_temp = World_Boxes(filename)
        # create the collaboration analyser
        collaborator = Collaborator_Boxes(world_temp, True)
        world_temp.render()

        world_temp.show_automatic = True
        for shappy in world_temp.shappy_group:
            # if shappy.type == "Coolaborative":
            shappy.auto = not shappy.auto
            shappy.calculate = True

        # main loop
        while running:
            world_temp.update()
            world_temp.render()
            if len(world_temp.box_group) == 0 and not self.write:
                running = False
                return (collaborator.agent1_points, collaborator.agent2_points)
            collaborator.update()