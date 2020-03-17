import numpy as np
import random
import copy
import math


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


class MDP_Collaborator_oneDBoxes(object):

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
        n_actions = len(self.ACTIONS)

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

        self.start_state = State(map=self.map)

        self.gamma = 0.9
        self.learning_rate = 0.1  # alpha

        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.epsilon = self.max_epsilon
        self.decay_rate = 0.001

        # n_states = len(self.map)  # * n_actions * 4       #4 é o numero de self.BOXes

        # Q_table = np.zeros((n_states, n_actions))
        self.Q_table = dict()

        self.type_of_policy = policy_file.replace("oneDBoxes_MDP_", '')
        self.type_of_policy = self.type_of_policy.replace("_policy.txt", '')

        self.create_policy()
        self.write_in_txt(policy_file)

    def detect_shappys_pos(self, non_col_shappys, col_shappys):

        if len(non_col_shappys) == 0 and len(col_shappys) == 0:
            raise Exception("No shappys in the map")
        elif len(non_col_shappys) == 0 and len(col_shappys) == 1:
            return col_shappys[0], math.inf
        elif len(non_col_shappys) == 0 and len(col_shappys) == 2:
            return col_shappys[0], col_shappys[1]
        elif len(non_col_shappys) == 1 and len(col_shappys) == 0:
            return non_col_shappys[0], math.inf
        elif len(non_col_shappys) == 2 and len(col_shappys) == 0:
            return non_col_shappys[0], non_col_shappys[1]
        elif len(non_col_shappys) == 1 and len(col_shappys) == 1:
            if non_col_shappys[0] < col_shappys[0]:
                return non_col_shappys[0], col_shappys[0]
            else:
                return col_shappys[0], non_col_shappys[0]

    def Q(self, state, action=None):

        if state not in self.Q_table:
            self.Q_table[state] = np.zeros(len(self.ACTIONS))

        if action is None:
            return self.Q_table[state]

        return self.Q_table[state][action]

    def choose_actions(self, state):
        random.seed()
        if random.random() < self.epsilon:  # exploration
            return random.randint(0, len(self.ACTIONS) - 1)
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
                new_reward += 100
            else:
                new_reward -= 1
            if state.map[new_second_shappy_pos] == self.BOX:
                new_reward += 100
            else:
                new_reward -= 1
        elif self.type_of_policy == "collaborative":
            if state.map[new_first_shappy_pos] == self.BOX:
                new_reward += 100
            else:
                new_reward -= 1
            if state.map[new_second_shappy_pos] == self.BOX:
                new_reward += 100
            else:
                new_reward -= 1
        elif self.type_of_policy == "non_collaborative":
            first_shappy_closest_box = self.get_closest_box(state, old_first_shappy_pos)
            second_shappy_closest_box = self.get_closest_box(state, old_second_shappy_pos)

            if state.map[new_first_shappy_pos] == self.BOX:
                new_reward += 100
            elif abs(first_shappy_closest_box - new_first_shappy_pos) < \
                    abs(first_shappy_closest_box - old_first_shappy_pos):  # o 1 shappy está a aproximar-se
                new_reward += 100
            elif abs(first_shappy_closest_box - new_first_shappy_pos) >= \
                    abs(first_shappy_closest_box - old_first_shappy_pos):  # o 1 shappy está a afastar-se
                new_reward -= 50
            else:
                new_reward -= 1
            if state.map[new_second_shappy_pos] == self.BOX:
                new_reward += 100
            elif abs(second_shappy_closest_box - new_second_shappy_pos) < \
                    abs(second_shappy_closest_box - old_second_shappy_pos):  # o 2 shappy está a aproximar-se
                new_reward += 100
            elif abs(second_shappy_closest_box - new_second_shappy_pos) >= \
                    abs(second_shappy_closest_box - old_second_shappy_pos):  # o 2 shappy está a afastar-se
                new_reward -= 50
            else:
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
        # Devia aqui alterar a tabela das transições P(state, action, new state)
        # Devia aqui alterar a tabela das rewards para cada estado R[state]
        # Q[si, a] = Q[si, a] + alpha * (r + gamma * max(Q[nsi, :]) - Q[si, a])
        # P[a, si, nsi] += 1
        # R[si] = r
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

        total_episodes = 3000  # tenho que aumentar isto para 100000 :(

        #starting_states = self.create_stating_states()
        starting_states = [self.start_state]
        # TRAIN
        rewards = []
        for i_state in range(len(starting_states)):
            for episode in range(total_episodes):

                state = starting_states[i_state]
                #print("State ", i_state, state, " Episode ", episode)
                print(episode)
                #print(self.epsilon)
                episode_rewards = []

                while True:
                    if 2 not in state.map:
                        break

                    actions = self.choose_actions(state)

                    new_state, reward = self.take_actions(state, actions)

                    # print(new_state, " ",actions)

                    self.learn(state, actions, reward, new_state)

                    episode_rewards.append(reward)

                    state = new_state

                    self.epsilon = self.epsilon - self.decay_rate
                    if self.epsilon < self.min_epsilon:
                        self.epsilon = self.min_epsilon

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
        # RESULTS
        f = open(policy_file, "w+")
        for line in self.Q_table:
            # print(line, "   ", np.argmax(self.Q(line)), "   ", self.Q(line))
            f.write("%s && %s && %s \r" % (line, np.argmax(self.Q(line)), self.Q(line)))
        f.write("final")
        f.close()

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
