import numpy as np
from numpy import savetxt
import random
import copy
import math
import pickle
from itertools import *


class State:

    def __init__(self, state):
        self.state = state

    def __eq__(self, other):
        return isinstance(other, State)

    def __hash__(self):
        return hash(str(self.state))

    def __str__(self):
        return f"{self.state}"


class MDP_Individual_Decentralized_policy_maker_twoDBoxes2(object):

    def __init__(self, terrain_matrix, policy_file, joint_rewards):

        self.start_map = []
        for line in terrain_matrix:
            temp_array = []
            for letter in line:
                temp_array.append(int(letter))
            self.start_map.append(temp_array)

        self.start_state = []
        for i in range(len(self.start_map)):
            for j in range(len(self.start_map[i])):
                if int(self.start_map[i][j]) == 7:
                    self.start_state.append([i, j])
                    self.start_state.append([i, j])
                    break
                if int(self.start_map[i][j]) == 3:
                    self.start_state.append([i, j])
                    break
        for i in range(len(self.start_map)):
            for j in range(len(self.start_map[i])):
                if int(self.start_map[i][j]) == 4:
                    self.start_state.append([i, j])
                    break
        for i in range(len(self.start_map)):
            for j in range(len(self.start_map[i])):
                if int(self.start_map[i][j]) == 2:
                    self.start_state.append([i, j])

        self.joint_rewards = joint_rewards

        random.seed()

        # Environment items
        self.WALL = 1
        self.BOX = 2
        self.SHAPPY3 = 3
        self.SHAPPY4 = 4
        self.BOTH_SHAPPYS = 7
        self.EMPTY = 0

        # Actions
        self.STAY = 0
        self.LEFT = 1
        self.RIGHT = 2
        self.UP = 3
        self.DOWN = 4

        self.ACTIONS = [self.STAY, self.LEFT, self.RIGHT, self.UP, self.DOWN]
        self.n_actions = len(self.ACTIONS)

        self.current_state = []
        self.current_map = []

        self.gamma = 0.9
        self.learning_rate = 0.1  # alpha

        self.max_epsilon = 0.9
        self.min_epsilon = 0.01
        self.epsilon = self.max_epsilon
        self.decay_rate = 0.001

        self.Q_table = dict()
        self.Q_tableTwo = dict()

        self.number_boxes = 0

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

    def Q2(self, state, action=None):
        if state not in self.Q_tableTwo:
            self.Q_tableTwo[state] = np.zeros(self.n_actions)
            for i in range(len(self.Q_tableTwo[state])):
                self.Q_tableTwo[state][i] = -1

        if action is None:
            return self.Q_tableTwo[state]

        return self.Q_tableTwo[state][action]

    def choose_actions(self, state):
        random.seed()
        if random.random() < self.epsilon:  # exploration
            return np.random.randint(0, len(self.ACTIONS))
        else:  # exploitation
            state_obj = State(state)
            return np.argmax(self.Q(state_obj))

    def choose_actions2(self, state):
        random.seed()
        if random.random() < self.epsilon:  # exploration
            return np.random.randint(0, len(self.ACTIONS))
        else:  # exploitation
            state_obj = State(state)
            return np.argmax(self.Q2(state_obj))

    def take_actions(self, state_shappy3, action3, state_shappy4, action4, map):
        old_shappy3_pos = state_shappy3[0]
        old_shappy4_pos = state_shappy4[0]

        def get_new_shappy_position(map, action3, action4):
            new_shappy3_pos = -1
            if action3 == self.STAY:
                new_shappy3_pos = old_shappy3_pos
            elif action3 == self.LEFT:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] - 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] - 1]
            elif action3 == self.RIGHT:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] + 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] + 1]
            elif action3 == self.UP:
                if map[old_shappy3_pos[0] - 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] - 1, old_shappy3_pos[1]]
            elif action3 == self.DOWN:
                if map[old_shappy3_pos[0] + 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] + 1, old_shappy3_pos[1]]
            else:
                raise ValueError(f"Unknown action {action3}")

            new_shappy4_pos = -1
            if action4 == self.STAY:
                new_shappy4_pos = old_shappy4_pos
            elif action4 == self.LEFT:
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] - 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] - 1]
            elif action4 == self.RIGHT:
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] + 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] + 1]
            elif action4 == self.UP:
                if map[old_shappy4_pos[0] - 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] - 1, old_shappy4_pos[1]]
            elif action4 == self.DOWN:
                if map[old_shappy4_pos[0] + 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] + 1, old_shappy4_pos[1]]
            else:
                raise ValueError(f"Unknown action {action4}")


            return new_shappy3_pos, new_shappy4_pos

        new_reward = 0
        new_shappy3_pos, new_shappy4_pos = get_new_shappy_position(map, action3, action4)

        new_map = copy.deepcopy(map)

        # # Criar as rewards
        new_reward3 = 0
        new_reward4 = 0
        # # Joint Rewards
        if self.joint_rewards:
            if map[new_shappy3_pos[0]][new_shappy3_pos[1]] == self.BOX or map[new_shappy4_pos[0]][new_shappy4_pos[1]] == self.BOX:
                new_reward3 += 100
                new_reward4 += 100

        # # Split Rewards
        else:
            if map[new_shappy3_pos[0]][new_shappy3_pos[1]] == self.BOX:
                new_reward3 += 100
            if map[new_shappy4_pos[0]][new_shappy4_pos[1]] == self.BOX:
                new_reward4 += 100

        if not self.compare_arrays(new_shappy3_pos, old_shappy3_pos):
            new_reward3 -= 1
        if not self.compare_arrays(new_shappy4_pos, old_shappy4_pos):
            new_reward4 -= 1

        # Só mexe o 1 - Mesmo sitio -> Separados
        if self.compare_arrays(old_shappy4_pos, new_shappy4_pos) and \
                self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                not self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy3_pos[0]][old_shappy3_pos[1]] = self.SHAPPY4
            new_map[new_shappy3_pos[0]][new_shappy3_pos[1]] = self.SHAPPY3

        # Só mexe o 1 - Separados -> Mesmo sitio
        elif self.compare_arrays(old_shappy4_pos, new_shappy4_pos) and \
                not self.compare_arrays(old_shappy3_pos, old_shappy4_pos) \
                and self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy3_pos[0]][old_shappy3_pos[1]] = self.EMPTY
            new_map[new_shappy3_pos[0]][new_shappy3_pos[1]] = self.BOTH_SHAPPYS

        # Só mexe o 1 - Separados -> Separados
        elif self.compare_arrays(old_shappy4_pos, new_shappy4_pos) and \
                not self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                not self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy3_pos[0]][old_shappy3_pos[1]] = self.EMPTY
            new_map[new_shappy3_pos[0]][new_shappy3_pos[1]] = self.SHAPPY3

        # Só mexe o 2 - Mesmo sitio -> Separados
        elif self.compare_arrays(old_shappy3_pos, new_shappy3_pos) and \
                self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                not self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy4_pos[0]][old_shappy4_pos[1]] = self.SHAPPY3
            new_map[new_shappy4_pos[0]][new_shappy4_pos[1]] = self.SHAPPY4

        # Só mexe o 2 - Separados -> Mesmo sitio
        elif self.compare_arrays(old_shappy3_pos, new_shappy3_pos) and \
                not self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy4_pos[0]][old_shappy4_pos[1]] = self.EMPTY
            new_map[new_shappy4_pos[0]][new_shappy4_pos[1]] = self.BOTH_SHAPPYS

        # Só mexe o 2 - Separados -> Separados
        elif self.compare_arrays(old_shappy3_pos, new_shappy3_pos) and \
                not self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                not self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy4_pos[0]][old_shappy4_pos[1]] = self.EMPTY
            new_map[new_shappy4_pos[0]][new_shappy4_pos[1]] = self.SHAPPY4

        # Mexem os dois - Mesmo sitio -> Mesmo sitio
        elif self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy3_pos[0]][old_shappy3_pos[1]] = self.EMPTY
            new_map[new_shappy3_pos[0]][new_shappy3_pos[1]] = self.BOTH_SHAPPYS

        # Mexem os dois - Separados -> Mesmo sitio
        elif not self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy3_pos[0]][old_shappy3_pos[1]] = self.EMPTY
            new_map[old_shappy4_pos[0]][old_shappy4_pos[1]] = self.EMPTY
            new_map[new_shappy3_pos[0]][new_shappy3_pos[1]] = self.BOTH_SHAPPYS

        # Mexem os dois - Mesmo sitio -> Separados
        elif self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                not self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy3_pos[0]][old_shappy3_pos[1]] = self.EMPTY
            new_map[new_shappy3_pos[0]][new_shappy3_pos[1]] = self.SHAPPY3
            new_map[new_shappy4_pos[0]][new_shappy4_pos[1]] = self.SHAPPY4

        # Mexem os dois - Separados -> Separados
        elif not self.compare_arrays(old_shappy3_pos, old_shappy4_pos) and \
                not self.compare_arrays(new_shappy3_pos, new_shappy4_pos):
            new_map[old_shappy3_pos[0]][old_shappy3_pos[1]] = self.EMPTY
            new_map[old_shappy4_pos[0]][old_shappy4_pos[1]] = self.EMPTY
            new_map[new_shappy3_pos[0]][new_shappy3_pos[1]] = self.SHAPPY3
            new_map[new_shappy4_pos[0]][new_shappy4_pos[1]] = self.SHAPPY4
        
        new_state = []
        for i in range(len(new_map)):
            for j in range(len(new_map[i])):
                if int(new_map[i][j]) == 7:
                    new_state.append([i, j])
                    new_state.append([i, j])
                    break
                if int(new_map[i][j]) == 3:
                    new_state.append([i, j])
                    break
        for i in range(len(new_map)):
            for j in range(len(new_map[i])):
                if int(new_map[i][j]) == 4:
                    new_state.append([i, j])
                    break
        for i in range(len(new_map)):
            for j in range(len(new_map[i])):
                if int(new_map[i][j]) == 2:
                    new_state.append([i, j])

        new_shappy3_state = copy.copy(new_state)
        new_shappy3_state.remove(new_shappy3_state[1])
        new_shappy4_state = copy.copy(new_state)
        new_shappy4_state.remove(new_shappy4_state[0])

        return new_shappy3_state, new_shappy4_state, new_map, new_reward3, new_reward4

    def learn(self, old_state3, new_state3, action3, old_state4, new_state4, action4, reward3, reward4):
        old_state3_obj = State(old_state3)
        new_state3_obj = State(new_state3)

        old_state4_obj = State(old_state4)
        new_state4_obj = State(new_state4)

        self.Q(old_state3_obj)[action3] = self.Q(old_state3_obj, action3) + self.learning_rate * \
                                (reward3 + self.gamma * np.max(self.Q(new_state3_obj)) - self.Q(old_state3_obj, action3))

        self.Q2(old_state4_obj)[action4] = self.Q2(old_state4_obj, action4) + self.learning_rate * \
                                (reward4 + self.gamma * np.max(self.Q2(new_state4_obj)) - self.Q2(old_state4_obj, action4))

    def create_stating_states(self):
        existing_starting_states = [self.start_state]
        existing_starting_maps = [self.start_map]

        return existing_starting_states, existing_starting_maps

    def create_policy(self):

        total_episodes = 100000

        starting_states, starting_maps = self.create_stating_states()

        # TRAIN
        rewards = []
        for i_state in range(len(starting_states)):
            for episode in range(total_episodes):
                self.current_state = starting_states[i_state]
                self.current_map = starting_maps[i_state]

                shappy3_state = copy.copy(self.current_state)
                shappy3_state.remove(shappy3_state[1])
                shappy4_state = copy.copy(self.current_state)
                shappy4_state.remove(shappy4_state[0])

                # print("State ", i_state, "/", len(starting_states), " Episode ", episode, "/", total_episodes)
                print((episode * 100) / total_episodes, "%")

                episode_rewards = []

                while True:
                    if len(shappy3_state) == 1 and len(shappy4_state) == 1:
                        break

                    # self.number_boxes = self.current_number_of_boxes(self.current_map)

                    action3 = self.choose_actions(shappy3_state)

                    action4 = self.choose_actions2(shappy4_state)

                    new_shappy3_state, new_shappy4_state, new_map, reward3, reward4 = self.take_actions(shappy3_state, action3, shappy4_state, action4, self.current_map)

                    self.learn(shappy3_state, new_shappy3_state, action3, shappy4_state, new_shappy4_state, action4, reward3, reward4)
                    episode_rewards.append(reward3)
                    episode_rewards.append(reward4)

                    shappy3_state = new_shappy3_state
                    shappy4_state = new_shappy4_state

                    self.current_map = new_map

                # if episode == 100:
                #     self.epsilon = 0.5
                # elif episode == 300:
                #      self.epsilon = 0.3
                # elif episode == 500:
                #      self.epsilon = 0.1
                # elif episode == 900:
                #     self.epsilon = 0.01

                # if episode == 500:
                #     self.epsilon = 0.5
                # elif episode == 900:
                #      self.epsilon = 0.3
                # elif episode == 1500:
                #      self.epsilon = 0.1
                # elif episode == 2800:
                #     self.epsilon = 0.01

                # if episode == 800:
                #     self.epsilon = 0.5
                # elif episode == 1400:
                #      self.epsilon = 0.3
                # elif episode == 2000:
                #      self.epsilon = 0.1
                # elif episode == 8000:
                #     self.epsilon = 0.01

                # if episode == 1000:
                #     self.epsilon = 0.5
                # elif episode == 2500:
                #      self.epsilon = 0.3
                # elif episode == 5000:
                #      self.epsilon = 0.1
                # elif episode == 8000:
                #     self.epsilon = 0.01

                if episode == int(total_episodes / 20):
                    self.epsilon = 0.5
                    # print("                                        " , self.epsilon)
                elif episode == int(total_episodes / 10):
                    self.epsilon = 0.3
                    # print("                                        " , self.epsilon)
                elif episode == int(total_episodes / 5):
                    self.epsilon = 0.1
                    # print("                                        " , self.epsilon)
                elif episode == int(total_episodes - (total_episodes / 10)):
                    self.epsilon = 0.01
                    # print("                                        ", self.epsilon)
                # elif episode == int(total_episodes - (total_episodes / 100)):
                #     self.epsilon = 0

                # if episode == 4000:
                #     self.epsilon = 0.5
                # elif episode == 9000:
                #      self.epsilon = 0.3
                # elif episode == 20000:
                #      self.epsilon = 0.1
                # elif episode == 990000:
                #     self.epsilon = 0.01

                rewards.append(np.mean(episode_rewards))

    def write_in_txt(self, policy_file):
        new_Q_table = []
        for line in self.Q_table:
            new_Q_table.append([line.state, self.Q(line)])

        new_Q_table2 = []
        for line in self.Q_tableTwo:
            new_Q_table2.append([line.state, self.Q2(line)])

        with open(policy_file, "wb") as fp:  # pickling
            pickle.dump((new_Q_table, new_Q_table2), fp)
            fp.close()

    def current_number_of_boxes(self, mapa):
        counter = 0
        for item in mapa:
            if item == 2:
                counter += 1
        return counter

    def compare_arrays(self, array1, array2):
        if len(array1) != len(array2):
            return False
        else:
            for i in range(len(array1)):
                if array1[i] != array2[i]:
                    return False
        return True
