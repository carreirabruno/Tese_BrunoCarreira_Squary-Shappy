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


class MDP_Decentralized_policy_maker_oneDBoxes(object):

    def __init__(self, terrain_matrix, policy_file):

        self.map = []
        for line in terrain_matrix:
            if 2 in line:
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

        self.start_state = State(map=self.map)
        self.current_state = []

        self.gamma = 0.9
        self.learning_rate = 0.1  # alpha

        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.epsilon = self.max_epsilon
        self.decay_rate = 0.001

        self.n_states = len(self.map) * len(boxes)
        self.n_states *= self.n_states

        self.Q_table = dict()

        self.states_numbered = []
        self.P_table = np.zeros((self.n_actions, self.n_states, self.n_states))

        self.type_of_policy = policy_file.replace("oneDBoxes_MDP_", '')
        self.type_of_policy = self.type_of_policy.replace("_policy2.pickle", '')
        self.type_of_policy = self.type_of_policy.replace("_policy3.pickle", '')
        self.type_of_policy = self.type_of_policy.replace("_policy2_individual.pickle", '')
        self.type_of_policy = self.type_of_policy.replace("_policy3_individual.pickle", '')

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
        old_shappy_pos = 0
        for i in range(len(state.map)):
            if state.map[i] == 7:
                old_shappy_pos = i
                break
            elif state.map[i] == self.SHAPPY:
                old_shappy_pos = i

        def get_new_shappy_position(state, action):
            if action == self.STAY:
                new_shappy_pos = old_shappy_pos
            elif action == self.LEFT:
                if state.map[old_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_shappy_pos = old_shappy_pos
                else:
                    new_shappy_pos = old_shappy_pos - 1
            elif action == self.RIGHT:
                if state.map[old_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_shappy_pos = old_shappy_pos
                else:
                    new_shappy_pos = old_shappy_pos + 1
            else:
                raise ValueError(f"Unknown action {action}")
            return new_shappy_pos

        new_reward = 0
        new_shappy_pos = get_new_shappy_position(state, actions)

        new_map = copy.deepcopy(state.map)
        # Criar as rewards
        if self.type_of_policy == "base":
            if state.map[new_shappy_pos] == self.BOX:
                new_reward += 10
            else:
                new_reward += 0
            if state.map[new_shappy_pos] == self.BOX:
                new_reward += 10
            else:
                new_reward += 0

            new_map[old_shappy_pos] = self.EMPTY
            new_map[new_shappy_pos] = self.SHAPPY


        return State(map=new_map), new_reward

    def learn(self, state, action, reward, new_state):
        self.Q(state)[action] = self.Q(state, action) + self.learning_rate * \
                                (reward + self.gamma * np.max(self.Q(new_state)) - self.Q(state, action))

        state_number = self.get_numbered_state(state.map)
        new_state_number = self.get_numbered_state(new_state.map)
        self.P_table[action, state_number, new_state_number] += 1

        # Devia aqui alterar a tabela das rewards para cada estado R[state]

    def create_stating_states(self):
        existing_starting_states = [self.start_state]

        map_copy = copy.deepcopy(self.map)
        if 3 in map_copy:
            map_copy = np.where(map_copy == 3, 0, map_copy)

        filled_positions = []
        boxes_positions = []
        for i in range(len(map_copy)):
            if map_copy[i] == 1:
                filled_positions.append(i)
            if map_copy[i] == 2:
                boxes_positions.append([i])

        boxes_positions.append([boxes_positions[0][0],boxes_positions[1][0]])
        boxes_positions.append([boxes_positions[0][0], boxes_positions[2][0]])
        boxes_positions.append([boxes_positions[1][0], boxes_positions[2][0]])
        different_boxes_map = [map_copy]
        for pos in boxes_positions:
            temp_map = copy.deepcopy(map_copy)
            for ind_pos in pos:
                temp_map[pos] = 0
            different_boxes_map.append(temp_map)

        for ind_map in different_boxes_map:
            for a in range(100):
                random.seed()
                temp_map = copy.deepcopy(ind_map)
                pos = random.randint(1, len(temp_map) - 1)
                while pos in filled_positions:
                    pos = random.randint(1, len(temp_map) - 1)

                temp_map[pos] = 3

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

        total_episodes = 1000

        starting_states = self.create_stating_states()
        #starting_states = [self.start_state]
        # TRAIN
        rewards = []
        for i_state in range(len(starting_states)):
            for episode in range(total_episodes):

                self.current_state = starting_states[i_state]

                print("State ", i_state, "/", len(starting_states)-1, " Episode ", episode)

                episode_rewards = []

                while True:
                    if 2 not in self.current_state.map:
                        break

                    #print(self.current_state)

                    actions = self.choose_actions(self.current_state)

                    new_state, reward = self.take_actions(self.current_state, actions)

                    self.learn(self.current_state, actions, reward, new_state)

                    episode_rewards.append(reward)

                    self.current_state = new_state

                if episode == 100:
                    self.epsilon = 0.5
                elif episode == 300:
                     self.epsilon = 0.3
                elif episode == 500:
                     self.epsilon = 0.1
                elif episode == 900:
                    self.epsilon = 0.01

                rewards.append(np.mean(episode_rewards))

    def write_in_txt(self, policy_file):
        new_Q_table = []
        for line in self.Q_table:
            new_Q_table.append([line.map, self.Q(line)])
        with open(policy_file, "wb") as fp:  # Unpickling
            pickle.dump((new_Q_table, self.states_numbered, self.P_table), fp)
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
                        if state[j] != self.states_numbered[i][j]:
                            equal = False
                            break
                    if equal:
                        return i
                if not equal:
                    self.states_numbered.append(np.asarray(state))