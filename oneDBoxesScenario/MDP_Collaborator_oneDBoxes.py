import numpy as np
import random
import copy
import math


class State:

    def __init__(self, map, first_shappy_pos, second_shappy_pos):
        self.map = map
        self.first_shappy_pos = first_shappy_pos
        self.second_shappy_pos = second_shappy_pos

    def __eq__(self, other):
        return isinstance(other,
                          State)  # and self.map == other.map and self.first_shappy_pos == other.first_shappy_pos \
        # and self.second_shappy_pos == other.second_shappy_pos

    def __hash__(self):
        return hash(str(self.map) + str(self.first_shappy_pos) + str(self.second_shappy_pos))

    def __str__(self):
        return f"State(map={self.map}, first_shappy_pos={self.first_shappy_pos}, " \
               f"second_shappy_pos={self.second_shappy_pos})"


class MDP_Collaborator_oneDBoxes(object):

    def __init__(self, terrain_matrix, policy_file):
        self.map = []
        for line in terrain_matrix:
            if 3 in line:                               #para criar a politica centralizada, trata ambos os shappys como collaborative
                line = np.where(line==3, 4, line)
            if 2 in line:
                self.map = np.array(line)


        random.seed(42)

        # Environment items
        self.WALL = 1
        self.BOX = 2
        # NON_COL_SHAPPY = 3
        self.SHAPPY = 4
        self.EMPTY = 0

        #map = np.array(
            #[self.WALL, self.BOX, self.EMPTY, self.EMPTY, self.EMPTY, self.SHAPPY, self.EMPTY, self.EMPTY, self.BOX, self.EMPTY, self.BOX, self.SHAPPY, self.EMPTY, self.BOX, self.WALL])

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
        shappys = np.where(self.map == 4)

        # first_shappy_pos, second_shappy_pos = detect_shappys_pos(non_col_shappys[0], col_shappys[0])

        self.start_state = State(map=self.map, first_shappy_pos=shappys[0][0], second_shappy_pos=shappys[0][1])

        self.gamma = 0.9
        self.learning_rate = 0.1  # alpha

        n_states = len(self.map)  # * n_actions * 4       #4 é o numero de self.BOXes

        # Q_table = np.zeros((n_states, n_actions))
        self.Q_table = dict()

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

        if random.random() < 0.1:  # exploration
            return random.randint(0, len(self.ACTIONS) - 1)
        else:  # exploitation
            return np.argmax(self.Q(state))

    def take_actions(self, state, actions):

        def new_shappy_pos(state, action):
            new_first_shappy_pos = copy.deepcopy(state.first_shappy_pos)
            new_second_shappy_pos = copy.deepcopy(state.second_shappy_pos)

            #if action == self.STAY_STAY:
            #    new_first_shappy_pos = new_first_shappy_pos
            #    new_second_shappy_pos = new_second_shappy_pos
            if action == self.STAY_LEFT:
                new_first_shappy_pos = new_first_shappy_pos
                if state.map[new_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_second_shappy_pos = new_second_shappy_pos
                else:
                    new_second_shappy_pos = max(0, new_second_shappy_pos - 1)
            elif action == self.STAY_RIGHT:
                new_first_shappy_pos = new_first_shappy_pos
                if state.map[new_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_second_shappy_pos = new_second_shappy_pos
                else:
                    new_second_shappy_pos = min(len(state.map) - 1, new_second_shappy_pos + 1)

            elif action == self.LEFT_STAY:
                if state.map[new_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_first_shappy_pos = new_first_shappy_pos
                else:
                    new_first_shappy_pos = max(0, new_first_shappy_pos - 1)
                new_second_shappy_pos = new_second_shappy_pos
            elif action == self.LEFT_LEFT:
                if state.map[new_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_first_shappy_pos = new_first_shappy_pos
                else:
                    new_first_shappy_pos = max(0, new_first_shappy_pos - 1)
                if state.map[new_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_second_shappy_pos = new_second_shappy_pos
                else:
                    new_second_shappy_pos = max(0, new_second_shappy_pos - 1)
            elif action == self.LEFT_RIGHT:
                if state.map[new_first_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_first_shappy_pos = new_first_shappy_pos
                else:
                    new_first_shappy_pos = max(0, new_first_shappy_pos - 1)
                if state.map[new_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_second_shappy_pos = new_second_shappy_pos
                else:
                    new_second_shappy_pos = min(len(state.map) - 1, new_second_shappy_pos + 1)

            elif action == self.RIGHT_STAY:
                if state.map[new_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_first_shappy_pos = new_first_shappy_pos
                else:
                    new_first_shappy_pos = min(len(state.map) - 1, new_first_shappy_pos + 1)
                new_second_shappy_pos = new_second_shappy_pos
            elif action == self.RIGHT_LEFT:
                if state.map[new_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_first_shappy_pos = new_first_shappy_pos
                else:
                    new_first_shappy_pos = min(len(state.map) - 1, new_first_shappy_pos + 1)
                if state.map[new_second_shappy_pos - 1] == self.WALL:  # colidiu com uma self.WALL
                    new_second_shappy_pos = new_second_shappy_pos
                else:
                    new_second_shappy_pos = max(0, new_second_shappy_pos - 1)
            elif action == self.RIGHT_RIGHT:
                if state.map[new_first_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_first_shappy_pos = new_first_shappy_pos
                else:
                    new_first_shappy_pos = min(len(state.map) - 1, new_first_shappy_pos + 1)
                if state.map[new_second_shappy_pos + 1] == self.WALL:  # colidiu com uma self.WALL
                    new_second_shappy_pos = new_second_shappy_pos
                else:
                    new_second_shappy_pos = min(len(state.map) - 1, new_second_shappy_pos + 1)

            else:
                raise ValueError(f"Unknown action {action}")
            return new_first_shappy_pos, new_second_shappy_pos

        new_first_pos, new_second_pos = new_shappy_pos(state, actions)
        first_map_item = state.map[new_first_pos]
        second_map_item = state.map[new_second_pos]

        new_map = copy.deepcopy(state.map)
        if first_map_item == self.BOX:
            new_reward = 100
            old_pos = state.first_shappy_pos
            new_map[old_pos] = self.EMPTY
            new_map[new_first_pos] = self.SHAPPY
        elif first_map_item == self.EMPTY:
            new_reward = -1
            old_pos = state.first_shappy_pos
            new_map[old_pos] = self.EMPTY
            new_map[new_first_pos] = self.SHAPPY
        elif first_map_item == self.SHAPPY:
            new_reward = -1
            old_pos = state.first_shappy_pos
            new_map[old_pos] = self.EMPTY
            new_map[new_first_pos] = self.SHAPPY

        if second_map_item == self.BOX:
            new_reward = 100
            old_pos = state.second_shappy_pos
            new_map[old_pos] = self.EMPTY
            new_map[new_second_pos] = self.SHAPPY
        elif second_map_item == self.EMPTY:
            new_reward = -1
            old_pos = state.second_shappy_pos
            new_map[old_pos] = self.EMPTY
            new_map[new_second_pos] = self.SHAPPY
        elif second_map_item == self.SHAPPY:
            new_reward = -1
            old_pos = state.second_shappy_pos
            new_map[old_pos] = self.EMPTY
            new_map[new_second_pos] = self.SHAPPY

        return State(map=new_map, first_shappy_pos=new_first_pos, second_shappy_pos=new_second_pos), new_reward

    def learn(self, state, action, reward, new_state):
        # Devia aqui alterar a tabela das transições P(state, action, new state)
        # Devia aqui alterar a tabela das rewards para cada estado R[state]
        # Q[si, a] = Q[si, a] + alpha * (r + gamma * max(Q[nsi, :]) - Q[si, a])
        # P[a, si, nsi] += 1
        # R[si] = r
        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        self.Q(state)[action] = self.Q(state, action) + self.learning_rate * \
                           (reward + self.gamma * np.max(self.Q(new_state)) - self.Q(state, action))

    def create_policy(self):

        total_episodes = 500  #tenho que aumentar isto para 100000 :(
        #total_test_episodes = 10

        # TRAIN
        rewards = []
        for episode in range(total_episodes):
            print(episode)
            state = self.start_state

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

            rewards.append(np.mean(episode_rewards))

        # clean up the lines where shappys where in different positions but only one 4 existed
        lines_to_delete = []
        for line in self.Q_table:
            if np.count_nonzero(line.map == 4) == 1 and line.first_shappy_pos != line.second_shappy_pos:
                lines_to_delete.append(line)

        for line in lines_to_delete:
            del self.Q_table[line]

        # for result in rewards:
        #     print(result)

    def write_in_txt(self, policy_file):
        # RESULTS
        f = open(policy_file, "w+")
        for line in self.Q_table:
            #print(line, "   ", np.argmax(self.Q(line)), "   ", self.Q(line))
            f.write("%s   %s    %s \r" % (line, np.argmax(self.Q(line)), self.Q(line)))
        f.close()
