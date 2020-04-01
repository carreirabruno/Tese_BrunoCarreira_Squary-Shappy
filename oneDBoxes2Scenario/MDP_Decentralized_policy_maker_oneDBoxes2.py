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

class MDP_Decentralized_policy_maker_oneDBoxes2(object):

    def __init__(self, terrain_matrix, policy_file):

        self.map = []
        for line in terrain_matrix:
            if 3 in line:
                self.map = np.array(line)

        random.seed()

        # Environment items
        self.WALL = 1
        self.BOX = 2
        self.SHAPPY = 3
        self.EMPTY = 0

        # Actions

        self.STAY = 0
        self.LEFT = 1
        self.RIGHT = 2

        self.ACTIONS = [self.STAY, self.LEFT, self.RIGHT]
        self.n_actions = len(self.ACTIONS)

        self.shappy_pos = -1
        for i in range(len(self.map)):

            if self.map[i] == 7:
                self.shappy_pos = i
            elif self.map[i] == 3:
                self.shappy_pos = i
            elif self.map[i] == 4:
                self.map[i] = 0

        boxes = []
        for i in range(len(self.map)):
            if self.map[i] == 2:
                boxes.append(i)

        self.start_map = self.map
        self.start_state = []
        for i in range(len(self.start_map)):
            if int(self.start_map[i]) == 3:
                self.start_state.append(i)
        for i in range(len(self.start_map)):
            if int(self.start_map[i]) == 2:
                self.start_state.append(i)

        self.current_state = []
        self.current_map = []

        self.gamma = 0.9
        self.learning_rate = 0.1  # alpha

        self.max_epsilon = 0.9
        self.min_epsilon = 0.01
        self.epsilon = self.max_epsilon
        self.decay_rate = 0.001

        self.Q_table = dict()

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

    def take_actions(self, state, map, actions):
        old_shappy_pos = state[0]

        def get_new_shappy_position(map, action):
            if action == self.STAY:
                new_shappy_pos = old_shappy_pos
            elif action == self.LEFT:
                if map[old_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_shappy_pos = old_shappy_pos
                else:
                    new_shappy_pos = old_shappy_pos - 1
            elif action == self.RIGHT:
                if map[old_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_shappy_pos = old_shappy_pos
                else:
                    new_shappy_pos = old_shappy_pos + 1
            else:
                raise ValueError(f"Unknown action {action}")
            return new_shappy_pos

        new_reward = 0
        new_shappy_pos = get_new_shappy_position(map, actions)

        new_map = copy.deepcopy(map)

        # Criar as rewards
        if map[new_shappy_pos] == self.BOX:
            new_reward += 10
        else:
            new_reward += 0
        if map[new_shappy_pos] == self.BOX:
            new_reward += 10
        else:
            new_reward += 0

        new_map[old_shappy_pos] = self.EMPTY
        new_map[new_shappy_pos] = self.SHAPPY

        new_state = []
        for i in range(len(new_map)):
            if new_map[i] == 3:
                new_state.append(i)
        for i in range(len(new_map)):
            if new_map[i] == 2:
                new_state.append(i)

        return new_state, new_map, new_reward

    def learn(self, state, action, reward, new_state):
        state_obj = State(state)
        new_state_obj = State(new_state)

        self.Q(state_obj)[action] = self.Q(state_obj, action) + self.learning_rate * \
                                (reward + self.gamma * np.max(self.Q(new_state_obj)) - self.Q(state_obj, action))

    def create_stating_states(self):
        existing_starting_states = [self.start_state]
        existing_starting_maps = [self.start_map]

        map_copy = copy.deepcopy(self.map)
        if 3 in map_copy:
            map_copy = np.where(map_copy == 3, 0, map_copy)

        filled_positions = []
        boxes_positions_temp = []
        for i in range(len(map_copy)):
            if map_copy[i] == 1:
                filled_positions.append(i)
            if map_copy[i] == 2:
                boxes_positions_temp.append(i)

        boxes_positions = [boxes_positions_temp, [boxes_positions_temp[0], boxes_positions_temp[1]],
                           [boxes_positions_temp[0], boxes_positions_temp[2]], [boxes_positions_temp[1], boxes_positions_temp[2]],
                           [boxes_positions_temp[0]], [boxes_positions_temp[1]], [boxes_positions_temp[2]]]

        different_boxes_map = [map_copy]
        for pos in boxes_positions:
            temp_map = copy.deepcopy(map_copy)
            for ind_pos in pos:
                temp_map[ind_pos] = 0
            different_boxes_map.append(temp_map)

        for ind_map in different_boxes_map:
            for a in range(100):
                random.seed()
                temp_map = copy.deepcopy(ind_map)
                pos = random.randint(1, len(temp_map) - 1)
                while pos in filled_positions:
                    pos = random.randint(1, len(temp_map) - 1)

                temp_map[pos] = 3

                temp_state = []

                for i in range(len(temp_map)):
                    if temp_map[i] == 3:
                        temp_state.append(i)
                for i in range(len(temp_map)):
                    if temp_map[i] == 2:
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

    def create_policy(self):

        total_episodes = 1000

        starting_states, starting_maps = self.create_stating_states()
        #starting_states = [self.start_state]
        # second_state = copy.deepcopy(self.start_state)
        # second_state[0] = 7
        # second_map = copy.deepcopy(self.start_map)
        # second_map[5] = 0
        # second_map[7] = 3
        # starting_states = [self.start_state, second_state]
        # starting_maps = [self.start_map, second_map]

        # TRAIN
        rewards = []
        for i_state in range(len(starting_states)):
            for episode in range(total_episodes):
                self.current_state = starting_states[i_state]
                self.current_map = starting_maps[i_state]

                print("State ", i_state, "/", len(starting_states)-1, " Episode ", episode)

                episode_rewards = []

                while True:
                    if len(self.current_state) == 1:
                        break

                    actions = self.choose_actions(self.current_state)

                    new_state, new_map, reward = self.take_actions(self.current_state, self.current_map, actions)

                    self.learn(self.current_state, actions, reward, new_state)

                    episode_rewards.append(reward)

                    self.current_state = new_state
                    self.current_map = new_map

                if episode == 100:
                    self.epsilon = 0.5
                elif episode == 300:
                     self.epsilon = 0.3
                elif episode == 500:
                     self.epsilon = 0.1
                elif episode == 900:
                    self.epsilon = 0.01

                # if episode == 500:
                #     self.epsilon = 0.5
                # elif episode == 900:
                #      self.epsilon = 0.3
                # elif episode == 1500:
                #      self.epsilon = 0.1
                # elif episode == 2800:
                #     self.epsilon = 0.01

                rewards.append(np.mean(episode_rewards))

    def write_in_txt(self, policy_file):
        new_Q_table = []
        for line in self.Q_table:
            new_Q_table.append([line.state, self.Q(line)])
        with open(policy_file, "wb") as fp:  # Unpickling
            pickle.dump(new_Q_table, fp)
            fp.close()
