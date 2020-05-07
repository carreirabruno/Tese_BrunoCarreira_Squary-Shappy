import pickle
import numpy as np
import copy


class Comparator_oneDBoxes2(object):

    def __init__(self, terrain_matrix, map_policies):
        for line in terrain_matrix:
            if 3 in line:
                self.map = line

        self.start_state = []
        for i in range(len(self.map)):
            if self.map[i] == 3:
                self.start_state.append(i)
            if self.map[i] == 4:
                self.start_state.append(i)
        for i in range(len(self.map)):
            if self.map[i] == 2:
                self.start_state.append(i)

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
        # self.get_global_matrices_policies()
        # self.compare_global_policies_matrices()

        self.optimal_matrices_states = []
        self.optimal_matrices_actions = []
        self.get_optimal_matrices_policies()
        self.compare_optimal_policies_matrices()

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
                    matrix = self.create_global_individual_matrices(policy3, policy4)

                elif policy_type == "peer_aware_decentralized":
                    matrix = self.create_global_peer_aware_matrices(policy3, policy4)

                elif policy_type == "peer_communication_decentralized":
                    matrix = self.create_global_peer_communication_matrices(policy3, policy4)

            self.global_matrices.append(matrix)

    def compare_global_policies_matrices(self):
        for i in range(len(self.global_matrices)):
            # print(self.map_policies[i])
            # for item in self.global_matrices[i]:
            #     print(item)
            for j in range(len(self.global_matrices)):
                score = self.compare_matrices_items(self.global_matrices[i], self.global_matrices[j])
                print(score, "  ", self.map_policies[i], self.map_policies[j])
            print()

    def compare_matrices_items(self, matrix1, matrix2):
        score = 0
        if len(matrix1) < len(matrix2):
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

    def compare_matrices_items_in_order(self, matrix1, matrix2):
        score = 0
        if len(matrix1) < len(matrix2):
            temp = copy.copy(matrix1)
            matrix1 = copy.copy(matrix2)
            matrix2 = copy.copy(temp)

        for i in range(len(matrix1)):
            if i < len(matrix2):
                if self.compare_arrays(matrix1[i], matrix2[i]):
                    score += 1
        # for item1 in matrix1:
        #     for item2 in matrix2:
        #         if self.compare_arrays(item1, item2):
        #             score += 1
        #         break
        # for i in range(len(matrix1)):
        #     if matrix1[i][0] == matrix2[i][0] and matrix1[i][1] == matrix2[i][1]:
        #         score += 1

        if len(matrix1) != 0:
            score_percentage = (score * 100) / len(matrix1)
        else:
            score_percentage = 0
        return score_percentage

    def create_global_individual_matrices(self, policy3, policy4):
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

    def create_global_peer_aware_matrices(self, policy3, policy4):
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

    def create_global_peer_communication_matrices(self, policy3, policy4):
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

                        equal = False
                        for state in matrix:
                            if self.compare_arrays(state[0], temp_item3):
                                equal = True
                        if not equal:
                            matrix.append([temp_item3, action])

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

        for line in matrix:
            print(line)
        print()

        return matrix

    def compare_arrays(self, array1, array2):
        if len(array1) != len(array2):
            return False
        else:
            for i in range(len(array1)):
                if array1[i] != array2[i]:
                    return False
        return True

    def get_optimal_matrices_policies(self):
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
            elif policy_type == "peer_listen_decentralized_split_rewards" or policy_type == "peer_listen_decentralized_joint_rewards":
                policy_type = "peer_listen_decentralized"
            elif policy_type == "peer_communication_decentralized_split_rewards" or policy_type == "peer_communication_decentralized_joint_rewards":
                policy_type = "peer_communication_decentralized"


            state_array = [self.start_state]
            if policy_type == "centralized":
                fp = open(policy_file, "rb")  # Unpickling
                policy = pickle.load(fp)
                fp.close()

                current_state = self.start_state
                matrix = []
                while len(current_state) > 2:
                    old_state = copy.copy(current_state)
                    for item in policy:
                        # old_state = copy.copy(current_state)
                        if self.compare_arrays(item[0], current_state):
                            action = np.argmax(item[1])
                            action3 = -1
                            action4 = -1
                            if action == 0:
                                action3 = 0
                                action4 = 1
                            elif action == 1:
                                action3 = 0
                                action4 = 2
                            elif action == 2:
                                action3 = 1
                                action4 = 0
                            elif action == 3:
                                action3 = 1
                                action4 = 1
                            elif action == 4:
                                action3 = 1
                                action4 = 2
                            elif action == 5:
                                action3 = 2
                                action4 = 0
                            elif action == 6:
                                action3 = 2
                                action4 = 1
                            elif action == 7:
                                action3 = 2
                                action4 = 2
                            new_state = self.update_state(current_state, action3, action4, False)

                            if old_state[0] == 1 and action3 == 1:
                               action3 = 0
                            elif old_state[0] == 8 and action3 == 2:
                               action3 = 0
                            if old_state[1] == 1 and action4 == 1:
                               action4 = 0
                            elif old_state[1] == 8 and action4 == 2:
                               action4 = 0

                            matrix.append([action3, action4])

                            current_state = new_state

                            state_array.append(current_state)

                            break

            else:
                fp = open(policy_file, "rb")  # Unpickling
                policy3, policy4 = pickle.load(fp)
                fp.close()

                matrix = []

                if policy_type == "individual_decentralized":
                    current_state3 = self.start_state
                    current_state4 = self.start_state
                    current_state = self.start_state
                    # for item in current_state4:
                    #     current_state.append(item)
                    matrix = []

                    while len(current_state) > 2:
                        old_state = copy.copy(current_state)
                        current_state3 = copy.copy(current_state)
                        current_state3.remove(current_state3[1])
                        current_state4 = copy.copy(current_state)
                        current_state4.remove(current_state4[0])
                        action3 = -1
                        for item in policy3:
                            if self.compare_arrays(item[0], current_state3):
                                action3 = np.argmax(item[1])
                        for item in policy4:
                            if self.compare_arrays(item[0], current_state4):
                                action4 = np.argmax(item[1])
                                new_state = self.update_state(current_state, action3, action4, False)

                                if old_state[0] == 1 and action3 == 1:
                                    action3 = 0
                                elif old_state[0] == 8 and action3 == 2:
                                    action3 = 0
                                if old_state[1] == 1 and action4 == 1:
                                    action4 = 0
                                elif old_state[1] == 8 and action4 == 2:
                                    action4 = 0
                                current_state = new_state
                                state_array.append(current_state)
                                matrix.append([action3, action4])
                                break

                elif policy_type == "peer_aware_decentralized":
                    # current_state = policy3[0][0]
                    current_state = self.start_state
                    matrix = []
                    while len(current_state) > 2:
                        old_state = copy.copy(current_state)
                        action3 = -1
                        for item in policy3:
                            if self.compare_arrays(item[0], current_state):
                                action3 = np.argmax(item[1])
                        for item in policy4:
                            if self.compare_arrays(item[0], current_state):
                                action4 = np.argmax(item[1])
                                new_state = self.update_state(current_state, action3, action4, False)

                                if old_state[0] == 1 and action3 == 1:
                                    action3 = 0
                                elif old_state[0] == 8 and action3 == 2:
                                    action3 = 0
                                if old_state[1] == 1 and action4 == 1:
                                    action4 = 0
                                elif old_state[1] == 8 and action4 == 2:
                                    action4 = 0
                                current_state = new_state
                                state_array.append(current_state)
                                matrix.append([action3, action4])
                                break

                elif policy_type == "peer_listen_decentralized":
                    # current_state3 = copy.copy(policy3[0][0])
                    # current_state4 = copy.copy(policy4[0][0])
                    # current_state = copy.copy(current_state3)
                    # current_state[1] = current_state4[1]

                    current_state3 = self.start_state
                    current_state4 = self.start_state
                    current_state = self.start_state

                    matrix = []
                    self.shappy3_knows = False
                    self.shappy4_knows = False
                    while len(current_state) > 2:
                        old_state = copy.copy(current_state)
                        current_state3 = copy.copy(current_state)
                        if not self.shappy3_knows:
                            current_state3[1] = -1

                        current_state4 = copy.copy(current_state)
                        if not self.shappy4_knows:
                            current_state4[0] = -1

                        action3 = -1
                        for item in policy3:
                            if self.compare_arrays(item[0], current_state3):
                                action3 = np.argmax(item[1])
                        for item in policy4:
                            if self.compare_arrays(item[0], current_state4):
                                action4 = np.argmax(item[1])
                                new_state = self.update_state(current_state, action3, action4, True)

                                if old_state[0] == 1 and action3 == 1:
                                    action3 = 0
                                elif old_state[0] == 8 and action3 == 2:
                                    action3 = 0
                                if old_state[1] == 1 and action4 == 1:
                                    action4 = 0
                                elif old_state[1] == 8 and action4 == 2:
                                    action4 = 0
                                if action3 == 3:
                                    action3 = 0
                                if action4 == 3:
                                    action4 = 0
                                current_state = new_state
                                state_array.append(current_state)
                                matrix.append([action3, action4])
                                break

                elif policy_type == "peer_communication_decentralized":
                    current_state3 = copy.copy(policy3[0][0])
                    current_state4 = copy.copy(policy4[0][0])
                    current_state = copy.copy(current_state3)
                    current_state[1] = current_state4[1]

                    matrix = []
                    self.shappy3_knows = False
                    self.shappy4_knows = False
                    while len(current_state) > 2:
                        old_state = copy.copy(current_state)
                        current_state3 = copy.copy(current_state)
                        if not self.shappy3_knows:
                            current_state3[1] = -1

                        current_state4 = copy.copy(current_state)
                        if not self.shappy4_knows:
                            current_state4[0] = -1

                        action3 = -1
                        for item in policy3:
                            if self.compare_arrays(item[0], current_state3):
                                action3 = np.argmax(item[1])
                        for item in policy4:
                            if self.compare_arrays(item[0], current_state4):
                                action4 = np.argmax(item[1])
                                new_state = self.update_state(current_state, action3, action4, True)

                                if old_state[0] == 1 and action3 == 1:
                                    action3 = 0
                                elif old_state[0] == 8 and action3 == 2:
                                    action3 = 0
                                if old_state[1] == 1 and action4 == 1:
                                    action4 = 0
                                elif old_state[1] == 8 and action4 == 2:
                                    action4 = 0
                                if action3 == 3:
                                    action3 = 0
                                if action4 == 3:
                                    action4 = 0
                                current_state = new_state
                                matrix.append([action3, action4])
                                break

            self.optimal_matrices_actions.append(matrix)
            self.optimal_matrices_states.append(state_array)

    def compare_optimal_policies_matrices2(self):
        for i in range(len(self.optimal_matrices)):
            for j in range(len(self.optimal_matrices)):
                score = self.compare_matrices_items(self.optimal_matrices[i], self.optimal_matrices[j])
                print(score, "  ", self.map_policies[i], self.map_policies[j])
            print()

    def compare_optimal_policies_matrices(self):
        # for line in self.optimal_matrices_states:
        #     print(line)
        # print()
        # for line in self.optimal_matrices_actions:
        #     print(line)
        # quit()

        for i in range(len(self.optimal_matrices_actions)):
            # for line in self.optimal_matrices[i]:
            print(self.map_policies[i])
            for j in range(len(self.optimal_matrices_actions)):
                score = self.compare_individual_actions(self.optimal_matrices_actions[i], self.optimal_matrices_actions[j])
                # score = self.compare_matrices_items_in_order(self.optimal_matrices_actions[i], self.optimal_matrices_actions[j])
                print(score, "  ", self.map_policies[i], self.map_policies[j])
            print()

    def update_state(self, current_state, action3, action4, communication):
        if communication:
            if action3 == 4:
                self.shappy3_knows = True
                action3 = 0
            if action4 == 4:
                self.shappy4_knows = True
                action4 = 0

        new_state = copy.copy(current_state)
        if action3 == 0:
            pass
        elif action3 == 1 and new_state[0] > 1:
            new_state[0] = new_state[0] - 1
        elif action3 == 2 and new_state[0] < 8:
            new_state[0] = new_state[0] + 1

        if action4 == 0:
            pass
        elif action4 == 1 and new_state[1] > 1:
            new_state[1] = new_state[1] - 1
        elif action4 == 2 and new_state[1] < 8:
            new_state[1] = new_state[1] + 1
        for i in range(2, len(new_state)):
            if new_state[0] == new_state[i]:
                temp_i = copy.copy(new_state[0])
                new_state.reverse()
                new_state.remove(temp_i)
                new_state.reverse()
                break

        for i in range(2, len(new_state)):
            if new_state[1] == new_state[i]:
                temp_i = copy.copy(new_state[1])
                new_state.reverse()
                new_state.remove(temp_i)
                new_state.reverse()
                break

        # if self.compare_arrays(new_state, [2, 8, 1]):
        #     print(new_state, action3, action4)
        #     quit()

        return new_state

    def compare_individual_actions(self, action_array1, action_array2):
        if len(action_array1) > len(action_array2):
            temp = copy.copy(action_array1)
            action_array1 = copy.copy(action_array2)
            action_array2 = copy.copy(temp)


        score = 0
        for i in range(len(action_array1)):
            if action_array1[i][0] == action_array2[i][0]:
                score += 0.5
            if action_array1[i][1] == action_array2[i][1]:
                score += 0.5
        # print(action_array1, action_array2)
        # print(score)
        if len(action_array1) != 0:
            score_percentage = (score * 1) / len(action_array1)
        else:
            score_percentage = 0
        # print(score_percentage)
        return score_percentage
