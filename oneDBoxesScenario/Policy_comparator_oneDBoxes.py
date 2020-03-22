import copy
import pickle
import numpy as np
import datetime
import math

class Policy_comparator_oneDBoxes(object):

    def __init__(self, policy_files):
        self.collaborative_policy = []
        self.non_collaborative_policy = []

        #self.get_policies(policy_files)
        
        self.simulation_run_states_and_action = []

        fp = open(policy_files[0], "rb")  # Unpickling
        self.Q_table_col, self.states_numbered_col, self.P_table_col = pickle.load(fp)
        fp.close()

        fp = open(policy_files[1], "rb")  # Unpickling
        self.Q_table_non_col, self.states_numbered_non_col, self.P_table_non_col = pickle.load(fp)
        fp.close()


        self.policies_array = [[self.Q_table_col, self.states_numbered_col, self.P_table_col, "Collaborative"],
                                 [self.Q_table_non_col, self.states_numbered_non_col, self.P_table_non_col,
                                  "Non collaborative"]]

        self.write_date = True

    # def get_policies(self, policy_files):
    #     for file in policy_files:
    #         policy = []
    #         f = open(file, "r")
    #
    #         save = True
    #         appended_line = ""
    #
    #         lines = f.readlines()
    #
    #         for line in lines:
    #             if "State" in line or "final" in line:
    #                 save = True
    #                 if len(appended_line) > 0:
    #
    #                     temp_appended_line = str(appended_line).replace('\'', '')
    #
    #                     temp_appended_line = str(temp_appended_line).replace(',', '')
    #                     split_appended_line = str(temp_appended_line).split('& &')
    #
    #                     # Criar o state
    #                     state_appended_line = split_appended_line[0]
    #                     state_appended_line = state_appended_line.replace(' ', '')
    #                     state_appended_line = state_appended_line.replace('[State(map=[', '')
    #                     state_appended_line = state_appended_line.replace('.', '')
    #                     state_appended_line = state_appended_line.replace(')', '')
    #                     state_appended_line = state_appended_line.replace(']', '')
    #                     state_appended_line = state_appended_line.replace('[', '')
    #                     state_appended_line = state_appended_line.replace('\\n', '')
    #
    #                     state_items = state_appended_line.split('&')
    #
    #                     map = []
    #
    #                     for item in state_items[0]:
    #                         if item == "[":
    #                             pass
    #                         else:
    #                             map.append(int(item))
    #
    #                     # Criar a action
    #                     action_appended_line = split_appended_line[1]
    #                     action_appended_line = action_appended_line.replace(' ', '')
    #                     action = int(action_appended_line)
    #
    #                     policy.append([map, action])
    #
    #                 appended_line = []
    #
    #             if save:
    #                 phrase = ""
    #                 for letter in line:
    #                     phrase += letter
    #                 appended_line += phrase
    #
    #         f.close()
    #
    #         temp_file = copy.deepcopy(file)
    #         temp_file = temp_file.replace('oneDBoxes_MDP_', '')
    #         temp_file = temp_file.replace('_policy.txt', '')
    #
    #         if temp_file == "collaborative":
    #             self.collaborative_policy = policy
    #         elif temp_file == "non_collaborative":
    #             self.non_collaborative_policy = policy

    def receive_world_simulation_run1(self, simulation_run):
        data = []
        for array in self.policies_array:
            actions_according_to_policy = []
            actions_made = []
            #print(array[3])
            for i in range(1, len(simulation_run)):
                old_state = self.get_state_number(simulation_run[i-1], array[1])
                new_state = self.get_state_number(simulation_run[i], array[1])

                if old_state != new_state:
                    for k in range(len(array[0])):
                        equal = True
                        for g in range(len(array[0][k][0])):
                            if simulation_run[i-1][g] != array[0][k][0][g]:
                                equal = False
                                break
                        if equal:
                            actions_according_to_policy.append(array[0][k][1])
                            break

                    max_actions = []
                    for action in array[2]:
                        max_actions.append(action[old_state][new_state])
                    actions_made.append(np.argmax(max_actions))

            v_total = self.V_action_state(actions_according_to_policy, actions_made, len(array[2]))
            data.append([array[3], actions_according_to_policy, actions_made, v_total])
            #self.write_in_txt(array[3], actions__according_to_policy, actions_made, v_total)

        v_total = 0
        for a in data:
            v_total += a[3]

        for a in data:
            a[3] = "{:.2f}".format(a[3] / v_total)

        self.write_in_txt(data)


    def receive_world_simulation_run2(self, simulation_run):
        data = []
        for array in self.policies_array:
            actions_according_to_policy = []
            total_actions_made = []
            action_made = -1
            v = 0
            #print(array[3])
            for i in range(1, len(simulation_run)):
                old_state = self.get_state_number(simulation_run[i-1], array[1])
                new_state = self.get_state_number(simulation_run[i], array[1])
                policy_actions_per_state = []
                if old_state != new_state:
                    for k in range(len(array[0])):
                        equal = True
                        for g in range(len(array[0][k][0])):
                            if simulation_run[i-1][g] != array[0][k][0][g]:
                                equal = False
                                break
                        if equal:
                            actions_according_to_policy.append(np.argmax(array[0][k][2]))
                            policy_actions_per_state.append(array[0][k][2])
                            break

                    max_actions = []
                    for action in array[2]:
                        max_actions.append(action[old_state][new_state])
                    action_made = np.argmax(max_actions)
                    total_actions_made.append(action_made)

                    #print(self.organize_and_get_action_value(action_made, policy_actions_per_state))

                    v += self.organize_and_get_action_value(action_made, policy_actions_per_state)
                    #calcular o V aqui

            #v_total = self.V_action_state(actions_according_to_policy, actions_made, len(array[2]))
            data.append([array[3], actions_according_to_policy, total_actions_made, v])
            #self.write_in_txt(array[3], actions__according_to_policy, actions_made, v_total)

        v_total = 0
        for a in data:
            v_total += a[3]

        for a in data:
            a[3] = "{:.2f}".format(a[3] / v_total)

        self.write_in_txt(data)

    def organize_and_get_action_value(self, action_made, policy_actions_per_state):
        temp_array = copy.deepcopy(policy_actions_per_state[0])
        organized_array = []
        for i in range(len(temp_array)):
            min_action = np.argmin(temp_array)
            organized_array.append(min_action)
            temp_array[min_action] = math.inf

        #print(organized_array)
        #print(action_made)

        for i in range(len(organized_array)):
            if action_made == organized_array[i]:
                return i


    def get_action_from_policy(self, state, policy):
        for line in policy:
            equal = True
            for i in range(len(line[0])):
                if line[0][i] != state[i]:
                    equal = False
            if equal:
                return line[1]

    def get_state_number(self, state, states_numbered):
        for i in range(len(states_numbered)):
            equal = True
            for j in range(len(states_numbered[i])):
                if state[j] != states_numbered[i][j]:
                    equal = False
                    break
            if equal:
                return i
        return -1

    # def V_action_state(self, actions_policy, actions_made, n_possible_policy_actions):
    #     v_total = 0.0
    #
    #     for i in range(len(actions_made)):
    #         if actions_made[i] == actions_policy[i]:
    #             v_total += math.exp(-1)/(math.exp(-1) + (n_possible_policy_actions-1)*math.exp(-2))
    #         #else:
    #          #   v_total += math.exp(-2) / (n_possible_policy_actions * math.exp(-2))
    #
    #     return v_total


    def write_in_txt(self, data):
        f = open("oneDBoxes_CollaborationResults.txt", "a+")

        datetime_object = datetime.datetime.now()
        datetime_object = datetime_object.strftime("DATE_%d-%m-%Y___TIME_%H-%M-%S")
        f.write("%s \n" % datetime_object)
        for item in data:
            f.write("%s \n" % item[0])
            f.write("Actions according to policy -> %s\r" % item[1])
            f.write("Actions according to shappy -> %s\r" % item[2])
            f.write("V -> %s\r" % item[3])
        f.write("\n")
        f.close()