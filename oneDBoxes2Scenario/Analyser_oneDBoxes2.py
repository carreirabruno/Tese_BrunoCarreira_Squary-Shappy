import datetime
import math
import copy
import pickle
import numpy as np

class Analyser_oneDBoxes2(object):

    def __init__(self, terrain_matrix, simulation_states, map_policies):
        for line in terrain_matrix:
            if 3 in line:
                self.map = line

        initial_state = []
        for i in range(len(self.map)):
            if int(self.map[i]) == 3:
                initial_state.append(i)
            if int(self.map[i]) == 4:
                initial_state.append(i)
        for i in range(len(self.map)):
            if int(self.map[i]) == 2:
                initial_state.append(i)

        self.simulation_states = [initial_state]

        for line in simulation_states:
            self.simulation_states.append(line)

        self.map_policies = map_policies

        # Base Actions
        self.STAY = 0
        self.LEFT = 1
        self.RIGHT = 2
        self.BASE_ACTIONS = [self.STAY, self.LEFT, self.RIGHT]

        self.compare_to_politics()

    def compare_to_politics(self):
        data = []
        sum_equal_moves = 0
        for policy_file in self.map_policies:
            equal_moves = 0
            filename = policy_file.replace("oneDBoxes2_MDP_", "")
            policy_type = filename.replace("_policy_map1.pickle", "")
            policy_type = policy_type.replace("_policy_map2.pickle", "")
            policy_type = policy_type.replace("_policy_map3.pickle", "")

            if policy_type == "peer_aware_decentralized" or policy_type == "peer_communication_decentralized":
                fp = open(policy_file, "rb")  # Unpickling
                policy, policy2 = pickle.load(fp)
                fp.close()
            else:
                fp = open(policy_file, "rb")  # Unpickling
                policy = pickle.load(fp)
                fp.close()

            self.map_type = filename.replace(policy_type+"_policy_", "")
            self.map_type = self.map_type.replace(".pickle", "")

            communication_3_knows = False
            communication_4_knows = False

            for i in range(1,len(self.simulation_states)):
                old_pos_shappy3 = self.simulation_states[i-1][0]
                new_pos_shappy3 = self.simulation_states[i][0]
                action_shappy3 = -1
                if old_pos_shappy3 == new_pos_shappy3:
                    action_shappy3 = 0
                elif old_pos_shappy3 > new_pos_shappy3:
                    action_shappy3 = 1
                elif old_pos_shappy3 < new_pos_shappy3:
                    action_shappy3 = 2

                old_pos_shappy4 = self.simulation_states[i-1][1]
                new_pos_shappy4 = self.simulation_states[i][1]
                action_shappy4 = -1
                if old_pos_shappy4 == new_pos_shappy4:
                    action_shappy4 = 0
                elif old_pos_shappy4 > new_pos_shappy4:
                    action_shappy4 = 1
                elif old_pos_shappy4 < new_pos_shappy4:
                    action_shappy4 = 2

                combined_action = -1
                if policy_type == "centralized":
                    for j in range(len(policy)):
                        if self.simulation_states[i - 1] in policy[j]:
                            if np.argmax(policy[j][1]) == 0:
                                if action_shappy3 == 0 and action_shappy4 == 1:
                                    equal_moves += 1
                                # if action_shappy4 == 1:
                                #     equal_moves += 0.5
                            elif np.argmax(policy[j][1]) == 1:
                                if action_shappy3 == 0 and action_shappy4 == 2:
                                    equal_moves += 1
                                # if action_shappy4 == 2:
                                #     equal_moves += 0.5
                            elif np.argmax(policy[j][1]) == 2:
                                if action_shappy3 == 1 and action_shappy4 == 0:
                                    equal_moves += 1
                                # if action_shappy4 == 0:
                                #     equal_moves += 0.5
                            elif np.argmax(policy[j][1]) == 3:
                                if action_shappy3 == 1 and action_shappy4 == 1:
                                    equal_moves += 1
                                # if action_shappy4 == 1:
                                #     equal_moves += 0.5
                            elif np.argmax(policy[j][1]) == 4:
                                if action_shappy3 == 1 and action_shappy4 == 2:
                                    equal_moves += 1
                                # if action_shappy4 == 2:
                                #     equal_moves += 0.5
                            elif np.argmax(policy[j][1]) == 5:
                                if action_shappy3 == 2 and action_shappy4 == 0:
                                    equal_moves += 1
                                # if action_shappy4 == 0:
                                #     equal_moves += 0.5
                            elif np.argmax(policy[j][1]) == 6:
                                if action_shappy3 == 2 and action_shappy4 == 1:
                                    equal_moves += 1
                                # if action_shappy4 == 1:
                                #     equal_moves += 0.5
                            elif np.argmax(policy[j][1]) == 7:
                                if action_shappy3 == 2 and action_shappy4 == 2:
                                    equal_moves += 1
                                # if action_shappy4 == 2:
                                #     equal_moves += 0.5

                    # if action_shappy3 == 0 and action_shappy4 == 1:
                    #    combined_action = 0
                    # elif action_shappy3 == 0 and action_shappy4 == 2:
                    #    combined_action = 1
                    # elif action_shappy3 == 1 and action_shappy4 == 0:
                    #    combined_action = 2
                    # elif action_shappy3 == 1 and action_shappy4 == 1:
                    #    combined_action = 3
                    # elif action_shappy3 == 1 and action_shappy4 == 2:
                    #    combined_action = 4
                    # elif action_shappy3 == 2 and action_shappy4 == 0:
                    #    combined_action = 5
                    # elif action_shappy3 == 2 and action_shappy4 == 1:
                    #    combined_action = 6
                    # elif action_shappy3 == 2 and action_shappy4 == 2:
                    #    combined_action = 7
                    #
                    # for j in range(len(policy)):
                    #     if self.simulation_states[i - 1] in policy[j]:
                    #         if np.argmax(policy[j][1]) == combined_action:
                    #             equal_moves += 1

                elif policy_type == "decentralized":
                    right_move = False
                    temp_state3 = copy.copy(self.simulation_states[i - 1])
                    temp_state4 = copy.copy(self.simulation_states[i - 1])
                    temp_state3.remove(temp_state3[1])
                    temp_state4.remove(temp_state4[0])

                    for j in range(len(policy)):
                        if len(temp_state3) == len(policy[j][0]):
                            if self.compare_equal_equal_sized_arrays(temp_state3, policy[j][0]):
                                if np.argmax(policy[j][1]) == action_shappy3:
                                    # equal_moves += 0.5
                                    right_move = True
                                    break
                    for j in range(len(policy)):
                        if len(temp_state4) == len(policy[j][0]):
                            if self.compare_equal_equal_sized_arrays(temp_state4, policy[j][0]):
                                if np.argmax(policy[j][1]) == action_shappy4 and right_move:
                                    equal_moves += 1
                                    break

                elif policy_type == "peer_aware_decentralized":
                    right_move = False
                    temp_state3 = copy.copy(self.simulation_states[i - 1])
                    temp_state4 = copy.copy(self.simulation_states[i - 1])

                    for j in range(len(policy)):
                        if len(temp_state3) == len(policy[j][0]):
                            if self.compare_equal_equal_sized_arrays(temp_state3, policy[j][0]):
                                if np.argmax(policy[j][1]) == action_shappy3:
                                    # equal_moves += 0.5
                                    right_move = True
                                    break
                                elif (action_shappy3 == 0 and temp_state3[0] == 1 and np.argmax(policy[j][1]) == 1) or (action_shappy3 == 0 and temp_state3[0] == 8 and np.argmax(policy[j][1]) == 2):
                                    right_move = True
                                    break

                    for j in range(len(policy2)):
                        if len(temp_state4) == len(policy2[j][0]):
                            if self.compare_equal_equal_sized_arrays(temp_state4, policy2[j][0]):
                                if np.argmax(policy2[j][1]) == action_shappy4 and right_move:
                                    equal_moves += 1
                                    break
                                elif (action_shappy4 == 0 and temp_state4[1] == 1 and np.argmax(policy[j][1]) == 1) or (action_shappy4 == 0 and temp_state4[1] == 8 and np.argmax(policy[j][1]) == 2):
                                    equal_moves += 1
                                    break

                elif policy_type == "peer_communication_decentralized":
                    right_move = False
                    temp_state3 = copy.copy(self.simulation_states[i - 1])
                    temp_state4 = copy.copy(self.simulation_states[i - 1])
                    if not communication_3_knows:
                        temp_state3[1] = -1
                    if not communication_4_knows:
                        temp_state4[0] = -1

                    for j in range(len(policy)):
                        if len(temp_state3) == len(policy[j][0]):
                            if self.compare_equal_equal_sized_arrays(temp_state3, policy[j][0]):
                                if np.argmax(policy[j][1]) == 3 and action_shappy3 == 0:
                                    action_shappy3 = 3
                                if np.argmax(policy[j][1]) == action_shappy3:

                                    # equal_moves += 0.5
                                    right_move = True
                                    break
                                elif (action_shappy3 == 0 and temp_state3[0] == 1 and np.argmax(policy[j][1]) == 1) or (action_shappy3 == 0 and temp_state3[0] == 8 and np.argmax(policy[j][1]) == 2):
                                    right_move = True
                                    break
                                elif (action_shappy3 == 0 and temp_state3[0] == 1 and np.argmax(policy[j][1]) == 1) or (action_shappy3 == 0 and temp_state3[0] == 8 and np.argmax(policy[j][1]) == 2):
                                    right_move = True
                                    break
                    for j in range(len(policy2)):
                        if len(temp_state4) == len(policy2[j][0]):
                            if self.compare_equal_equal_sized_arrays(temp_state4, policy2[j][0]):
                                if np.argmax(policy2[j][1]) == 3 and action_shappy4 == 0:
                                    action_shappy4 = 3
                                if np.argmax(policy2[j][1]) == action_shappy4 and right_move:
                                    equal_moves += 1
                                    break
                                elif (action_shappy4 == 0 and temp_state4[1] == 1 and np.argmax(policy[j][1]) == 1) or (action_shappy4 == 0 and temp_state4[1] == 8 and np.argmax(policy[j][1]) == 2):
                                    equal_moves += 1
                                    break

                    if action_shappy3 == 3:
                        communication_4_knows = True
                    if action_shappy4 == 3:
                        communication_3_knows = True

            sum_equal_moves += equal_moves
            normalized_equal_moves = (equal_moves/(len(self.simulation_states) - 1)) * 100
            data.append([self.simulation_states, policy_type, normalized_equal_moves, equal_moves])

        #sum_equal_moves = (len(self.simulation_states)-1) * 2
        # float(x - minX) * float(100 - 0) / (maxX - minX)

        for item in data:
            scaled_zero_to_ten = (item[3] * 100) / sum_equal_moves
            item[3] = scaled_zero_to_ten

        self.write_in_txt(data)

    def write_in_txt(self, data):

        filename = "oneDBoxes_CollaborationResults2_" + self.map_type + ".txt"
        f = open(filename, "a+")

        datetime_object = datetime.datetime.now()
        datetime_object = datetime_object.strftime("DATE_%d-%m-%Y___TIME_%H-%M-%S")
        f.write("%s \n" % datetime_object)

        f.write("States:\r")
        for state in data[0][0]:
            f.write("%s\r" % state)
        for item in data:
            f.write("%s policy  -  %s  -  %s\r" % (item[1], item[2], item[3]))
        f.write("\n")
        f.close()

    def compare_equal_equal_sized_arrays(self, array1, array2):
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                return False
        return True