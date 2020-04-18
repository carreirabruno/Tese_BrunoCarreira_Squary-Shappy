import pickle
import numpy as np
import copy

class Comparator_oneDBoxes2(object):

    def __init__(self, terrain_matrix, map_policies):
        for line in terrain_matrix:
            if 3 in line:
                self.map = line

        self.map_policies = map_policies

        # #Combined Actions
        # self.STAY_LEFT = 0
        # self.STAY_RIGHT = 1
        # self.LEFT_STAY = 2
        # self.LEFT_LEFT = 3
        # self.LEFT_RIGHT = 4
        # self.RIGHT_STAY = 5
        # self.RIGHT_LEFT = 6
        # self.RIGHT_RIGHT = 7

        # #Individual Actions
        # self.STAY = 0
        # self.LEFT = 1
        # self.RIGHT = 2

        # for line in self.map_policies:
        #     print(line)
        # print()

        self.global_matrices = []
        self.get_global_matrices_policies()

        self.compare_global_policies_matrices()
        # self.compare_optimal_policies_matrices()

    def get_global_matrices_policies(self):
        global_matrix = []
        for policy_file in self.map_policies:
            equal_moves = 0
            filename = policy_file.replace("oneDBoxes2_MDP_", "")
            policy_type = filename.replace("_policy_map1.pickle", "")
            policy_type = policy_type.replace("_policy_map2.pickle", "")
            policy_type = policy_type.replace("_policy_map3.pickle", "")

            if policy_type == "individual_decentralized_split_rewards" or policy_type == "individual_decentralized_joint_rewards":
                policy_type = "individual_decentralized"
            elif policy_type == "peer_aware_decentralized_split_rewards" or policy_type == "peer_aware_decentralized_joint_rewards":
                policy_type = "peer_aware_decentralized"
            elif policy_type == "peer_communication_decentralized_split_rewards" or policy_type == "peer_communication_decentralized_joint_rewards":
                policy_type = "peer_communication_decentralized"

            if policy_type == "centralized":
                fp = open(policy_file, "rb")  # Unpickling
                policy = pickle.load(fp)
                fp.close()

                matrix = []
                for item in policy:
                    matrix.append([item[0], np.argmax(item[1])])

            else:
                fp = open(policy_file, "rb")  # Unpickling
                policy3, policy4 = pickle.load(fp)
                fp.close()

                matrix = []

                if policy_type == "individual_decentralized":
                    matrix = self.create_individual_matrices(policy3, policy4)

                elif policy_type == "peer_aware_decentralized":
                    matrix = self.create_peer_aware_matrices(policy3, policy4)

                elif policy_type == "peer_communication_decentralized":
                    matrix = self.create_peer_communication_matrices(policy3, policy4)


            self.global_matrices.append(matrix)

    def compare_matrices_items(self, matrix1, matrix2):
        score = 0
        if len(matrix1) > len(matrix2):
            temp = copy.copy(matrix1)
            matrix1 = copy.copy(matrix2)
            matrix2 = copy.copy(temp)

        for item1 in matrix1:
            for item2 in matrix2:
                if item1[0] == item2[0] and item1[1] == item2[1]:
                    score += 1
                    break
        # for i in range(len(matrix1)):
        #     if matrix1[i][0] == matrix2[i][0] and matrix1[i][1] == matrix2[i][1]:
        #         score += 1

        if len(matrix1) != 0:
            score_percentage = (score * 100) / len(matrix1)
        else:
            score_percentage = 0
        return score_percentage

    def create_individual_matrices(self, policy3, policy4):
        matrix = []
        for item3 in policy3:
            temp_item3 = copy.deepcopy(item3[0])
            temp_item3.remove(temp_item3[0])
            # if len(temp_item3) > 4:
            #     temp_item3.remove(temp_item3[0])
            #     temp_item3.remove(temp_item3[1])
            #     print(temp_item3)
            for item4 in policy4:
                temp_item4 = copy.deepcopy(item4[0])
                temp_item4.remove(temp_item4[0])
                # if len(temp_item4) > 4:
                #     temp_item4.remove(temp_item4[0])
                #     print(temp_item4)
                if self.compare_arrays(temp_item3, temp_item4):
                # if temp_item3[0] == temp_item4[0]:
                    action3 = np.argmax(item3[1])
                    action4 = np.argmax(item4[1])
                    action = 0
                    if action3 == 0 and action4 == 1:
                        action = 0
                    elif action3 == 0 and action4 == 2:
                        action = 1
                    elif action3 == 1 and action4 == 0:
                        action = 2
                    elif action3 == 1 and action4 == 1:
                        action = 3
                    elif action3 == 1 and action4 == 2:
                        action = 4
                    elif action3 == 2 and action4 == 0:
                        action = 5
                    elif action3 == 2 and action4 == 1:
                        action = 6
                    elif action3 == 2 and action4 == 2:
                        action = 7

                    temp_state = [item3[0][0]]
                    for item in item4[0]:
                        temp_state.append(item)
                    matrix.append([temp_state, action])

        return matrix

    def create_peer_aware_matrices(self, policy3, policy4):
        matrix = []
        for item3 in policy3:
            for item4 in policy4:
                if item3[0] == item4[0]:
                    action3 = np.argmax(item3[1])
                    action4 = np.argmax(item4[1])
                    action = 0
                    if action3 == 0 and action4 == 1:
                        action = 0
                    elif action3 == 0 and action4 == 2:
                        action = 1
                    elif action3 == 1 and action4 == 0:
                        action = 2
                    elif action3 == 1 and action4 == 1:
                        action = 3
                    elif action3 == 1 and action4 == 2:
                        action = 4
                    elif action3 == 2 and action4 == 0:
                        action = 5
                    elif action3 == 2 and action4 == 1:
                        action = 6
                    elif action3 == 2 and action4 == 2:
                        action = 7

                    matrix.append([item3[0], action])

        return matrix

    def create_peer_communication_matrices(self, policy3, policy4):
        matrix = []
        for item3 in policy3:
            temp_item3 = copy.deepcopy(item3[0])
            for item4 in policy4:
                temp_item4 = copy.deepcopy(item4[0])
                if -1 not in temp_item3 and -1 not in temp_item4:
                    if self.compare_arrays(temp_item3, temp_item4):
                        action3 = np.argmax(item3[1])
                        action4 = np.argmax(item4[1])
                        action = 0
                        if action3 == 0 and action4 == 1:
                            action = 0
                        elif action3 == 0 and action4 == 2:
                            action = 1
                        elif action3 == 1 and action4 == 0:
                            action = 2
                        elif action3 == 1 and action4 == 1:
                            action = 3
                        elif action3 == 1 and action4 == 2:
                            action = 4
                        elif action3 == 2 and action4 == 0:
                            action = 5
                        elif action3 == 2 and action4 == 1:
                            action = 6
                        elif action3 == 2 and action4 == 2:
                            action = 7

                        matrix.append([item3[0], action])

                else:
                    temp_item3 = copy.deepcopy(item3[0])
                    temp_item3.remove(temp_item3[0])
                    temp_item3.remove(temp_item3[0])
                    temp_item4.remove(temp_item4[0])
                    temp_item4.remove(temp_item4[0])
                    if self.compare_arrays(temp_item3, temp_item4):
                        action3 = np.argmax(item3[1])
                        action4 = np.argmax(item4[1])
                        action = 0
                        if (action3 == 0 or action3 == 3) and action4 == 1:
                            action = 0
                        elif (action3 == 0 or action3 == 3) and action4 == 2:
                            action = 1
                        elif action3 == 1 and (action4 == 0 or action4 == 3):
                            action = 2
                        elif action3 == 1 and action4 == 1:
                            action = 3
                        elif action3 == 1 and action4 == 2:
                            action = 4
                        elif action3 == 2 and (action4 == 0 or action4 == 3):
                            action = 5
                        elif action3 == 2 and action4 == 1:
                            action = 6
                        elif action3 == 2 and action4 == 2:
                            action = 7

                        temp_state = item4[0]
                        temp_state[0] = item3[0][0]

                        # temp_state = [item3[0][0]]
                        # for item in item4[0]:
                        #     temp_state.append(item)
                        equal = False
                        for state in matrix:
                            if self.compare_arrays(state[0], temp_state):
                                equal = True
                        if not equal:
                            matrix.append([temp_state, action])
        return matrix

    def compare_arrays(self, array1, array2):
        if len(array1) != len(array2):
            return False
        else:
            for i in range(len(array1)):
                if array1[i] != array2[i]:
                    return False
        return True

    def compare_global_policies_matrices(self):
        for i in range(len(self.global_matrices)):
            # print(self.map_policies[i])
            # for item in self.global_matrices[i]:
            #     print(item)
            for j in range(len(self.global_matrices)):
                score = self.compare_matrices_items(self.global_matrices[i], self.global_matrices[j])
                print(score, "  ", self.map_policies[i], self.map_policies[j])
            print()

    def compare_optimal_policies_matrices(self):
        for policy in self.global_matrices:
            state = policy[0][0]
            print(state)

