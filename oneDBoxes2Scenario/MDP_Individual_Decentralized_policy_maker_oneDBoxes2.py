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

class MDP_Individual_Decentralized_policy_maker_oneDBoxes2(object):

    def __init__(self, terrain_matrix, policy_file):

        self.map = []
        for line in terrain_matrix:
            if 3 in line:
                self.map = np.array(line)

        random.seed()

        # Environment items
        self.WALL = 1
        self.BOX = 2
        self.ME_SHAPPY = 3
        self.PEER_SHAPPY = 4
        self.BOTH_SHAPPYS = 7
        self.EMPTY = 0

        # Actions
        self.STAY = 0
        self.LEFT = 1
        self.RIGHT = 2

        self.ACTIONS = [self.STAY, self.LEFT, self.RIGHT]
        self.n_actions = len(self.ACTIONS)

        self.shappy3_pos = -1
        self.shappy4_pos = -1
        for i in range(len(self.map)):
            if self.map[i] == 7:
                self.shappy3_pos = i
                self.shappy4_pos = i
            elif self.map[i] == 3:
                self.shappy3_pos = i
            elif self.map[i] == 4:
                self.shappy4_pos = i

        boxes = []
        for i in range(len(self.map)):
            if self.map[i] == 2:
                boxes.append(i)

        self.start_map = self.map
        self.start_state = []
        for i in range(len(self.start_map)):
            if int(self.start_map[i]) == 3:
                self.start_state.append(i)
            if int(self.start_map[i]) == 4:
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
                if map[old_shappy3_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = old_shappy3_pos - 1
            elif action3 == self.RIGHT:
                if map[old_shappy3_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_shappy3_pos = old_shappy3_pos
                else:
                    new_shappy3_pos = old_shappy3_pos + 1
            else:
                raise ValueError(f"Unknown action {action3}")

            new_shappy4_pos = -1
            if action4 == self.STAY:
                new_shappy4_pos = old_shappy4_pos
            elif action4 == self.LEFT:
                if map[old_shappy4_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = old_shappy4_pos - 1
            elif action4 == self.RIGHT:
                if map[old_shappy4_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_shappy4_pos = old_shappy4_pos
                else:
                    new_shappy4_pos = old_shappy4_pos + 1
            else:
                raise ValueError(f"Unknown action {action4}")

            return new_shappy3_pos, new_shappy4_pos

        new_reward = 0
        new_shappy3_pos, new_shappy4_pos = get_new_shappy_position(map, action3, action4)

        new_map = copy.deepcopy(map)

        # # Criar as rewards
        # new_reward3 = 0
        # new_reward4 = 0
        # if map[new_shappy3_pos] == self.BOX:
        #     new_reward3 = 10
        # else:
        #     new_reward3 = -1
        # if map[new_shappy4_pos] == self.BOX:
        #     new_reward4 = 10
        # else:
        #     new_reward4 = -1


        # Só mexe o 1 - Mesmo sitio -> Separados
        if old_shappy4_pos == new_shappy4_pos and old_shappy3_pos == old_shappy4_pos \
                and new_shappy3_pos != new_shappy4_pos:
            new_map[old_shappy3_pos] = self.PEER_SHAPPY
            new_map[new_shappy3_pos] = self.ME_SHAPPY

        # Só mexe o 1 - Separados -> Mesmo sitio
        if old_shappy4_pos == new_shappy4_pos and old_shappy3_pos != old_shappy4_pos \
                and new_shappy3_pos == new_shappy4_pos:
            new_map[old_shappy3_pos] = self.EMPTY
            new_map[new_shappy3_pos] = self.BOTH_SHAPPYS

        # Só mexe o 1 - Separados -> Separados
        if old_shappy4_pos == new_shappy4_pos and old_shappy3_pos != old_shappy4_pos \
                and new_shappy3_pos != new_shappy4_pos:
            new_map[old_shappy3_pos] = self.EMPTY
            new_map[new_shappy3_pos] = self.ME_SHAPPY

        # Só mexe o 2 - Mesmo sitio -> Separados
        elif old_shappy3_pos == new_shappy3_pos and old_shappy3_pos == old_shappy4_pos \
                and new_shappy3_pos != new_shappy4_pos:
            new_map[old_shappy4_pos] = self.ME_SHAPPY
            new_map[new_shappy4_pos] = self.PEER_SHAPPY

        # Só mexe o 2 - Separados -> Mesmo sitio
        elif old_shappy3_pos == new_shappy3_pos and old_shappy3_pos != old_shappy4_pos \
                and new_shappy3_pos == new_shappy4_pos:
            new_map[old_shappy4_pos] = self.EMPTY
            new_map[new_shappy4_pos] = self.BOTH_SHAPPYS

        # Só mexe o 2 - Separados -> Separados
        elif old_shappy3_pos == new_shappy3_pos and old_shappy3_pos != old_shappy4_pos \
                and new_shappy3_pos != new_shappy4_pos:
            new_map[old_shappy4_pos] = self.EMPTY
            new_map[new_shappy4_pos] = self.PEER_SHAPPY

        # Mexem os dois - Mesmo sitio -> Mesmo sitio
        elif old_shappy3_pos == old_shappy4_pos and new_shappy3_pos == new_shappy4_pos:
            new_map[old_shappy3_pos] = self.EMPTY
            new_map[new_shappy3_pos] = self.BOTH_SHAPPYS

        # Mexem os dois - Separados -> Mesmo sitio
        elif old_shappy3_pos != old_shappy4_pos and new_shappy3_pos == new_shappy4_pos:
            new_map[old_shappy3_pos] = self.EMPTY
            new_map[old_shappy4_pos] = self.EMPTY
            new_map[new_shappy3_pos] = self.BOTH_SHAPPYS

        # Mexem os dois - Mesmo sitio -> Separados
        elif old_shappy3_pos == old_shappy4_pos and new_shappy3_pos != new_shappy4_pos:
            new_map[old_shappy3_pos] = self.EMPTY
            new_map[new_shappy3_pos] = self.ME_SHAPPY
            new_map[new_shappy4_pos] = self.PEER_SHAPPY

        # Mexem os dois - Separados -> Separados
        elif old_shappy3_pos != old_shappy4_pos and new_shappy3_pos != new_shappy4_pos:
            new_map[old_shappy3_pos] = self.EMPTY
            new_map[old_shappy4_pos] = self.EMPTY
            new_map[new_shappy3_pos] = self.ME_SHAPPY
            new_map[new_shappy4_pos] = self.PEER_SHAPPY

        new_state = []
        for i in range(len(new_map)):
            if new_map[i] == 7:
                new_state.append(i)
                new_state.append(i)
                break
            if new_map[i] == 3:
                new_state.append(i)
                break
        for i in range(len(new_map)):
            if new_map[i] == 4:
                new_state.append(i)
                break
        for i in range(len(new_map)):
            if new_map[i] == 2:
                new_state.append(i)

        new_shappy3_state = copy.copy(new_state)
        new_shappy3_state.remove(new_shappy3_state[1])
        new_shappy4_state = copy.copy(new_state)
        new_shappy4_state.remove(new_shappy4_state[0])

        # Criar as rewards
        new_number_of_boxes = self.current_number_of_boxes(new_map)
        if self.number_boxes != new_number_of_boxes:
            new_reward = (self.number_boxes - new_number_of_boxes) * 10
            new_reward3 = new_reward
            new_reward4 = new_reward
        else:
            new_reward3 = -1
            new_reward4 = -1

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

        # map_copy = copy.deepcopy(self.map)
        # if 3 in map_copy:
        #     map_copy = np.where(map_copy == 3, 0, map_copy)
        #
        # filled_positions = []
        # boxes_positions_temp = []
        # for i in range(len(map_copy)):
        #     if map_copy[i] == 1:
        #         filled_positions.append(i)
        #     if map_copy[i] == 2:
        #         boxes_positions_temp.append(i)
        #
        # boxes_positions = []
        # for i in range(1, len(boxes_positions_temp) + 1):
        #     temp_comb = combinations(boxes_positions_temp, i)
        #     for item in temp_comb:
        #         temp_array = []
        #         for j in range(len(item)):
        #             temp_array.append(item[j])
        #         boxes_positions.append(temp_array)
        #
        # different_boxes_map = [map_copy]
        # for pos in boxes_positions:
        #     temp_map = copy.deepcopy(map_copy)
        #     for ind_pos in pos:
        #         temp_map[ind_pos] = 0
        #     different_boxes_map.append(temp_map)
        #
        # for ind_map in different_boxes_map:
        #     for a in range(100):
        #         random.seed()
        #         temp_map = copy.deepcopy(ind_map)
        #         pos = random.randint(1, len(temp_map) - 1)
        #         while pos in filled_positions:
        #             pos = random.randint(1, len(temp_map) - 1)
        #
        #         temp_map[pos] = 3
        #
        #         temp_state = []
        #
        #         for i in range(len(temp_map)):
        #             if temp_map[i] == 3:
        #                 temp_state.append(i)
        #         for i in range(len(temp_map)):
        #             if temp_map[i] == 2:
        #                 temp_state.append(i)
        #
        #         already_exists = False
        #         for state in existing_starting_states:
        #             equal = True
        #             for i in range(len(state)):
        #                 if len(temp_state) != len(state) or temp_state[i] != state[i]:
        #                     equal = False
        #             if equal:
        #                 already_exists = True
        #
        #         if not already_exists:
        #             existing_starting_maps.append(temp_map)
        #             existing_starting_states.append(temp_state)

        # second_map = copy.copy(self.start_map)
        # second_map[self.shappy3_pos] = 4
        # second_map[self.shappy4_pos] = 3
        # second_state = copy.copy(self.start_state)
        # second_state[0] = self.shappy4_pos
        # second_state[1] = self.shappy3_pos
        #
        # existing_starting_states.append(second_state)
        # existing_starting_maps.append(second_map)

        return existing_starting_states, existing_starting_maps

    def create_policy(self):

        total_episodes = 10000

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

                print("State ", i_state, "/", len(starting_states), " Episode ", episode, "/", total_episodes)

                episode_rewards = []

                while True:
                    if len(shappy3_state) == 1 and len(shappy4_state) == 1:
                        break

                    self.number_boxes = self.current_number_of_boxes(self.current_map)

                    action3 = self.choose_actions(self.current_state)

                    action4 = self.choose_actions2(self.current_state)

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

                if episode == 1000:
                    self.epsilon = 0.5
                elif episode == 2500:
                     self.epsilon = 0.3
                elif episode == 5000:
                     self.epsilon = 0.1
                # elif episode == 8000:
                #     self.epsilon = 0.01

                # if episode == int(total_episodes / 12):
                #     self.epsilon = 0.5
                #     # print("                                        " , self.epsilon)
                # elif episode == int(total_episodes / 8):
                #     self.epsilon = 0.3
                #     # print("                                        " , self.epsilon)
                # elif episode == int(total_episodes / 5):
                #     self.epsilon = 0.1
                #     # print("                                        " , self.epsilon)
                # elif episode == int(total_episodes - (total_episodes / 10)):
                #     self.epsilon = 0.01
                #     # print("                                        ", self.epsilon)
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
