import numpy as np
from numpy import savetxt
import random
import copy
import math
import pickle
from itertools import *
import time
import pandas as pd
import matplotlib.pyplot as plt


class State:

    def __init__(self, state):
        self.state = state

    def __eq__(self, other):
        return isinstance(other, State)

    def __hash__(self):
        return hash(str(self.state))

    def __str__(self):
        return f"{self.state}"


class MDP_Centralized_policy_maker_twoDBoxes2(object):

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
        # self.STAY_STAY = 0
        self.STAY_LEFT = 0
        self.STAY_RIGHT = 1
        self.STAY_UP = 2
        self.STAY_DOWN = 3
        
        self.LEFT_STAY = 4
        self.LEFT_LEFT = 5
        self.LEFT_RIGHT = 6
        self.LEFT_UP = 7
        self.LEFT_DOWN = 8
        
        self.RIGHT_STAY = 9
        self.RIGHT_LEFT = 10
        self.RIGHT_RIGHT = 11
        self.RIGHT_UP = 12
        self.RIGHT_DOWN = 13
        
        self.UP_STAY = 14
        self.UP_LEFT = 15
        self.UP_RIGHT = 16
        self.UP_UP = 17
        self.UP_DOWN = 18
        
        self.DOWN_STAY = 19
        self.DOWN_LEFT = 20
        self.DOWN_RIGHT = 21
        self.DOWN_UP = 22
        self.DOWN_DOWN = 23
    
        self.ACTIONS = [self.STAY_LEFT, self.STAY_RIGHT, self.STAY_UP, self.STAY_DOWN,
                        self.LEFT_STAY, self.LEFT_LEFT, self.LEFT_RIGHT, self.LEFT_UP, self.LEFT_DOWN,
                        self.RIGHT_STAY, self.RIGHT_LEFT, self.RIGHT_RIGHT, self.RIGHT_UP, self.RIGHT_DOWN,
                        self.UP_STAY, self.UP_LEFT, self.UP_RIGHT, self.UP_UP, self.UP_DOWN,
                        self.DOWN_STAY, self.DOWN_LEFT, self.DOWN_RIGHT, self.DOWN_UP, self.DOWN_DOWN]
        self.n_actions = len(self.ACTIONS)

        self.current_state = []
        self.current_map = []

        self.gamma = 0.9
        self.learning_rate = 0.1  # alpha

        self.max_epsilon = 0.1
        self.min_epsilon = 0.01
        self.epsilon = self.max_epsilon

        self.Q_table = dict()

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

    def choose_actions(self, state):
        random.seed()
        if random.random() < self.epsilon:  # exploration
            return np.random.randint(0, len(self.ACTIONS))
        else:  # exploitation
            state_obj = State(state)
            return np.argmax(self.Q(state_obj))

    def take_actions(self, state, action, map):
        old_shappy3_pos = state[0]
        old_shappy4_pos = state[1]

        def get_new_shappy_position(map, action):
            new_shappy3_pos = -1
            new_shappy4_pos = -1
            if action == self.STAY_LEFT:
                new_shappy3_pos = old_shappy3_pos
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] - 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] - 1]
            elif action == self.STAY_RIGHT:
                new_shappy3_pos = old_shappy3_pos
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] + 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] + 1]
            elif action == self.STAY_UP:
                new_shappy3_pos = old_shappy3_pos
                if map[old_shappy4_pos[0] - 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] - 1, old_shappy4_pos[1]]
            elif action == self.STAY_DOWN:
                new_shappy3_pos = old_shappy3_pos
                if map[old_shappy4_pos[0] + 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] + 1, old_shappy4_pos[1]]

            elif action == self.LEFT_STAY:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] - 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] - 1]
                new_shappy4_pos = old_shappy4_pos
            elif action == self.LEFT_LEFT:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] - 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] - 1]
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] - 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] - 1]
            elif action == self.LEFT_RIGHT:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] - 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] - 1]
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] + 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] + 1]
            elif action == self.LEFT_UP:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] - 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] - 1]
                if map[old_shappy4_pos[0] - 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] - 1, old_shappy4_pos[1]]
            elif action == self.LEFT_DOWN:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] - 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] - 1]
                if map[old_shappy4_pos[0] + 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] + 1, old_shappy4_pos[1]]

            elif action == self.RIGHT_STAY:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] + 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] + 1]
                new_shappy4_pos = old_shappy4_pos
            elif action == self.RIGHT_LEFT:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] + 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] + 1]
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] - 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] - 1]
            elif action == self.RIGHT_RIGHT:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] + 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] + 1]
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] + 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] + 1]
            elif action == self.RIGHT_UP:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] + 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] + 1]
                if map[old_shappy4_pos[0] - 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] - 1, old_shappy4_pos[1]]
            elif action == self.RIGHT_DOWN:
                if map[old_shappy3_pos[0]][old_shappy3_pos[1] + 1] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0], old_shappy3_pos[1] + 1]
                if map[old_shappy4_pos[0] + 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] + 1, old_shappy4_pos[1]]

            elif action == self.UP_STAY:
                if map[old_shappy3_pos[0] - 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] - 1, old_shappy3_pos[1]]
                new_shappy4_pos = old_shappy4_pos
            elif action == self.UP_LEFT:
                if map[old_shappy3_pos[0] - 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] - 1, old_shappy3_pos[1]]
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] - 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] - 1]
            elif action == self.UP_RIGHT:
                if map[old_shappy3_pos[0] - 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] - 1, old_shappy3_pos[1]]
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] + 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] + 1]
            elif action == self.UP_UP:
                if map[old_shappy3_pos[0] - 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] - 1, old_shappy3_pos[1]]
                if map[old_shappy4_pos[0] - 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] - 1, old_shappy4_pos[1]]
            elif action == self.UP_DOWN:
                if map[old_shappy3_pos[0] - 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] - 1, old_shappy3_pos[1]]
                if map[old_shappy4_pos[0] + 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] + 1, old_shappy4_pos[1]]

            elif action == self.DOWN_STAY:
                if map[old_shappy3_pos[0] + 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] + 1, old_shappy3_pos[1]]
                new_shappy4_pos = old_shappy4_pos
            elif action == self.DOWN_LEFT:
                if map[old_shappy3_pos[0] + 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] + 1, old_shappy3_pos[1]]
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] - 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] - 1]
            elif action == self.DOWN_RIGHT:
                if map[old_shappy3_pos[0] + 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] + 1, old_shappy3_pos[1]]
                if map[old_shappy4_pos[0]][old_shappy4_pos[1] + 1] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0], old_shappy4_pos[1] + 1]
            elif action == self.DOWN_UP:
                if map[old_shappy3_pos[0] + 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] + 1, old_shappy3_pos[1]]
                if map[old_shappy4_pos[0] - 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] - 1, old_shappy4_pos[1]]
            elif action == self.DOWN_DOWN:
                if map[old_shappy3_pos[0] + 1][old_shappy3_pos[1]] == self.WALL:
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = [old_shappy3_pos[0] + 1, old_shappy3_pos[1]]
                if map[old_shappy4_pos[0] + 1][old_shappy4_pos[1]] == self.WALL:
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = [old_shappy4_pos[0] + 1, old_shappy4_pos[1]]

            else:
                raise ValueError(f"Unknown action {action}")

            return new_shappy3_pos, new_shappy4_pos

        new_shappy3_pos, new_shappy4_pos = get_new_shappy_position(map, action)

        new_map = copy.deepcopy(map)

        # # Criar as rewards
        new_reward = 0
        # # Joint Rewards
        if self.joint_rewards:
            if map[new_shappy3_pos[0]][new_shappy3_pos[1]] == self.BOX or map[new_shappy4_pos[0]][
                                                                              new_shappy4_pos[1]] == self.BOX:
                new_reward += 100
        # # Split Rewards
        # else:
        #     if map[new_shappy3_pos[0]][new_shappy3_pos[1]] == self.BOX:
        #         new_reward += 100
        #     if map[new_shappy4_pos[0]][new_shappy4_pos[1]] == self.BOX:
        #         new_reward4 += 100

        if not self.compare_arrays(new_shappy3_pos, old_shappy3_pos):
            new_reward -= 1
        if not self.compare_arrays(new_shappy4_pos, old_shappy4_pos):
            new_reward -= 1

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

        return new_state, new_map, new_reward

    def learn(self, state, action, reward, new_state):
        state_obj = State(state)
        new_state_obj = State(new_state)

        self.Q(state_obj)[action] = self.Q(state_obj, action) + self.learning_rate * \
                                    (reward + self.gamma * np.max(self.Q(new_state_obj)) - self.Q(state_obj, action))

    def create_stating_states(self):
        existing_starting_states = [self.start_state]
        existing_starting_maps = [self.start_map]

        map_copy = copy.deepcopy(self.start_map)
        if 3 in map_copy:
            map_copy = np.where(map_copy == 3, 0, map_copy)
            map_copy = np.where(map_copy == 4, 0, map_copy)

        filled_positions = []
        boxes_positions_temp = []
        for i in range(len(map_copy)):
            if map_copy[i] == 1 or map_copy[i] == 2:
                filled_positions.append(i)

        for a in range(100):
            random.seed()
            temp_map = copy.deepcopy(map_copy)
            pos1 = random.randint(1, len(temp_map) - 1)
            while pos1 in filled_positions:
                pos1 = random.randint(1, len(temp_map) - 1)
            # filled_positions.append(pos1)  # Os shappys começam sempre em sitios diferentes
            pos2 = random.randint(1, len(temp_map) - 1)
            while pos2 in filled_positions:
                pos2 = random.randint(1, len(temp_map) - 1)

            if pos1 < pos2:
                temp_map[pos1] = 3
                temp_map[pos2] = 4
            elif pos1 > pos2:
                temp_map[pos2] = 3
                temp_map[pos1] = 4
            else:
                temp_map[pos1] = 7

            temp_state = []

            for i in range(len(temp_map)):
                if int(temp_map[i]) == 7:
                    temp_state.append(i)
                    temp_state.append(i)
                    break
                if int(temp_map[i]) == 3:
                    temp_state.append(i)
                if int(temp_map[i]) == 4:
                    temp_state.append(i)
            for i in range(len(temp_map)):
                if int(temp_map[i]) == 2:
                    temp_state.append(i)

            already_exists = False
            for state in existing_starting_states:
                equal = True
                for i in range(len(state)):
                    if len(temp_state) != len(state) or temp_state[i] != state[i]:
                        equal = False
                if equal:
                    already_exists = True

            if not already_exists:
                existing_starting_maps.append(temp_map)
                existing_starting_states.append(temp_state)

        return existing_starting_states, existing_starting_maps

    def create_random_initial_states(self):
        random.seed()
        occupied_list = copy.deepcopy(self.start_state)
        occupied_list.pop(0)
        occupied_list.pop(0)

        new_positions = []

        x = -1
        y = -1
        for i in range(2):
            equal = True
            while equal:
                random.seed()
                x = random.randint(1, 8)
                y = random.randint(1, 8)
                for item in occupied_list:
                    if self.compare_arrays(item, [x, y]) or self.start_map[x][y] == 1:
                        equal = True
                        break
                    else:
                        equal = False

            new_positions.append([x, y])
            occupied_list.append([x, y])

        if new_positions[0][0] < new_positions[1][0] or (new_positions[0][0] == new_positions[1][0] and
                                                         new_positions[0][1] < new_positions[1][1]):
            shappy3_new_pos = new_positions[0]
            shappy4_new_pos = new_positions[1]
        else:
            shappy3_new_pos = new_positions[1]
            shappy4_new_pos = new_positions[0]

        new_state = copy.deepcopy(self.start_state)
        new_state[0] = shappy3_new_pos
        new_state[1] = shappy4_new_pos

        new_map = copy.deepcopy(self.start_map)

        new_map[self.start_state[0][0]][self.start_state[0][1]] = 0
        new_map[self.start_state[1][0]][self.start_state[1][1]] = 0

        new_map[new_state[0][0]][new_state[0][1]] = 3
        new_map[new_state[1][0]][new_state[1][1]] = 4

        # for line in self.start_map:
        #     print(line)
        # print()
        #
        # for line in new_map:
        #     print(line)
        # quit()

        return new_state, new_map

    def create_policy(self):

        total_episodes = 100000

        starting_states = [self.start_state]
        starting_maps = [self.start_map]

        step_array = []
        time_array = []
        # TRAIN
        for i_state in range(len(starting_states)):
            for episode in range(total_episodes):

                # self.current_state = starting_states[i_state]
                # self.current_map = starting_maps[i_state]
                self.current_state, self.current_map = self.create_random_initial_states()

                # print("State ", i_state, "/", len(starting_states) - 1, " Episode ", episode, "/", total_episodes)
                print((episode * 100) / total_episodes, "%")

                episode_rewards = []

                start_time = time.time()

                step_count = 0
                while True:
                    if len(self.current_state) == 2 or step_count == 64:
                        # time_array.append(time.time() - start_time)
                        step_array.append(step_count)
                        break

                    self.number_boxes = self.current_number_of_boxes(self.current_map)

                    actions = self.choose_actions(self.current_state)

                    new_state, new_map, reward = self.take_actions(self.current_state, actions, self.current_map)

                    self.learn(self.current_state, actions, reward, new_state)

                    episode_rewards.append(reward)

                    self.current_state = new_state

                    self.current_map = new_map

                    step_count += 1

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
                # elif episode == 1500:
                #      self.epsilon = 0.3
                # elif episode == 2500:
                #      self.epsilon = 0.1
                # elif episode == 4800:
                #     self.epsilon = 0.01

                # if episode == 1000:
                #     self.epsilon = 0.5
                # elif episode == 2000:
                #      self.epsilon = 0.3
                # elif episode == 3500:
                #      self.epsilon = 0.1
                # elif episode == 8000:
                #     self.epsilon = 0.01

                # if episode == 4000:
                #     self.epsilon = 0.5
                # elif episode == 9000:
                #      self.epsilon = 0.3
                # elif episode == 30000:
                #      self.epsilon = 0.1
                # elif episode == 990000:
                #     self.epsilon = 0.01

                # if episode == int(total_episodes / 20):
                #     self.epsilon = 0.5
                #     # print("                                        " , self.epsilon)
                # elif episode == int(total_episodes / 10):
                #     self.epsilon = 0.3
                #     # print("                                        " , self.epsilon)
                # elif episode == int(total_episodes / 5):
                #     self.epsilon = 0.1
                #     # print("                                        " , self.epsilon)
                # elif episode == int(total_episodes - (total_episodes / 10)):
                #     self.epsilon = 0.01
                    # print("                                        ", self.epsilon)

        # self.plot_an_array(time_array)
        self.plot_an_array(step_array)

    def write_in_txt(self, policy_file):
        new_Q_table = []
        for line in self.Q_table:
            new_Q_table.append([line.state, self.Q(line)])

        with open(policy_file, "wb") as fp:  # Unpickling
            pickle.dump(new_Q_table, fp)
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

    def plot_an_array(self, array):
        plt.plot(array, '.', color='black')
        plt.show()