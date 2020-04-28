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

    def __eq__(self, other):
        return isinstance(other,
                          State)

    def __hash__(self):
        return hash(str(self.map))

    def __str__(self):
        return f"{self.map}"


class MDP_Centralized_policy_maker2_twoDBoxes2(object):

    def __init__(self, terrain_matrix, policy_file):

        #Tirar o espaço do "chat"
        terrain_matrix = terrain_matrix[:-2]

        self.map = []
        for line in terrain_matrix:
            temp_array = []
            for letter in line:
            #     if int(letter) == 4:
            #         temp_array.append(int(3))
            #     else:
                temp_array.append(int(letter))
            self.map.append(temp_array)

        random.seed()

        # Environment items
        self.WALL = 1
        self.BOX = 2
        self.SHAPPY1 = 3
        self.SHAPPY2 = 4
        #self.SHAPPY = 3
        self.BOTH_SHAPPYS = 7
        self.EMPTY = 0

        # Actions
        self.STAY_STAY = 0
        self.STAY_LEFT = 1
        self.STAY_RIGHT = 2
        self.STAY_UP = 3
        self.STAY_DOWN = 4

        self.LEFT_STAY = 5
        self.LEFT_LEFT = 6
        self.LEFT_RIGHT = 7
        self.LEFT_UP = 8
        self.LEFT_DOWN = 9

        self.RIGHT_STAY = 10
        self.RIGHT_LEFT = 11
        self.RIGHT_RIGHT = 12
        self.RIGHT_UP = 13
        self.RIGHT_DOWN = 14

        self.UP_STAY = 15
        self.UP_LEFT = 16
        self.UP_RIGHT = 17
        self.UP_UP = 18
        self.UP_DOWN = 19

        self.DOWN_STAY = 20
        self.DOWN_LEFT = 21
        self.DOWN_RIGHT = 22
        self.DOWN_UP = 23
        self.DOWN_DOWN = 24

        self.COMMUNICATE_COMMUNICATE = 25

        self.ACTIONS = [self.STAY_STAY, self.STAY_LEFT, self.STAY_RIGHT, self.STAY_UP, self.STAY_DOWN,
                        self.LEFT_STAY, self.LEFT_LEFT, self.LEFT_RIGHT, self.LEFT_UP, self.LEFT_DOWN,
                        self.RIGHT_STAY, self.RIGHT_LEFT, self.RIGHT_RIGHT, self.RIGHT_UP, self.RIGHT_DOWN,
                        self.UP_STAY, self.UP_LEFT, self.UP_RIGHT, self.UP_UP, self.UP_DOWN,
                        self.DOWN_STAY, self.DOWN_LEFT, self.DOWN_RIGHT, self.DOWN_UP, self.DOWN_DOWN,
                        self.COMMUNICATE_COMMUNICATE]
        self.n_actions = len(self.ACTIONS)

        shappys = []
        boxes = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 2:
                    boxes.append([i, j])
                if self.map[i][j] == 7:
                    shappys.append([i, j])
                    shappys.append([i, j])
                elif self.map[i][j] == 3 or self.map[i][j] == 4:
                    shappys.append([i, j])

        self.start_state = State(map=self.map)
        self.current_state = []

        self.gamma = 0.9
        self.learning_rate = 0.1  # alpha

        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.epsilon = self.max_epsilon
        self.decay_rate = 0.001

        self.Q_table = dict()

        self.states_numbered = []

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
            return np.argmax(self.Q(state))

    def take_actions(self, state, actions):

        new_reward = 0
        new_first_shappy_pos, new_second_shappy_pos, old_first_shappy_pos, \
                                                     old_second_shappy_pos = self.new_shappy_pos(state, actions)

        new_map = copy.deepcopy(state.map)

        # Criar as rewards
        if state.map[new_first_shappy_pos[0]][new_first_shappy_pos[1]] == self.BOX:
            new_reward += 10
        else:
            new_reward += 0
        if state.map[new_second_shappy_pos[0]][new_second_shappy_pos[1]] == self.BOX:
            new_reward += 10
        else:
            new_reward += 0

        # Só mexe o 1 - Mesmo sitio -> Separados
        if old_second_shappy_pos == new_second_shappy_pos and old_first_shappy_pos == old_second_shappy_pos \
                and new_first_shappy_pos != new_second_shappy_pos:
            new_map[old_first_shappy_pos[0]][old_first_shappy_pos[1]] = self.SHAPPY2
            new_map[new_first_shappy_pos[0]][new_first_shappy_pos[1]] = self.SHAPPY1

        # Só mexe o 1 - Separados -> Mesmo sitio
        if old_second_shappy_pos == new_second_shappy_pos and old_first_shappy_pos != old_second_shappy_pos \
                and new_first_shappy_pos == new_second_shappy_pos:
            new_map[old_first_shappy_pos[0]][old_first_shappy_pos[1]] = self.EMPTY
            new_map[new_first_shappy_pos[0]][new_first_shappy_pos[1]] = self.BOTH_SHAPPYS

        # Só mexe o 2 - Mesmo sitio -> Separados
        elif old_first_shappy_pos == new_first_shappy_pos and old_first_shappy_pos == old_second_shappy_pos \
                and new_first_shappy_pos != new_second_shappy_pos:
            new_map[old_second_shappy_pos[0]][old_second_shappy_pos[1]] = self.SHAPPY1
            new_map[new_second_shappy_pos[0]][new_second_shappy_pos[1]] = self.SHAPPY2

        # Só mexe o 2 - Separados -> Mesmo sitio
        elif old_first_shappy_pos == new_first_shappy_pos and old_first_shappy_pos != old_second_shappy_pos \
                and new_first_shappy_pos == new_second_shappy_pos:
            new_map[old_second_shappy_pos[0]][old_second_shappy_pos[1]] = self.EMPTY
            new_map[new_second_shappy_pos[0]][new_second_shappy_pos[1]] = self.BOTH_SHAPPYS

        # Mexem os dois - Mesmo sitio -> Mesmo sitio
        elif old_first_shappy_pos == old_second_shappy_pos and new_first_shappy_pos == new_second_shappy_pos:
            new_map[old_first_shappy_pos[0]][old_first_shappy_pos[1]] = self.EMPTY
            new_map[new_first_shappy_pos[0]][new_first_shappy_pos[1]] = self.BOTH_SHAPPYS

        # Mexem os dois - Separados -> Mesmo sitio
        elif old_first_shappy_pos != old_second_shappy_pos and new_first_shappy_pos == new_second_shappy_pos:
            new_map[old_first_shappy_pos[0]][old_first_shappy_pos[1]] = self.EMPTY
            new_map[old_second_shappy_pos[0]][old_second_shappy_pos[1]] = self.EMPTY
            new_map[new_first_shappy_pos[0]][new_first_shappy_pos[1]] = self.BOTH_SHAPPYS

        # Mexem os dois - Mesmo sitio -> Separados
        elif old_first_shappy_pos == old_second_shappy_pos and new_first_shappy_pos != new_second_shappy_pos:
            new_map[old_first_shappy_pos[0]][old_first_shappy_pos[1]] = self.EMPTY
            new_map[new_first_shappy_pos[0]][new_first_shappy_pos[1]] = self.SHAPPY1
            new_map[new_second_shappy_pos[0]][new_second_shappy_pos[1]] = self.SHAPPY2

        # Mexem os dois - Separados -> Separados
        elif old_first_shappy_pos != old_second_shappy_pos and new_first_shappy_pos != new_second_shappy_pos:
            new_map[old_first_shappy_pos[0]][old_first_shappy_pos[1]] = self.EMPTY
            new_map[old_second_shappy_pos[0]][old_second_shappy_pos[1]] = self.EMPTY
            new_map[new_first_shappy_pos[0]][new_first_shappy_pos[1]] = self.SHAPPY1
            new_map[new_second_shappy_pos[0]][new_second_shappy_pos[1]] = self.SHAPPY2

        return State(map=new_map), new_reward

    def new_shappy_pos(self, state, action):
        old_first_shappy_pos = []
        old_second_shappy_pos = []
        for i in range(len(state.map)):
            for j in range(len(state.map[i])):
                if state.map[i][j] == 7:
                    old_first_shappy_pos = [i, j]
                    old_second_shappy_pos = [i, j]
                    break
                elif state.map[i][j] == 3:
                    old_first_shappy_pos = [i, j]
                elif state.map[i][j] == 4:
                    old_second_shappy_pos = [i, j]

        if action == self.STAY_STAY:
            first_shappy_pos = old_first_shappy_pos
            second_shappy_pos = old_second_shappy_pos
        elif action == self.STAY_LEFT:
            first_shappy_pos = old_first_shappy_pos
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] - 1]
        elif action == self.STAY_RIGHT:
            first_shappy_pos = old_first_shappy_pos
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] + 1]
        elif action == self.STAY_UP:
            first_shappy_pos = old_first_shappy_pos
            if state.map[old_second_shappy_pos[0] - 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] - 1, old_second_shappy_pos[1]]
        elif action == self.STAY_DOWN:
            first_shappy_pos = old_first_shappy_pos
            if state.map[old_second_shappy_pos[0] + 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] + 1, old_second_shappy_pos[1]]

        elif action == self.LEFT_STAY:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] - 1]
            second_shappy_pos = old_second_shappy_pos
        elif action == self.LEFT_LEFT:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] - 1]
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] - 1]
        elif action == self.LEFT_RIGHT:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] - 1]
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] + 1]
        elif action == self.LEFT_UP:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] - 1]
            if state.map[old_second_shappy_pos[0] - 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] - 1, old_second_shappy_pos[1]]
        elif action == self.LEFT_DOWN:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] - 1]
            if state.map[old_second_shappy_pos[0] + 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] + 1, old_second_shappy_pos[1]]

        elif action == self.RIGHT_STAY:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] + 1]
            second_shappy_pos = old_second_shappy_pos
        elif action == self.RIGHT_LEFT:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] + 1]
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] - 1]
        elif action == self.RIGHT_RIGHT:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] + 1]
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] + 1]
        elif action == self.RIGHT_UP:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] + 1]
            if state.map[old_second_shappy_pos[0] - 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] - 1, old_second_shappy_pos[1]]
        elif action == self.RIGHT_DOWN:
            if state.map[old_first_shappy_pos[0]][old_first_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0], old_first_shappy_pos[1] + 1]
            if state.map[old_second_shappy_pos[0] + 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] + 1, old_second_shappy_pos[1]]

        elif action == self.UP_STAY:
            if state.map[old_first_shappy_pos[0] - 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] - 1, old_first_shappy_pos[1]]
            second_shappy_pos = old_second_shappy_pos
        elif action == self.UP_LEFT:
            if state.map[old_first_shappy_pos[0] - 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] - 1, old_first_shappy_pos[1]]
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] - 1]
        elif action == self.UP_RIGHT:
            if state.map[old_first_shappy_pos[0] - 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] - 1, old_first_shappy_pos[1]]
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] + 1]
        elif action == self.UP_UP:
            if state.map[old_first_shappy_pos[0] - 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] - 1, old_first_shappy_pos[1]]
            if state.map[old_second_shappy_pos[0] - 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] - 1, old_second_shappy_pos[1]]
        elif action == self.UP_DOWN:
            if state.map[old_first_shappy_pos[0] - 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] - 1, old_first_shappy_pos[1]]
            if state.map[old_second_shappy_pos[0] + 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] + 1, old_second_shappy_pos[1]]

        elif action == self.DOWN_STAY:
            if state.map[old_first_shappy_pos[0] + 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] + 1, old_first_shappy_pos[1]]
            second_shappy_pos = old_second_shappy_pos
        elif action == self.DOWN_LEFT:
            if state.map[old_first_shappy_pos[0] + 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] + 1, old_first_shappy_pos[1]]
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] - 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] - 1]
        elif action == self.DOWN_RIGHT:
            if state.map[old_first_shappy_pos[0] + 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] + 1, old_first_shappy_pos[1]]
            if state.map[old_second_shappy_pos[0]][old_second_shappy_pos[1] + 1] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0], old_second_shappy_pos[1] + 1]
        elif action == self.DOWN_UP:
            if state.map[old_first_shappy_pos[0] + 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] + 1, old_first_shappy_pos[1]]
            if state.map[old_second_shappy_pos[0] - 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] - 1, old_second_shappy_pos[1]]
        elif action == self.DOWN_DOWN:
            if state.map[old_first_shappy_pos[0] + 1][old_first_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                first_shappy_pos = old_first_shappy_pos
            else:
                first_shappy_pos = [old_first_shappy_pos[0] + 1, old_first_shappy_pos[1]]
            if state.map[old_second_shappy_pos[0] + 1][old_second_shappy_pos[1]] == self.WALL:  # colidiu com uma self.WALL
                second_shappy_pos = old_second_shappy_pos
            else:
                second_shappy_pos = [old_second_shappy_pos[0] + 1, old_second_shappy_pos[1]]

        else:
            raise ValueError(f"Unknown action {action}")

        return first_shappy_pos, second_shappy_pos, old_first_shappy_pos, old_second_shappy_pos

    def learn(self, state, action, reward, new_state):
        self.Q(state)[action] = self.Q(state, action) + self.learning_rate * \
                                (reward + self.gamma * np.max(self.Q(new_state)) - self.Q(state, action))

    def create_stating_states(self):
        existing_starting_states = [self.start_state]

        map_copy = copy.deepcopy(self.map)
        for i in range(len(map_copy)):
            for j in range(len(map_copy[i])):
                if map_copy[i][j] == 3 or map_copy[i][j] == 4:
                    map_copy[i][j] = 0

        filled_positions = []
        for i in range(len(map_copy)):
            for j in range(len(map_copy[i])):
                if map_copy[i][j] == 1 or map_copy[i][j] == 2:
                    filled_positions.append([i, j])

        for a in range(10):
            random.seed()

            temp_map = copy.deepcopy(map_copy)
            pos1_x = random.randint(1, len(temp_map) - 1)
            pos1_y = random.randint(1, len(temp_map) - 1)
            while [pos1_x, pos1_y] in filled_positions:
                pos1_x = random.randint(1, len(temp_map) - 1)
                pos1_y = random.randint(1, len(temp_map) - 1)
            filled_positions.append([pos1_x, pos1_y])  # Os shappys começam sempre em sitios diferentes
            pos2_x = random.randint(1, len(temp_map) - 1)
            pos2_y = random.randint(1, len(temp_map) - 1)
            while [pos2_x, pos2_y] in filled_positions:
                pos2_x = random.randint(1, len(temp_map) - 1)
                pos2_y = random.randint(1, len(temp_map) - 1)
            filled_positions.remove([pos1_x, pos1_y])

            temp_map[pos1_x][pos1_y] = 3
            temp_map[pos2_x][pos2_y] = 4

            temp_state = State(map=temp_map)
            already_exists = False
            for state in existing_starting_states:
                if self.compare_arrays(state.map, temp_state.map):
                    already_exists = True

            if not already_exists:
                existing_starting_states.append(temp_state)

        # for item in existing_starting_states:
        #     self.print_array(item.map)
        #     print()

        return existing_starting_states

    def create_policy(self):

        total_episodes = 100000

        # starting_states = self.create_stating_states()
        starting_states = [self.start_state]

        # TRAIN
        rewards = []
        for i_state in range(len(starting_states)):
            self.epsilon = self.max_epsilon
            for episode in range(total_episodes):
                self.current_state = starting_states[i_state]
                print("State ", i_state, " Episode ", episode)
                episode_rewards = []
                while True:
                    #self.print_array(self.current_state.map)
                    self.check_walls()

                    stop = True
                    for i in range(len(self.current_state.map)):
                        for j in range(len(self.current_state.map[i])):
                            if self.current_state.map[i][j] == 2:
                                stop = False
                    if stop:
                        break

                    actions = self.choose_actions(self.current_state)

                    new_state, reward = self.take_actions(self.current_state, actions)

                    self.learn(self.current_state, actions, reward, new_state)

                    episode_rewards.append(reward)

                    self.current_state = new_state

                if episode == 1000:
                    self.epsilon = 0.5
                elif episode == 3000:
                    self.epsilon = 0.3
                elif episode == 10000:
                    self.epsilon = 0.1
                elif episode == 40000:
                    self.epsilon = 0.01
                elif episode == 49000:
                    self.epsilon = 0

                rewards.append(np.mean(episode_rewards))

    def write_in_txt(self, policy_file):
        new_Q_table = []
        for line in self.Q_table:
            new_Q_table.append([line.map, self.Q(line)])
        with open(policy_file, "wb") as fp:  # Unpickling
            pickle.dump(new_Q_table, fp)
            fp.close()

    def get_numbered_state(self, state):
        equal = True
        while True:
            if len(self.states_numbered) == 0:
                self.states_numbered.append(np.asarray(state))
            else:
                for i in range(len(self.states_numbered)):
                    equal = True
                    for j in range(len(self.states_numbered[i])):
                        if not self.compare_arrays(state[j], self.states_numbered[i][j]):
                            equal = False
                    if equal:
                        return i
                self.states_numbered.append(np.asarray(state))

    def print_array(self, array):
        for line in array:
            print(line)

    def compare_arrays(self, array1, array2):
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                return False
        return True

    def check_walls(self):
        array =[self.current_state.map[0], self.current_state.map[len(self.current_state.map[0])-1]]
        for i in range(len(array)):
            for j in range(len(array[i])):
                if array[i][j] != 1:
                    return False

        for i in range(1, len(self.current_state.map[0])-1):
            if self.current_state.map[i][0] != 1 or self.current_state.map[i][len(self.current_state.map[0])-1] != 1:
                print()
                print()
                self.print_array(self.current_state)
                quit()

    def send_message(self, _from, _to, message):
        pass
