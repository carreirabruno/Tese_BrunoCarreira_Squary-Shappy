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
        return isinstance(other, State)

    def __hash__(self):
        return hash(str(self.map))

    def __str__(self):
        return f"State(map={self.map})"


class MDP_Centralized_policy_maker_oneDBoxes2(object):

    def __init__(self, terrain_matrix, policy_file):

        self.map = []
        for line in terrain_matrix:
            if 2 in line:
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

        self.Q_table = dict()

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
        if state.map[new_first_shappy_pos] == self.BOX:
            new_reward += 10
        else:
            new_reward += 0
        if state.map[new_second_shappy_pos] == self.BOX:
            new_reward += 10
        else:
            new_reward += 0

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

        return State(map=new_map), new_reward

    def learn(self, state, action, reward, new_state):
        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        self.Q(state)[action] = self.Q(state, action) + self.learning_rate * \
                                (reward + self.gamma * np.max(self.Q(new_state)) - self.Q(state, action))

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

        total_episodes = 5000

        #starting_states = self.create_stating_states()
        starting_states = [self.start_state]
        # TRAIN
        rewards = []
        for i_state in range(len(starting_states)):
            for episode in range(total_episodes):

                self.current_state = starting_states[i_state]

                print("State ", i_state, " Episode ", episode)

                episode_rewards = []

                while True:
                    if 2 not in self.current_state.map:
                        break

                    actions = self.choose_actions(self.current_state)

                    new_state, reward = self.take_actions(self.current_state, actions)

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

                rewards.append(np.mean(episode_rewards))


    def write_in_txt(self, policy_file):
        new_Q_table = []
        for line in self.Q_table:
            new_Q_table.append([line.map, self.Q(line)])
        with open(policy_file, "wb") as fp:  # Unpickling
            pickle.dump(new_Q_table, fp)
            fp.close()
