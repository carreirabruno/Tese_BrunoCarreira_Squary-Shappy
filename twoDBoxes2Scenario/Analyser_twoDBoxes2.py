import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pickle
import copy


class Analyser_twoDBoxes2(object):
    # def __init__(self, terrain_matrix, run_states, scenario_policies):
    #     self.terrain_matrix = terrain_matrix
    #     self.run_states = run_states
    #     self.scenario_policies = scenario_policies
    #
    #     # # Maximize Social Utility
    #     self.count_number_of_steps()
    #
    #     # # Count collisions
    #     self.count_boxes_caught()
    #
    #     # # Count collisions
    #     self.count_collisions()
    #
    #     # # Count communications
    #     self.count_communications()
    #
    #     # # Split Attention
    #     self.create_heatmaps()
    #
    # def count_number_of_steps(self):
    #     shappy3_steps = 0
    #     shappy4_steps = 0
    #     print(self.run_states[0])
    #     for i in range(1, len(self.run_states)):
    #         if not self.compare_arrays(self.run_states[i][0], self.run_states[i-1][0]):
    #             shappy3_steps += 1
    #         if not self.compare_arrays(self.run_states[i][1], self.run_states[i-1][1]):
    #             shappy4_steps += 1
    #         print(self.run_states[i])
    #
    #     print("Steps made by shappy 3 -> ", shappy3_steps)
    #     print("Steps made by shappy 4 -> ", shappy4_steps)
    #     print("Total steps made -> ", shappy3_steps + shappy4_steps)
    #
    # def compare_arrays(self, array1, array2):
    #     if len(array1) != len(array2):
    #         return False
    #     else:
    #         for i in range(len(array1)):
    #             if array1[i] != array2[i]:
    #                 return False
    #     return True
    #
    # def get_policy(self, policy_file, centralized):
    #     fp = open(policy_file, "rb")  # Unpickling
    #     if centralized:
    #         policy = pickle.load(fp)
    #     else:
    #         policy1, policy2 = pickle.load(fp)
    #     fp.close()
    #     if centralized:
    #         return policy
    #     else:
    #         return policy1, policy2
    #
    # def count_communications(self):
    #     shappy3_communication = 0
    #     shappy4_communication = 0
    #     policy3, policy4 = self.get_policy(self.scenario_policies[3], False)
    #     for state in self.run_states:
    #         state3 = copy.deepcopy(state)
    #         state4 = copy.deepcopy(state)
    #         if shappy3_communication == 0:
    #             state3[1] = [-1, -1]
    #         if shappy4_communication == 0:
    #             state4[0] = [-1, -1]
    #         for policy in policy3:
    #             if self.compare_arrays(state3, policy[0]) and np.argmax(policy[1]) == 5:
    #                 shappy3_communication += 1
    #                 break
    #         for policy in policy4:
    #             if self.compare_arrays(state4, policy[0]) and np.argmax(policy[1]) == 5:
    #                 shappy4_communication += 1
    #                 break
    #     print("Blue listened: ", shappy3_communication)
    #     print("Red listened: ", shappy4_communication)
    #
    # def count_collisions(self):
    #     collisions = 0
    #     for state in self.run_states:
    #         if self.compare_arrays(state[0], state[1]):
    #             collisions += 1
    #
    #     print("Collisions: ", collisions)
    #
    # def count_boxes_caught(self):
    #     shappy3_boxes = 0
    #     shappy4_boxes = 0
    #     for i in range(1, len(self.run_states)):
    #         for j in range(2, len(self.run_states[i-1])):
    #             if self.compare_arrays(self.run_states[i][0], self.run_states[i-1][j]):
    #                 shappy3_boxes += 1
    #             if self.compare_arrays(self.run_states[i][1], self.run_states[i-1][j]):
    #                 shappy4_boxes += 1
    #
    #     print("Boxes caught by shappy 3 -> ", shappy3_boxes)
    #     print("Boxes caught by shappy 4 -> ", shappy4_boxes)

    def __init__(self, ):

        self.run_states = []

        self.shappys_movement = []

        self.shappys_movement_centralized = []
        self.shappys_movement_individual = []

    def write_shappys_movement(self, run_states, filename):
        self.run_states = run_states

        self.get_shappys_movement()

        for a in self.shappys_movement:
            print(a[0], " ", a[1])

        self.write_in_txt(filename)

    def read_shappys_movement(self, filename_centralized, filename_individual):
        self.read_from_txt(filename_centralized, filename_individual)
        self.analyse_shappys_movement()

    def get_shappys_movement(self):
        for i in range(1, len(self.run_states)):
            if self.compare_arrays(self.run_states[i][0], self.run_states[i-1][0]):
                self.shappys_movement.append(["Shappy3", "Stay"])
            elif self.run_states[i][0][0] > self.run_states[i-1][0][0]:
                self.shappys_movement.append(["Shappy3", "Down"])
            elif self.run_states[i][0][0] < self.run_states[i - 1][0][0]:
                self.shappys_movement.append(["Shappy3", "Up"])
            elif self.run_states[i][0][1] > self.run_states[i - 1][0][1]:
                self.shappys_movement.append(["Shappy3", "Right"])
            elif self.run_states[i][0][1] < self.run_states[i - 1][0][1]:
                self.shappys_movement.append(["Shappy3", "Left"])

            if self.compare_arrays(self.run_states[i][1], self.run_states[i-1][1]):
                self.shappys_movement.append(["Shappy4", "Stay"])
            elif self.run_states[i][1][0] > self.run_states[i-1][1][0]:
                self.shappys_movement.append(["Shappy4", "Down"])
            elif self.run_states[i][1][0] < self.run_states[i - 1][1][0]:
                self.shappys_movement.append(["Shappy4", "Up"])
            elif self.run_states[i][1][1] > self.run_states[i - 1][1][1]:
                self.shappys_movement.append(["Shappy4", "Right"])
            elif self.run_states[i][1][1] < self.run_states[i - 1][1][1]:
                self.shappys_movement.append(["Shappy4", "Left"])

    def analyse_shappys_movement(self):
        longerList = []
        shorterList = []

        _similarityValue = 0

        if len(self.shappys_movement_centralized) >= len(self.shappys_movement_individual):
            longerList = self.shappys_movement_centralized
            shorterList = self.shappys_movement_individual
        else:
            longerList = self.shappys_movement_individual
            shorterList = self.shappys_movement_centralized

        for i in range(len(shorterList)):
            if self.compare_arrays(longerList[i], shorterList[i]):
                _similarityValue += 1

        _similarityValue = _similarityValue / len(longerList)

        print("SIMILARITY VALUE = ", _similarityValue)

    def compare_arrays(self, array1, array2):
        if len(array1) != len(array2):
            return False
        else:
            for i in range(len(array1)):
                if array1[i] != array2[i]:
                    return False
        return True

    def write_in_txt(self, filename):
        with open(filename, "wb") as fp:  # Unpickling
            pickle.dump(self.shappys_movement, fp)
            fp.close()

    def read_from_txt(self, filename_centralized, filename_individual):
        cen = open(filename_centralized, 'rb')
        self.shappys_movement_centralized = pickle.load(cen)
        cen.close()

        ind = open(filename_individual, 'rb')
        self.shappys_movement_individual = pickle.load(ind)
        ind.close()
