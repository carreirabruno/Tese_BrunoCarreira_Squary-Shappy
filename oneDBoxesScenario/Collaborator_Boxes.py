import pygame
import math
from itertools import *
import datetime
import os
import time
from oneDBoxesScenario.World_Boxes import *


class Collaborator_Boxes(object):

    def __init__(self, world, simulation):
        self.world = world

        self.agent1_old_distance = math.inf
        self.agent2_old_distance = math.inf

        self.agent1_points = 0
        self.agent2_points = 0
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

        self.best_behaviour = self.get_best_collaboration_behaviour()

        if not simulation:
            self.max_best_behaviour()

        self.agent1_old_distance = abs(self.best_behaviour[0][1][0] - self.best_behaviour[0][0])
        self.agent2_old_distance = abs(self.best_behaviour[1][1][0] - self.best_behaviour[1][0])

    def update(self):
        if len(self.world.box_group) == 0 and self.write:
            self.write_in_txt()
            quit()
        else:
            changed = self.check_boxes_changes()
            if changed:
                self.best_behaviour = self.get_best_collaboration_behaviour()
                self.agent1_old_distance = math.inf
                self.agent2_old_distance = math.inf

            self.analyse_behaviour(self.best_behaviour)

    def write_in_txt(self):
        f = open("oneDBoxes_CollaborationResults.txt", "a+")
        agent_list = []
        for agent in self.world.shappy_group:
            agent_list.append(agent.type)

        datetime_object = datetime.datetime.now()
        datetime_object = datetime_object.strftime("DATE_%d-%m-%Y___TIME_%H-%M-%S")
        f.write("%s \n" % datetime_object)
        f.write(("AGENT1 -> %s - %d\r") % (agent_list[0], self.agent1_points))
        f.write(("AGENT2 -> %s - %d\r") % (agent_list[1], self.agent2_points))
        f.write("TOTAL -> %d\r" % (self.agent1_points + self.agent2_points))
        f.write("AVG_NON_COLLABORATIVE_SCORE -> %d\r" % self.avg_non_collaborative_total_score)
        f.write("AVG_COLLABORATIVE_SCORE -> %d\r" % self.avg_collaborative_total_score)

        if abs((self.agent1_points + self.agent2_points) - self.avg_non_collaborative_total_score) < abs((self.agent1_points + self.agent2_points) - self.avg_collaborative_total_score):
            f.write("NON COLLABORATIVE BEHAVIOUR\r\n")
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
            agent_list.append(agent.x_pos)

        if len(self.box_group) == 0:
            print("NO MORE BOXES")
        elif len(self.box_group) == 1:
            if abs(self.box_group[0] - agent_list[0]) < abs(self.box_group[0] - agent_list[1]):
                best_collaborative_behaviour = [[agent_list[0], self.box_group], [agent_list[1], math.inf]]
            else:
                best_collaborative_behaviour = [[agent_list[0], math.inf], [agent_list[1], self.box_group]]
        else:
            best_possible_path_1 = self.calculate_best_possible_paths(agent_list[0], agent_list[1], self.box_group)
            best_possible_path_2 = self.calculate_best_possible_paths(agent_list[1], agent_list[0], self.box_group)


            # CRIA-SE AQUI A COMBINAÇÃO AGENTE-BOX PARA ANALISAR OS MOVIMENTOS
            if best_possible_path_1[0] <= best_possible_path_2[0]:
                best_collaborative_behaviour = [[agent_list[0], best_possible_path_1[1][0]],
                                                [agent_list[1], best_possible_path_1[1][1]]]
            else:
                best_collaborative_behaviour = [[agent_list[0], best_possible_path_1[1][1]],
                                                [agent_list[1], best_possible_path_1[1][0]]]

        return best_collaborative_behaviour

    def analyse_behaviour(self, behaviour_array):
        if self.agent1_old_distance == math.inf and self.agent2_old_distance == math.inf:
            if behaviour_array[0][1] != math.inf:
                self.agent1_old_distance = abs(behaviour_array[0][1][0] - behaviour_array[0][0])
            else:
                self.agent1_old_distance = behaviour_array[0][0]
            if behaviour_array[1][1] != math.inf:
                self.agent2_old_distance = abs(behaviour_array[1][1][0] - behaviour_array[1][0])
            else:
                self.agent2_old_distance = behaviour_array[1][0]
        else:
            agent_list = []
            for agent in self.world.shappy_group:
                agent_list.append(agent.x_pos)
            if behaviour_array[0][1] != math.inf and abs(
                    behaviour_array[0][1][0] - agent_list[0]) == self.agent1_old_distance:
                self.freeze_counter1 += 1
                if self.freeze_counter1 == 500:
                    self.agent1_points -= 3
                    self.freeze_counter1 = 0
            elif behaviour_array[0][1] != math.inf and abs(
                    behaviour_array[0][1][0] - agent_list[0]) < self.agent1_old_distance:   #está a aproximar-se do objetivo
                self.agent1_old_distance = abs(behaviour_array[0][1][0] - agent_list[0])
                self.agent1_points += 3
            elif behaviour_array[0][1] != math.inf and abs(behaviour_array[0][1][0] - agent_list[
                0]) > self.agent1_old_distance:     #está a afastar-se do objetivo
                # self.agent1_old_distance = abs(behaviour_array[0][1][0] - agent_list[0])
                self.agent1_points -= 9
            elif behaviour_array[0][1] == math.inf and abs(self.agent1_old_distance - agent_list[0]) < 10:  #não tem objetivo e está quieto
                self.agent1_points += 1
            elif behaviour_array[0][1] == math.inf and abs(self.agent1_old_distance - agent_list[0]) > 10:  #não tem objetivo e está a mover-se (desperdicio de ações e pode estar a ser greedy)
                self.agent1_points -= 1

            if behaviour_array[1][1] != math.inf and abs(
                    behaviour_array[1][1][0] - agent_list[1]) == self.agent2_old_distance:
                self.freeze_counter2 += 1
                if self.freeze_counter2 == 500:
                    self.agent2_points -= 3
                    self.freeze_counter2 = 0
            elif behaviour_array[1][1] != math.inf and abs(
                    behaviour_array[1][1][0] - agent_list[1]) < self.agent2_old_distance:
                self.agent2_old_distance = abs(behaviour_array[1][1][0] - agent_list[1])
                self.agent2_points += 3
            elif behaviour_array[1][1] != math.inf and abs(
                    behaviour_array[1][1][0] - agent_list[1]) > self.agent2_old_distance:
                # self.agent2_old_distance = abs(behaviour_array[1][1][0] - agent_list[1])
                self.agent2_points -= 9
            elif behaviour_array[1][1] == math.inf and abs(self.agent2_old_distance - agent_list[1]) < 10:
                self.agent2_points += 1
            elif behaviour_array[1][1] == math.inf and abs(self.agent2_old_distance - agent_list[1]) > 10:
                self.agent2_points -= 1

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
    def calculate_best_possible_paths(self, agent1_pos_x, agent2_pos_x, boxes_group):
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
        #                 print(agent1_pos_x, " ", agent2_pos_x , " ", path, "  ", distance_agent_1, "  ", distance_agent_2)
        #
        # print("a " , agent1_pos_x, " ", agent2_pos_x, " ", best_possible_path, "  ", distance_agent_1, "  ", distance_agent_2)

        return [minimum_total_distance, best_possible_path]

    def check_boxes_changes(self):
        if len(self.world.box_group) != len(self.box_group):
            return True
        else:
            return False

    def max_best_behaviour(self):  # aqui o algoritmo determina qual é o melhor score possivel tendo em conta colaboração e execução total para depois ser comparado com os resultados de cada agente
        n = 5
        #substituir os A por B e depois o contrário

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