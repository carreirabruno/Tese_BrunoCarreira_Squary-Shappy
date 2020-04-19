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


class MDP_Centralized_policy_maker_oneDBoxes2(object):

    def __init__(self, terrain_matrix, policy_file):

        self.map = []
        for line in terrain_matrix:
            if 3 in line:
                self.map = np.array(line)

        random.seed()

        # Environment items
        self.WALL = 1
        self.BOX = 2
        self.SHAPPY1 = 3
        self.SHAPPY2 = 4
        self.BOTH_SHAPPYS = 7
        self.EMPTY = 0

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

        self.Q_table = dict()

        self.imprimir = False

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

    def take_actions(self, state, map, actions):
        old_first_shappy_pos = state[0]
        old_second_shappy_pos = state[1]

        def new_shappy_pos(map, action):

            if action == self.STAY_LEFT:
                first_shappy_pos = old_first_shappy_pos
                if map[old_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos - 1
            elif action == self.STAY_RIGHT:
                first_shappy_pos = old_first_shappy_pos
                if map[old_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos + 1

            elif action == self.LEFT_STAY:
                if map[old_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos - 1
                second_shappy_pos = old_second_shappy_pos
            elif action == self.LEFT_LEFT:
                if map[old_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos - 1
                if map[old_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos - 1
            elif action == self.LEFT_RIGHT:
                if map[old_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos - 1
                if map[old_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos + 1

            elif action == self.RIGHT_STAY:
                if map[old_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos + 1
                second_shappy_pos = old_second_shappy_pos
            elif action == self.RIGHT_LEFT:
                if map[old_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos + 1
                if map[old_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos - 1
            elif action == self.RIGHT_RIGHT:
                if map[old_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    first_shappy_pos = old_first_shappy_pos
                else:
                    first_shappy_pos = old_first_shappy_pos + 1
                if map[old_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    second_shappy_pos = old_second_shappy_pos
                else:
                    second_shappy_pos = old_second_shappy_pos + 1

            else:
                raise ValueError(f"Unknown action {action}")
            return first_shappy_pos, second_shappy_pos

        new_first_shappy_pos, new_second_shappy_pos = new_shappy_pos(map, actions)

        new_map = copy.deepcopy(map)

        new_reward = 0
        # # Joint Rewards
        # if map[new_first_shappy_pos] == self.BOX or map[new_second_shappy_pos] == self.BOX:
        #     new_reward += 10
        # else:
        #     if new_first_shappy_pos != old_first_shappy_pos:
        #         new_reward += -1
        #     if new_second_shappy_pos != old_second_shappy_pos:
        #         new_reward += -1
        if map[new_first_shappy_pos] == self.BOX:
            new_reward += 10
        if new_first_shappy_pos != old_first_shappy_pos:
            new_reward -= 1
        if map[new_second_shappy_pos] == self.BOX and new_first_shappy_pos != new_second_shappy_pos:
            new_reward += 10
        if new_second_shappy_pos != old_second_shappy_pos:
            new_reward -= 1


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

        new_state = []
        for i in range(len(new_map)):
            if new_map[i] == 7:
                new_state.append(i)
                new_state.append(i)
                break
            if new_map[i] == 3:
                new_state.append(i)
        for i in range(len(new_map)):
            if new_map[i] == 4:
                new_state.append(i)
        for i in range(len(new_map)):
            if new_map[i] == 2:
                new_state.append(i)

        # Criar as rewards
        # new_number_of_boxes = self.current_number_of_boxes(new_map)
        # new_reward = (self.number_boxes - new_number_of_boxes) * 10

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
            #filled_positions.append(pos1)  # Os shappys começam sempre em sitios diferentes
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

    def create_policy(self):

        total_episodes = 100000

#        starting_states, starting_maps = self.create_stating_states()
        starting_states = [self.start_state]
        starting_maps = [self.start_map]
        # TRAIN
        rewards = []
        for i_state in range(len(starting_states)):
            # print(starting_states[i_state], starting_maps[i_state])

            for episode in range(total_episodes):

                self.current_state = starting_states[i_state]
                self.current_map = starting_maps[i_state]

                print("State ", i_state, "/", len(starting_states)-1, " Episode ", episode, "/", total_episodes)

                episode_rewards = []

                while True:
                    if len(self.current_state) == 2:
                        break

                    self.number_boxes = self.current_number_of_boxes(self.current_map)

                    actions = self.choose_actions(self.current_state)

                    new_state, new_map, reward = self.take_actions(self.current_state, self.current_map, actions)

                    self.learn(self.current_state, actions, reward, new_state)

                    episode_rewards.append(reward)

                    self.current_state = new_state

                    self.current_map = new_map

                    #print(self.current_state, actions)

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

                if episode == int(total_episodes/12):
                    self.epsilon = 0.5
                    # print("                                        " , self.epsilon)
                elif episode == int(total_episodes/8):
                    self.epsilon = 0.3
                    # print("                                        " , self.epsilon)
                elif episode == int(total_episodes/5):
                    self.epsilon = 0.1
                    # print("                                        " , self.epsilon)
                elif episode == int(total_episodes - (total_episodes/10)):
                    self.epsilon = 0.01
                    # print("                                        ", self.epsilon)

                rewards.append(np.mean(episode_rewards))

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