import numpy as np
from numpy import savetxt
import random
import copy
import math
import pickle
from itertools import *


class State:

    def __init__(self, map):
        self.map = map
        # self.first_shappy_pos = first_shappy_pos
        # self.second_shappy_pos = second_shappy_pos

    def __eq__(self, other):
        return isinstance(other,
                          State)  # and self.map == other.map and self.first_shappy_pos == other.first_shappy_pos \
        # and self.second_shappy_pos == other.second_shappy_pos

    def __hash__(self):
        return hash(str(self.map))

    def __str__(self):
        return f"State(map={self.map})"


class MDP_Centralized_policy_maker_oneDBoxes(object):

    def __init__(self, terrain_matrix, policy_file):

        self.map = []
        for line in terrain_matrix:
            if 2 in line:
                self.map = np.array(line)

        random.seed()

        # Environment items
        self.WALL = 1
        self.BOX = 2
        # NON_COL_SHAPPY = 3
        self.SHAPPY1 = 3
        self.SHAPPY2 = 4
        self.BOTH_SHAPPYS = 7
        self.EMPTY = 0

        # map = np.array(
        # [self.WALL, self.BOX, self.EMPTY, self.EMPTY, self.EMPTY, self.SHAPPY, self.EMPTY, self.EMPTY, self.BOX, self.EMPTY, self.BOX, self.SHAPPY, self.EMPTY, self.BOX, self.WALL])

        # Actions
        # self.STAY_STAY = 0
        self.STAY_LEFT = 0
        self.STAY_RIGHT = 1
        self.LEFT_STAY = 2
        self.LEFT_LEFT = 3
        self.LEFT_RIGHT = 4
        self.RIGHT_STAY = 5
        self.RIGHT_LEFT = 6
        self.RIGHT_RIGHT = 7

        self.ACTIONS = [self.STAY_LEFT, self.STAY_RIGHT,
                        self.LEFT_STAY, self.LEFT_LEFT, self.LEFT_RIGHT,
                        self.RIGHT_STAY, self.RIGHT_LEFT, self.RIGHT_RIGHT]
        self.n_actions = len(self.ACTIONS)

        # non_col_shappys = np.where(map == "3")
        # shappys = np.where(self.map == 4 or self.map == 3)
        shappys = []
        for i in range(len(self.map)):
            if self.map[i] == 7:
                shappys.append(i)
                shappys.append(i)
                break
            elif self.map[i] == 3 or self.map[i] == 4:
                shappys.append(i)

        boxes = []
        for i in range(len(self.map)):
            if self.map[i] == 2:
                boxes.append(i)

        self.start_state = State(map=self.map)
        self.current_state = []

        self.gamma = 0.9
        self.learning_rate = 0.1  # alpha

        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.epsilon = self.max_epsilon
        self.decay_rate = 0.001

        self.n_states = len(self.map) * len(shappys) * len(boxes)
        self.n_states *= self.n_states

        # Q_table = np.zeros((n_states, n_actions))
        self.Q_table = dict()

        self.states_numbered = []
        #self.P_table = np.zeros((self.n_states * self.n_actions, self.n_states))
        #self.P_table = dict()
        self.P_table = np.zeros((self.n_actions, self.n_states, self.n_states))

        self.type_of_policy = policy_file.replace("oneDBoxes_MDP_", '')
        self.type_of_policy = self.type_of_policy.replace("_policy2.pickle", '')
        self.type_of_policy = self.type_of_policy.replace("_policy3.pickle", '')

        self.imprimir = False

        self.create_policy()
        self.write_in_txt(policy_file)

    def Q(self, state, action=None):

        if state not in self.Q_table:
            self.Q_table[state] = np.zeros(self.n_actions)
            for i in range(len(self.Q_table[state])):
                self.Q_table[state][i] = -1

        if action is None:
            return self.Q_table[state]

        return self.Q_table[state][action]

    def P(self, state, new_state=None):
        if state not in self.P_table:
            self.P_table[state] = np.zeros(self.n_states)

        if new_state is None:
            return self.P_table[state]

        return self.P_table[state][new_state]

    def choose_actions(self, state):
        random.seed()
        if random.random() < self.epsilon:  # exploration
            return np.random.randint(0, len(self.ACTIONS))
        else:  # exploitation
            return np.argmax(self.Q(state))

    def take_actions(self, state, actions):

        old_first_shappy_pos = 0
        old_second_shappy_pos = 0
        for i in range(len(state.map)):
            if state.map[i] == 7:
                old_first_shappy_pos = i
                old_second_shappy_pos = i
                break
            elif state.map[i] == 3:
                old_first_shappy_pos = i
            elif state.map[i] == 4:
                old_second_shappy_pos = i

        def new_shappy_pos(state, action):
            if action == self.STAY_LEFT:
                first_shappy_pos = old_first_shappy_pos
                if state.map[old_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos - 1
            elif action == self.STAY_RIGHT:
                first_shappy_pos = old_first_shappy_pos
                if state.map[old_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos + 1

            elif action == self.LEFT_STAY:
                if state.map[old_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos - 1
                second_shappy_pos = old_second_shappy_pos
            elif action == self.LEFT_LEFT:
                if state.map[old_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos - 1
                if state.map[old_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos - 1
            elif action == self.LEFT_RIGHT:
                if state.map[old_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos - 1
                if state.map[old_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos + 1

            elif action == self.RIGHT_STAY:
                if state.map[old_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos + 1
                second_shappy_pos = old_second_shappy_pos
            elif action == self.RIGHT_LEFT:
                if state.map[old_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos + 1
                if state.map[old_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos - 1
            elif action == self.RIGHT_RIGHT:
                if state.map[old_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos + 1
                if state.map[old_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos + 1

            else:
                raise ValueError(f"Unknown action {action}")
            return first_shappy_pos, second_shappy_pos

        new_reward = 0
        new_first_shappy_pos, new_second_shappy_pos = new_shappy_pos(state, actions)

        new_map = copy.deepcopy(state.map)
        # Criar as rewards
        if self.type_of_policy == "base":
            if state.map[new_first_shappy_pos] == self.BOX:
                new_reward += 10
            else:
                new_reward += 0
            if state.map[new_second_shappy_pos] == self.BOX:
                new_reward += 10
            else:
                new_reward += 0
        elif self.type_of_policy == "collaborative":
            best_collaboration_path = self.calculate_best_possible_paths()
            shappy3_boxes_path = best_collaboration_path[0]
            shappy4_boxes_path = best_collaboration_path[1]
            if state.map[new_first_shappy_pos] == self.BOX:
                new_reward += 10
            elif shappy3_boxes_path[0] == new_first_shappy_pos:
                new_reward += 2
            elif abs(shappy3_boxes_path[0] - new_first_shappy_pos) < abs(shappy3_boxes_path[0] - old_first_shappy_pos):
                new_reward += 2
            else:
                new_reward -= 10
            if state.map[new_second_shappy_pos] == self.BOX:
                new_reward += 10
            elif shappy4_boxes_path[0] == new_second_shappy_pos:
                new_reward += 2
            elif abs(shappy4_boxes_path[0] - new_second_shappy_pos) < abs(shappy4_boxes_path[0] - old_second_shappy_pos):
                new_reward += 2
            else:
                new_reward -= 10
        elif self.type_of_policy == "non_collaborative":
            first_shappy_closest_box = self.get_closest_box(state, old_first_shappy_pos)
            second_shappy_closest_box = self.get_closest_box(state, old_second_shappy_pos)
            if state.map[new_first_shappy_pos] == self.BOX:
                new_reward += 10
            elif abs(first_shappy_closest_box - new_first_shappy_pos) < \
                    abs(first_shappy_closest_box - old_first_shappy_pos):  # o 1 shappy está a aproximar-se
                new_reward += 2
            else:
                new_reward -= 10
            if state.map[new_second_shappy_pos] == self.BOX:
                new_reward += 10
            elif abs(second_shappy_closest_box - new_second_shappy_pos) < \
                    abs(second_shappy_closest_box - old_second_shappy_pos):  # o 2 shappy está a aproximar-se
                new_reward += 2
            else:
                new_reward -= 10

        # Só mexe o 1 - Mesmo sitio -> Separados
        if old_second_shappy_pos == new_second_shappy_pos and old_first_shappy_pos == old_second_shappy_pos \
                and new_first_shappy_pos != new_second_shappy_pos:
            new_map[old_first_shappy_pos] = self.SHAPPY2
            new_map[new_first_shappy_pos] = self.SHAPPY1

        # Só mexe o 1 - Separados -> Mesmo sitio
        if old_second_shappy_pos == new_second_shappy_pos and old_first_shappy_pos != old_second_shappy_pos \
                and new_first_shappy_pos == new_second_shappy_pos:
            new_map[old_first_shappy_pos] = self.EMPTY
            new_map[new_first_shappy_pos] = self.BOTH_SHAPPYS

        # Só mexe o 2 - Mesmo sitio -> Separados
        elif old_first_shappy_pos == new_first_shappy_pos and old_first_shappy_pos == old_second_shappy_pos \
                and new_first_shappy_pos != new_second_shappy_pos:
            new_map[old_second_shappy_pos] = self.SHAPPY1
            new_map[new_second_shappy_pos] = self.SHAPPY2

        # Só mexe o 2 - Separados -> Mesmo sitio
        elif old_first_shappy_pos == new_first_shappy_pos and old_first_shappy_pos != old_second_shappy_pos \
                and new_first_shappy_pos == new_second_shappy_pos:
            new_map[old_second_shappy_pos] = self.EMPTY
            new_map[new_second_shappy_pos] = self.BOTH_SHAPPYS

        # Mexem os dois - Mesmo sitio -> Mesmo sitio
        elif old_first_shappy_pos == old_second_shappy_pos and new_first_shappy_pos == new_second_shappy_pos:
            new_map[old_first_shappy_pos] = self.EMPTY
            new_map[new_first_shappy_pos] = self.BOTH_SHAPPYS

        # Mexem os dois - Separados -> Mesmo sitio
        elif old_first_shappy_pos != old_second_shappy_pos and new_first_shappy_pos == new_second_shappy_pos:
            new_map[old_first_shappy_pos] = self.EMPTY
            new_map[old_second_shappy_pos] = self.EMPTY
            new_map[new_first_shappy_pos] = self.BOTH_SHAPPYS

        # Mexem os dois - Mesmo sitio -> Separados
        elif old_first_shappy_pos == old_second_shappy_pos and new_first_shappy_pos != new_second_shappy_pos:
            new_map[old_first_shappy_pos] = self.EMPTY
            new_map[new_first_shappy_pos] = self.SHAPPY1
            new_map[new_second_shappy_pos] = self.SHAPPY2

        # Mexem os dois - Separados -> Separados
        elif old_first_shappy_pos != old_second_shappy_pos and new_first_shappy_pos != new_second_shappy_pos:
            new_map[old_first_shappy_pos] = self.EMPTY
            new_map[old_second_shappy_pos] = self.EMPTY
            new_map[new_first_shappy_pos] = self.SHAPPY1
            new_map[new_second_shappy_pos] = self.SHAPPY2

        # first_map_item = state.map[new_first_shappy_pos]
        # second_map_item = state.map[new_second_shappy_pos]
        # if old_first_shappy_pos != new_first_shappy_pos:
        #     if first_map_item == self.BOX:
        #         new_reward = 100
        #         print(" ola", new_map[old_second_shappy_pos])
        #         if new_map[old_first_shappy_pos] != self.BOTH_SHAPPYS:
        #             new_map[old_first_shappy_pos] = self.EMPTY
        #         else:
        #             new_map[old_first_shappy_pos] = self.SHAPPY2
        #         new_map[new_first_shappy_pos] = self.SHAPPY1
        #     elif first_map_item == self.EMPTY:
        #         new_reward = -1
        #         if new_map[old_first_shappy_pos] != self.BOTH_SHAPPYS:
        #             new_map[old_first_shappy_pos] = self.EMPTY
        #         else:
        #             new_map[old_first_shappy_pos] = self.SHAPPY2
        #         new_map[new_first_shappy_pos] = self.SHAPPY1
        #     elif first_map_item == self.SHAPPY1:
        #         new_reward = -1
        #         if new_map[old_first_shappy_pos] != self.BOTH_SHAPPYS:
        #             new_map[old_first_shappy_pos] = self.EMPTY
        #         else:
        #             new_map[old_first_shappy_pos] = self.SHAPPY2
        #         new_map[new_first_shappy_pos] = self.SHAPPY1
        #     elif first_map_item == self.SHAPPY2:
        #         new_reward = -1
        #         if new_map[old_first_shappy_pos] != self.BOTH_SHAPPYS:
        #             new_map[old_first_shappy_pos] = self.EMPTY
        #         else:
        #             new_map[old_first_shappy_pos] = self.SHAPPY2
        #         new_map[new_first_shappy_pos] = self.BOTH_SHAPPYS
        #
        # if old_second_shappy_pos != new_second_shappy_pos:
        #     if second_map_item == self.BOX:
        #         new_reward = 100
        #         if new_map[old_second_shappy_pos] != self.BOTH_SHAPPYS:
        #             new_map[old_second_shappy_pos] = self.EMPTY
        #         else:
        #             new_map[old_second_shappy_pos] = self.SHAPPY1
        #         new_map[new_second_shappy_pos] = self.SHAPPY2
        #     elif second_map_item == self.EMPTY:
        #         new_reward = -1
        #         if new_map[old_second_shappy_pos] != self.BOTH_SHAPPYS:
        #             new_map[old_second_shappy_pos] = self.EMPTY
        #         else:
        #             new_map[old_second_shappy_pos] = self.SHAPPY1
        #         new_map[new_second_shappy_pos] = self.SHAPPY2
        #     elif second_map_item == self.SHAPPY2:
        #         new_reward = -1
        #         if new_map[old_second_shappy_pos] != self.BOTH_SHAPPYS:
        #             new_map[old_second_shappy_pos] = self.EMPTY
        #         else:
        #             new_map[old_second_shappy_pos] = self.SHAPPY1
        #     elif second_map_item == self.SHAPPY1:
        #         new_reward = -1
        #         if new_map[old_second_shappy_pos] != self.BOTH_SHAPPYS:
        #             new_map[old_second_shappy_pos] = self.EMPTY
        #         else:
        #             new_map[old_second_shappy_pos] = self.SHAPPY1
        #         new_map[new_second_shappy_pos] = self.BOTH_SHAPPYS

        return State(map=new_map), new_reward

    def learn(self, state, action, reward, new_state):
        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        self.Q(state)[action] = self.Q(state, action) + self.learning_rate * \
                                (reward + self.gamma * np.max(self.Q(new_state)) - self.Q(state, action))

        state_number = self.get_numbered_state(state.map)
        new_state_number = self.get_numbered_state(new_state.map)
        #print("numbers ", state_number, new_state_number)
        #self.P(state_number)[new_state_number] = action
        self.P_table[action, state_number, new_state_number] += 1

        # Devia aqui alterar a tabela das rewards para cada estado R[state]

    def create_stating_states(self):
        existing_starting_states = [self.start_state]

        map_copy = copy.deepcopy(self.map)
        if 3 in map_copy or 4 in map_copy:
            map_copy = np.where(map_copy == 3, 0, map_copy)
            map_copy = np.where(map_copy == 4, 0, map_copy)

        filled_positions = []
        for i in range(len(map_copy)):
            if map_copy[i] == 1 or map_copy[i] == 2:
                filled_positions.append(i)

        for a in range(100):
            random.seed()
            temp_map = copy.deepcopy(map_copy)
            pos1 = random.randint(1, len(temp_map) - 1)
            while pos1 in filled_positions:
                pos1 = random.randint(1, len(temp_map) - 1)
            filled_positions.append(pos1)  # Os shappys começam sempre em sitios diferentes
            pos2 = random.randint(1, len(temp_map) - 1)
            while pos2 in filled_positions:
                pos2 = random.randint(1, len(temp_map) - 1)
            filled_positions.remove(pos1)

            if pos1 < pos2:
                temp_map[pos1] = 3
                temp_map[pos2] = 4
            else:
                temp_map[pos2] = 3
                temp_map[pos1] = 4

            temp_state = State(map=temp_map)
            already_exists = False
            for state in existing_starting_states:
                comparison = state.map == temp_state.map
                if comparison.all():
                    already_exists = True

            if not already_exists:
                existing_starting_states.append(temp_state)

        return existing_starting_states

    def create_policy(self):

        #total_episodes = 3000  # tenho que aumentar isto para 100000 :(
        total_episodes = 5000

        #starting_states = self.create_stating_states()
        starting_states = [self.start_state]
        # TRAIN
        rewards = []
        for i_state in range(len(starting_states)):
            for episode in range(total_episodes):

                self.current_state = starting_states[i_state]
                # self.calculate_best_possible_paths()
                print("State ", i_state, " Episode ", episode)
                #print("Episode ", episode)
                #print(self.epsilon)
                episode_rewards = []

                keep_going = True
                while True:
                    if 2 not in self.current_state.map:
                        break

                    actions = self.choose_actions(self.current_state)
                    #print("action ", self.current_state, " ", actions)
                    new_state, reward = self.take_actions(self.current_state, actions)

                    # print(new_state, " ",actions)

                    self.learn(self.current_state, actions, reward, new_state)

                    episode_rewards.append(reward)

                    self.current_state = new_state

                if episode == 1000:
                    self.epsilon = 0.5
                elif episode == 2000:
                     self.epsilon = 0.3
                elif episode == 3000:
                     self.epsilon = 0.1
                elif episode == 4500:
                    self.imprimir = True
                    self.epsilon = 0.01
                # elif episode == 2990:
                # if episode == 1:
                #     self.epsilon = 0
                # for line in self.Q_table:
                #     print(line, self.Q(line))
                    # self.epsilon = 0
                # self.epsilon = self.epsilon - self.decay_rate
                # if self.epsilon < self.min_epsilon:
                #     self.epsilon = self.min_epsilon

                rewards.append(np.mean(episode_rewards))


        # # clean up the lines where shappys where in different positions but only one 4 existed
        # lines_to_delete = []
        # for line in self.Q_table:
        #     if np.count_nonzero(line.map == 4) == 1 and line.first_shappy_pos != line.second_shappy_pos:
        #         lines_to_delete.append(line)
        #
        # for line in lines_to_delete:
        #     del self.Q_table[line]

        # for result in rewards:
        #     print(result)

    def write_in_txt(self, policy_file):
        new_Q_table = []
        for line in self.Q_table:
            new_Q_table.append([line.map, self.Q(line)])
        with open(policy_file, "wb") as fp:  # Unpickling
            pickle.dump((new_Q_table, self.states_numbered, self.P_table), fp)
            fp.close()

        # # RESULTS
        # f = open(policy_file, "w+")
        # for line in self.Q_table:
        #     # print(line, "   ", np.argmax(self.Q(line)), "   ", self.Q(line))
        #     f.write("%s && %s && %s \r" % (line, np.argmax(self.Q(line)), self.Q(line)))
        # f.write("Q_TABLE\r")
        #
        # for i in range(len(self.states_numbered)):
        #     f.write("%s \r" % self.states_numbered[i][0]) #, self.states_numbered[i][1]))
        # f.write("States_numbered\r")
        # f.close()
        #
        # savetxt('data.csv', self.P_table, delimiter='.')

    def get_closest_box(self, state, pos):
        closest_box = math.inf
        minimum_distance = math.inf
        box_list = []
        for i in range(len(state.map)):
            if state.map[i] == 2:
                box_list.append(i)

        for box in box_list:
            if abs(box - pos) < minimum_distance:
                minimum_distance = abs(box - pos)
                closest_box = box

        return closest_box

    def get_numbered_state(self, state):
        #print(state)
        equal = True
        while True:
            if len(self.states_numbered) == 0:
                self.states_numbered.append(np.asarray(state))
            else:
                for i in range(len(self.states_numbered)):
                    equal = True
                    for j in range(len(self.states_numbered[i])):
                        if state[j] != self.states_numbered[i][j]:
                            equal = False
                            break
                    if equal:
                        return i
                if not equal:
                    self.states_numbered.append(np.asarray(state))

    #For collaborative behaviour
    # isto só funciona com 2 agentes, não está otimizado para mais
    def calculate_all_possible_paths(self):
        boxes_group = []
        for i in range(len(self.current_state.map)):
            if self.current_state.map[i] == 2:
                boxes_group.append(i)

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
        else:
            paths_combinations.append([paths_combinations[0][1], paths_combinations[0][0]])
            return paths_combinations

    # isto só funciona com 2 agentes, não está otimizado para mais
    def calculate_best_possible_paths(self):
        best_possible_path = []
        possible_paths = self.calculate_all_possible_paths()

        shappy3_pos = -1
        shappy4_pos = -1
        for i in range(len(self.current_state.map)):
            if self.current_state.map[i] == 3:
                shappy3_pos = i
            if self.current_state.map[i] == 4:
                shappy4_pos = i
            if self.current_state.map[i] == 7:
                shappy3_pos = i
                shappy4_pos = i

        minimum_distance_shappy3 = math.inf
        minimum_path_shappy3 = []
        minimum_distance_shappy4 = math.inf
        minimum_path_shappy4 = []
        minimum_total_distance = math.inf

        for path in possible_paths:
            if path[0] == math.inf:
                if shappy3_pos <= shappy4_pos:
                    distance_shappy3 = 0
                    distance_shappy4 = abs(path[1][0] - shappy4_pos)
                    for i in range(1, len(path[1])):
                        distance_shappy4 += abs(path[1][i] - path[1][i - 1])
                    if distance_shappy3 + distance_shappy4 < minimum_total_distance:
                        # print("inf, else ", path)
                        minimum_total_distance = distance_shappy3 + distance_shappy4
                        minimum_distance_shappy3 = distance_shappy3
                        minimum_path_shappy3 = path[0]
                        minimum_distance_shappy4 = distance_shappy4
                        minimum_path_shappy4 = path[1]
                        best_possible_path = [path[1], path[0]]
                elif shappy3_pos > shappy4_pos:
                    distance_shappy4 = 0
                    distance_shappy3 = abs(path[1][0] - shappy3_pos)
                    for i in range(1, len(path[1])):
                        distance_shappy3 += abs(path[1][i] - path[1][i - 1])
                    if distance_shappy4 + distance_shappy3 < minimum_total_distance:
                        minimum_total_distance = distance_shappy4 + distance_shappy3
                        minimum_distance_shappy4 = distance_shappy4
                        minimum_path_shappy4 = path[0]
                        minimum_distance_shappy3 = distance_shappy3
                        minimum_path_shappy3 = path[1]
                        best_possible_path = [path[0], path[1]]
            elif path[1] == math.inf:
                if shappy3_pos <= shappy4_pos:
                    distance_shappy3 = 0
                    distance_shappy4 = abs(path[0][0] - shappy4_pos)
                    for i in range(1, len(path[0])):
                        distance_shappy4 += abs(path[0][i] - path[0][i - 1])
                    if distance_shappy3 + distance_shappy4 < minimum_total_distance:
                        # print("inf, else ", path)
                        minimum_total_distance = distance_shappy3 + distance_shappy4
                        minimum_distance_shappy3 = distance_shappy3
                        minimum_path_shappy3 = path[1]
                        minimum_distance_shappy4 = distance_shappy4
                        minimum_path_shappy4 = path[0]
                        best_possible_path = [path[1], path[0]]
                elif shappy3_pos > shappy4_pos:
                    distance_shappy4 = 0
                    distance_shappy3 = abs(path[0][0] - shappy3_pos)
                    for i in range(1, len(path[0])):
                        distance_shappy3 += abs(path[0][i] - path[0][i - 1])
                    if distance_shappy4 + distance_shappy3 < minimum_total_distance:
                        minimum_total_distance = distance_shappy4 + distance_shappy3
                        minimum_distance_shappy4 = distance_shappy4
                        minimum_path_shappy4 = path[1]
                        minimum_distance_shappy3 = distance_shappy3
                        minimum_path_shappy3 = path[0]
                        best_possible_path = [path[0], path[1]]
            elif len(path[0]) == 1 and path[0][0] != math.inf:
                if shappy3_pos <= shappy4_pos:
                    distance_shappy3 = abs(path[0][0] - shappy3_pos)
                    distance_shappy4 = abs(path[1][0] - shappy4_pos)
                    for i in range(1, len(path[1])):
                        distance_shappy4 += abs(path[1][i] - path[1][i - 1])
                    if distance_shappy3 + distance_shappy4 < minimum_total_distance:
                        minimum_total_distance = distance_shappy3 + distance_shappy4
                        minimum_distance_shappy3 = distance_shappy3
                        minimum_path_shappy3 = path[0]
                        minimum_distance_shappy4 = distance_shappy4
                        minimum_path_shappy4 = path[1]
                        best_possible_path = [path[0], path[1]]
                elif shappy3_pos > shappy4_pos:
                    distance_shappy4 = abs(path[0][0] - shappy4_pos)
                    distance_shappy3 = abs(path[1][0] - shappy3_pos)
                    for i in range(1, len(path[1])):
                        distance_shappy3 += abs(path[1][i] - path[1][i - 1])
                    if distance_shappy4 + distance_shappy3 < minimum_total_distance:
                        minimum_total_distance = distance_shappy4 + distance_shappy3
                        minimum_distance_shappy3 = distance_shappy4
                        minimum_path_shappy4 = path[0]
                        minimum_distance_shappy3 = distance_shappy3
                        minimum_path_shappy3 = path[1]
                        best_possible_path = [path[1], path[0]]
            elif len(path[1]) == 1 and path[1][0] != math.inf:
                if shappy3_pos <= shappy4_pos:
                    distance_shappy3 = abs(path[0][0] - shappy3_pos)
                    distance_shappy4 = abs(path[1][0] - shappy4_pos)
                    for i in range(1, len(path[1])):
                        distance_shappy4 += abs(path[1][i] - path[1][i - 1])
                    if distance_shappy3 + distance_shappy4 < minimum_total_distance:
                        minimum_total_distance = distance_shappy3 + distance_shappy4
                        minimum_distance_shappy3 = distance_shappy3
                        minimum_path_shappy3 = path[0]
                        minimum_distance_shappy4 = distance_shappy4
                        minimum_path_shappy4 = path[1]
                        best_possible_path = [path[1], path[0]]
                elif shappy3_pos > shappy4_pos:
                    distance_shappy4 = abs(path[0][0] - shappy4_pos)
                    distance_shappy3 = abs(path[1][0] - shappy3_pos)
                    for i in range(1, len(path[1])):
                        distance_shappy3 += abs(path[1][i] - path[1][i - 1])
                    if distance_shappy4 + distance_shappy3 < minimum_total_distance:
                        minimum_total_distance = distance_shappy4 + distance_shappy3
                        minimum_distance_shappy3 = distance_shappy4
                        minimum_path_shappy4 = path[0]
                        minimum_distance_shappy3 = distance_shappy3
                        minimum_path_shappy3 = path[1]
                        best_possible_path = [path[0], path[1]]
            else:
                if shappy3_pos <= shappy4_pos:
                    distance_shappy3 = abs(path[0][0] - shappy3_pos)
                    for i in range(1, len(path[0])):
                        distance_shappy3 += abs(path[0][i] - path[0][i - 1])
                        distance_shappy4 = abs(path[1][0] - shappy4_pos)
                        for j in range(1, len(path[1])):
                            distance_shappy4 += abs(path[1][j] - path[1][j - 1])
                        if distance_shappy3 + distance_shappy4 < minimum_total_distance:
                            print("else, else ", path)
                            minimum_total_distance = distance_shappy3 + distance_shappy4
                            minimum_distance_shappy3 = distance_shappy3
                            minimum_path_shappy3 = path[0]
                            minimum_distance_shappy4 = distance_shappy4
                            minimum_path_shappy4 = path[1]
                            best_possible_path = path
                elif shappy3_pos > shappy4_pos:
                    distance_shappy4 = abs(path[0][0] - shappy4_pos)
                    for i in range(1, len(path[0])):
                        distance_shappy4 += abs(path[0][i] - path[0][i - 1])
                        distance_shappy3 = abs(path[1][0] - shappy3_pos)
                        for j in range(1, len(path[1])):
                            distance_shappy3 += abs(path[1][j] - path[1][j - 1])
                        if distance_shappy4 + distance_shappy3 < minimum_total_distance:
                            minimum_total_distance = distance_shappy4 + distance_shappy3
                            minimum_distance_shappy4 = distance_shappy4
                            minimum_path_shappy3 = path[0]
                            minimum_distance_shappy3 = distance_shappy3
                            minimum_path_shappy3 = path[1]
                            best_possible_path = [path[1], path[0]]


        # # 1º shappy é o shappy4
        # elif shappy4_pos < shappy3_pos:
        #     for path in possible_paths:
        #         if path[0] == math.inf:
        #             distance_shappy4 = 0
        #             distance_shappy3 = abs(path[1][0] - shappy3_pos)
        #             for i in range(1, len(path[1])):
        #                 distance_shappy3 += abs(path[1][i] - path[1][i - 1])
        #             if distance_shappy4 + distance_shappy3 < minimum_total_distance:
        #                 minimum_total_distance = distance_shappy4 + distance_shappy3
        #                 minimum_distance_shappy4 = distance_shappy4
        #                 minimum_path_shappy4 = path[0]
        #                 minimum_distance_shappy3 = distance_shappy3
        #                 minimum_path_shappy3 = path[1]
        #                 best_possible_path = [path[1], path[0]]
        #         elif len(path[0]) == 1 and path[0][0] != math.inf:
        #             distance_shappy4 = abs(path[0][0] - shappy4_pos)
        #             distance_shappy3 = abs(path[1][0] - shappy3_pos)
        #             for i in range(1, len(path[1])):
        #                 distance_shappy3 += abs(path[1][i] - path[1][i - 1])
        #             if distance_shappy4 + distance_shappy3 < minimum_total_distance:
        #                 minimum_total_distance = distance_shappy4 + distance_shappy3
        #                 minimum_distance_shappy3 = distance_shappy4
        #                 minimum_path_shappy4 = path[0]
        #                 minimum_distance_shappy3 = distance_shappy3
        #                 minimum_path_shappy3 = path[1]
        #                 best_possible_path = [path[1], path[0]]
        #         else:
        #             distance_shappy4 = abs(path[0][0] - shappy4_pos)
        #             for i in range(1, len(path[0])):
        #                 distance_shappy4 += abs(path[0][i] - path[0][i - 1])
        #                 distance_shappy3 = abs(path[1][0] - shappy3_pos)
        #                 for j in range(1, len(path[1])):
        #                     distance_shappy3 += abs(path[1][j] - path[1][j - 1])
        #                 if distance_shappy4 + distance_shappy3 < minimum_total_distance:
        #                     minimum_total_distance = distance_shappy4 + distance_shappy3
        #                     minimum_distance_shappy4 = distance_shappy4
        #                     minimum_path_shappy3 = path[0]
        #                     minimum_distance_shappy3 = distance_shappy3
        #                     minimum_path_shappy3 = path[1]
        #                     best_possible_path = [path[1], path[0]]

        # for path in possible_paths:
        #     if path[0] == math.inf:
        #         distance_agent_1 = 0
        #         distance_agent_2 = abs(path[1][0] - agent2[1])
        #         for i in range(1, len(path[1])):
        #             distance_agent_2 += abs(path[1][i] - path[1][i - 1])
        #         if distance_agent_2 < minimum_distance_agent_2:
        #             minimum_total_distance = distance_agent_1 + distance_agent_2
        #             minimum_distance_agent_1 = distance_agent_1
        #             minimum_path_agent_1 = path[0]
        #             minimum_distance_agent_2 = distance_agent_2
        #             minimum_path_agent_2 = path[1]
        #             best_possible_path = path
        #     elif len(path[0]) == 1 and path[0][0] != math.inf:
        #         distance_agent_1 = abs(path[0][0] - agent1[1])
        #         distance_agent_2 = abs(path[1][0] - agent2[1])
        #         for i in range(1, len(path[1])):
        #             distance_agent_2 += abs(path[1][i] - path[1][i - 1])
        #         if distance_agent_2 < minimum_distance_agent_2:
        #             minimum_total_distance = distance_agent_1 + distance_agent_2
        #             minimum_distance_agent_1 = distance_agent_1
        #             minimum_path_agent_1 = path[0]
        #             minimum_distance_agent_2 = distance_agent_2
        #             minimum_path_agent_2 = path[1]
        #             best_possible_path = path
        #     else:
        #         distance_agent_1 = abs(path[0][0] - agent1[1])
        #         for i in range(1, len(path[0])):
        #             distance_agent_1 += abs(path[0][i] - path[0][i - 1])
        #             distance_agent_2 = abs(path[1][0] - agent2[1])
        #             for j in range(1, len(path[1])):
        #                 distance_agent_2 += abs(path[1][j] - path[1][j - 1])
        #             if (distance_agent_1 + distance_agent_2) < minimum_total_distance:
        #                 minimum_total_distance = distance_agent_1 + distance_agent_2
        #                 minimum_distance_agent_1 = distance_agent_1
        #                 minimum_path_agent_1 = path[0]
        #                 minimum_distance_agent_2 = distance_agent_2
        #                 minimum_path_agent_2 = path[1]
        #                 best_possible_path = path
        #                 print(agent1_pos_x, " ", agent2_pos_x , " ", path, "  ", distance_agent_1, "  ", distance_agent_2)
        #
        # print("a " , agent1_pos_x, " ", agent2_pos_x, " ", best_possible_path, "  ", distance_agent_1, "  ", distance_agent_2)

        if best_possible_path[0] == math.inf:
            best_possible_path[0] = [shappy3_pos]
        if best_possible_path[1] == math.inf:
            best_possible_path[1] = [shappy4_pos]


        return best_possible_path
