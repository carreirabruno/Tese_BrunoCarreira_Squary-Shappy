import copy

class Policy_comparator_oneDBoxes(object):

    def __init__(self, policy_files):
        self.collaborative_policy = []
        self.non_collaborative_policy = []

        self.get_policies(policy_files)
        
        self.simulation_run_states_and_action = []

    def get_policies(self, policy_files):
        for file in policy_files:
            policy = []
            f = open(file, "r")

            save = True
            appended_line = ""

            lines = f.readlines()

            for line in lines:
                if "State" in line or "final" in line:
                    save = True
                    if len(appended_line) > 0:

                        temp_appended_line = str(appended_line).replace('\'', '')

                        temp_appended_line = str(temp_appended_line).replace(',', '')
                        split_appended_line = str(temp_appended_line).split('& &')

                        # Criar o state
                        state_appended_line = split_appended_line[0]
                        state_appended_line = state_appended_line.replace(' ', '')
                        state_appended_line = state_appended_line.replace('[State(map=[', '')
                        state_appended_line = state_appended_line.replace('.', '')
                        state_appended_line = state_appended_line.replace(')', '')
                        state_appended_line = state_appended_line.replace(']', '')
                        state_appended_line = state_appended_line.replace('[', '')
                        state_appended_line = state_appended_line.replace('\\n', '')

                        state_items = state_appended_line.split('&')

                        map = []

                        for item in state_items[0]:
                            if item == "[":
                                pass
                            else:
                                map.append(int(item))

                        # Criar a action
                        action_appended_line = split_appended_line[1]
                        action_appended_line = action_appended_line.replace(' ', '')
                        action = int(action_appended_line)

                        policy.append([map, action])

                    appended_line = []

                if save:
                    phrase = ""
                    for letter in line:
                        phrase += letter
                    appended_line += phrase

            f.close()

            temp_file = copy.deepcopy(file)
            temp_file = temp_file.replace('oneDBoxes_MDP_', '')
            temp_file = temp_file.replace('_policy.txt', '')

            if temp_file == "collaborative":
                self.collaborative_policy = policy
            elif temp_file == "non_collaborative":
                self.non_collaborative_policy = policy

    def receive_world_simulation_run(self, simulation_run):
        self.simulation_run_states_and_action = []
        for i in range(1, len(simulation_run)):
            shappy3_old = -1
            shappy3_new = -1
            shappy4_old = -1
            shappy4_new = -1
            for j in range(len(simulation_run[i])):
                if simulation_run[i-1][j] == 3:
                    shappy3_old = j
                elif simulation_run[i-1][j] == 4:
                    shappy4_old = j
                if simulation_run[i][j] == 3:
                    shappy3_new = j
                elif simulation_run[i][j] == 4:
                    shappy4_new = j

            if shappy3_new == shappy3_old and shappy4_new < shappy4_old:        # STAY_LEFT
                self.simulation_run_states_and_action.append([simulation_run[i-1], 0])
            elif shappy3_new == shappy3_old and shappy4_new > shappy4_old:      # STAY_RIGHT
                self.simulation_run_states_and_action.append([simulation_run[i - 1], 1])
            elif shappy3_new < shappy3_old and shappy4_new == shappy4_old:      # LEFT_STAY
                self.simulation_run_states_and_action.append([simulation_run[i - 1], 2])
            elif shappy3_new < shappy3_old and shappy4_new < shappy4_old:      # LEFT_LEFT
                self.simulation_run_states_and_action.append([simulation_run[i - 1], 3])
            elif shappy3_new < shappy3_old and shappy4_new > shappy4_old:      # LEFT_RIGHT
                self.simulation_run_states_and_action.append([simulation_run[i - 1], 4])
            elif shappy3_new > shappy3_old and shappy4_new == shappy4_old:      # RIGHT_STAY
                self.simulation_run_states_and_action.append([simulation_run[i - 1], 5])
            elif shappy3_new > shappy3_old and shappy4_new < shappy4_old:      # RIGHT_LEFT
                self.simulation_run_states_and_action.append([simulation_run[i - 1], 6])
            elif shappy3_new > shappy3_old and shappy4_new > shappy4_old:      # RIGHT_RIGHT
                self.simulation_run_states_and_action.append([simulation_run[i - 1], 7])

        self.compare_run_to_policies()

    def compare_run_to_policies(self):
        col = 0
        non_col = 0
        for item in self.simulation_run_states_and_action:
            collaborative_action = self.get_action_from_policy(item[0], self.collaborative_policy)
            non_collaborative_action = self.get_action_from_policy(item[0], self.non_collaborative_policy)
            if item[1] == collaborative_action:
                col += 1
            elif item[1] == non_collaborative_action:
                non_col += 1
        print(col, " ", non_col)


    def get_action_from_policy(self, state, policy):
        for line in policy:
            equal = True
            for i in range(len(line[0])):
                if line[0][i] != state[i]:
                    equal = False
            if equal:
                return line[1]

