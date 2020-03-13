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
        return isinstance(other, State)# and self.map == other.map and self.first_shappy_pos == other.first_shappy_pos \
               #and self.second_shappy_pos == other.second_shappy_pos

    def __hash__(self):
        return hash(str(self.map) + str(self.first_shappy_pos) + str(self.second_shappy_pos))

    def __str__(self):
        return f"State(map={self.map}, first_shappy_pos={self.first_shappy_pos}, " \
               f"second_shappy_pos={self.second_shappy_pos})"


def detect_shappys_pos(non_col_shappys, col_shappys):
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

def Q(state, action=None):
    if state not in Q_table:
        Q_table[state] = np.zeros(len(ACTIONS))

    if action is None:
        return Q_table[state]

    return Q_table[state][action]


def choose_actions(state):
    if random.random() < 0.1:  # exploration
        return random.randint(0, len(ACTIONS) - 1)
    else:  # exploitation
        return np.argmax(Q(state))


def take_actions(state, actions):
    def new_shappy_pos(state, action):
        new_first_shappy_pos = copy.deepcopy(state.first_shappy_pos)
        new_second_shappy_pos = copy.deepcopy(state.second_shappy_pos)
        if action == LEFT_LEFT:
            if state.map[new_first_shappy_pos - 1] == WALL:  # colidiu com uma wall
                new_first_shappy_pos = new_first_shappy_pos
            else:
                new_first_shappy_pos = max(0, new_first_shappy_pos - 1)
            if state.map[new_second_shappy_pos - 1] == WALL:  # colidiu com uma wall
                new_second_shappy_pos = new_second_shappy_pos
            else:
                new_second_shappy_pos = max(0, new_second_shappy_pos - 1)
        elif action == LEFT_STAY:
            if state.map[new_first_shappy_pos - 1] == WALL:  # colidiu com uma wall
                new_first_shappy_pos = new_first_shappy_pos
            else:
                new_first_shappy_pos = max(0, new_first_shappy_pos - 1)
            new_second_shappy_pos = new_second_shappy_pos
        elif action == LEFT_RIGHT:
            if state.map[new_first_shappy_pos - 1] == WALL:  # colidiu com uma wall
                new_first_shappy_pos = new_first_shappy_pos
            else:
                new_first_shappy_pos = max(0, new_first_shappy_pos - 1)
            if state.map[new_second_shappy_pos + 1] == WALL:  # colidiu com uma wall
                new_second_shappy_pos = new_second_shappy_pos
            else:
                new_second_shappy_pos = min(len(state.map) - 1, new_second_shappy_pos + 1)
        elif action == STAY_LEFT:
            new_first_shappy_pos = new_first_shappy_pos
            if state.map[new_second_shappy_pos - 1] == WALL:  # colidiu com uma wall
                new_second_shappy_pos = new_second_shappy_pos
            else:
                new_second_shappy_pos = max(0, new_second_shappy_pos - 1)
        elif action == STAY_STAY:
            new_first_shappy_pos = new_first_shappy_pos
            new_second_shappy_pos = new_second_shappy_pos
        elif action == STAY_RIGHT:
            new_first_shappy_pos = new_first_shappy_pos
            if state.map[new_second_shappy_pos + 1] == WALL:  # colidiu com uma wall
                new_second_shappy_pos = new_second_shappy_pos
            else:
                new_second_shappy_pos = min(len(state.map) - 1, new_second_shappy_pos + 1)
        elif action == RIGHT_LEFT:
            if state.map[new_first_shappy_pos + 1] == WALL:  # colidiu com uma wall
                new_first_shappy_pos = new_first_shappy_pos
            else:
                new_first_shappy_pos = min(len(state.map) - 1, new_first_shappy_pos + 1)
            if state.map[new_second_shappy_pos - 1] == WALL:  # colidiu com uma wall
                new_second_shappy_pos = new_second_shappy_pos
            else:
                new_second_shappy_pos = max(0, new_second_shappy_pos - 1)
        elif action == RIGHT_STAY:
            if state.map[new_first_shappy_pos + 1] == WALL:  # colidiu com uma wall
                new_first_shappy_pos = new_first_shappy_pos
            else:
                new_first_shappy_pos = min(len(state.map) - 1, new_first_shappy_pos + 1)
            new_second_shappy_pos = new_second_shappy_pos
        elif action == RIGHT_RIGHT:
            if state.map[new_first_shappy_pos + 1] == WALL:  # colidiu com uma wall
                new_first_shappy_pos = new_first_shappy_pos
            else:
                new_first_shappy_pos = min(len(state.map) - 1, new_first_shappy_pos + 1)
            if state.map[new_second_shappy_pos + 1] == WALL:  # colidiu com uma wall
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
    if first_map_item == BOX:
        new_reward = 100
        old_pos = state.first_shappy_pos
        new_map[old_pos] = EMPTY
        new_map[new_first_pos] = SHAPPY
    elif first_map_item == EMPTY:
        new_reward = -1
        old_pos = state.first_shappy_pos
        new_map[old_pos] = EMPTY
        new_map[new_first_pos] = SHAPPY
    elif first_map_item == SHAPPY:
        new_reward = -1
        old_pos = state.first_shappy_pos
        new_map[old_pos] = EMPTY
        new_map[new_first_pos] = SHAPPY


    if second_map_item == BOX:
        new_reward = 100
        old_pos = state.second_shappy_pos
        new_map[old_pos] = EMPTY
        new_map[new_second_pos] = SHAPPY
    elif second_map_item == EMPTY:
        new_reward = -1
        old_pos = state.second_shappy_pos
        new_map[old_pos] = EMPTY
        new_map[new_second_pos] = SHAPPY
    elif second_map_item == SHAPPY:
        new_reward = -1
        old_pos = state.second_shappy_pos
        new_map[old_pos] = EMPTY
        new_map[new_second_pos] = SHAPPY

    return State(map=new_map, first_shappy_pos=new_first_pos, second_shappy_pos=new_second_pos), new_reward


def learn(state, action, reward, new_state):
    # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
    Q(state)[action] = Q(state, action) + learning_rate * \
                             (reward + gamma * np.max(Q(new_state)) - Q(state, action))

    # Devia aqui alterar a tabela das transições P(state, action, new state)
    # Devia aqui alterar a tabela das rewards para cada estado R[state]

    # Q[si, a] = Q[si, a] + alpha * (r + gamma * max(Q[nsi, :]) - Q[si, a])
    # P[a, si, nsi] += 1
    # R[si] = r




##############################################################################################
    random.seed(42)


#BEGIN RUN

# Environment
WALL = "1"
BOX = "2"
#NON_COL_SHAPPY = 3
SHAPPY = "4"
EMPTY = "."

map = np.array(
    [WALL, BOX, EMPTY, EMPTY, EMPTY, SHAPPY, EMPTY, EMPTY, BOX, EMPTY, BOX, SHAPPY, EMPTY, BOX, WALL])

# Actions
STAY_STAY = 0
STAY_LEFT = 1
STAY_RIGHT = 2
LEFT_STAY = 3
LEFT_LEFT = 4
LEFT_RIGHT = 5
RIGHT_STAY = 6
RIGHT_LEFT = 7
RIGHT_RIGHT = 8

ACTIONS = [STAY_STAY, STAY_LEFT, STAY_RIGHT,
           LEFT_STAY, LEFT_LEFT, LEFT_RIGHT,
           RIGHT_STAY, RIGHT_LEFT, RIGHT_RIGHT]
n_actions = len(ACTIONS)

#non_col_shappys = np.where(map == "3")
shappys = np.where(map == "4")


#first_shappy_pos, second_shappy_pos = detect_shappys_pos(non_col_shappys[0], col_shappys[0])

start_state = State(map=map, first_shappy_pos=shappys[0][0], second_shappy_pos=shappys[0][1])

gamma = 0.9
learning_rate = 0.1  # alpha

n_states = len(map)  # * n_actions * 4       #4 é o numero de boxes

# Q_table = np.zeros((n_states, n_actions))
Q_table = dict()

total_episodes = 100
total_test_episodes = 10

# TRAIN
rewards = []
for episode in range(total_episodes):

    state = start_state
    episode_rewards = []

    while True:
        if "2" not in state.map:
            break

        actions = choose_actions(state)

        new_state, reward = take_actions(state, actions)

        # print(new_state, " ",actions)

        learn(state, actions, reward, new_state)

        episode_rewards.append(reward)

        state = new_state

    rewards.append(np.mean(episode_rewards))

#clean up the lines where shappys where in different positions but only one 4 existed
lines_to_delete = []
for line in Q_table:
    if np.count_nonzero(line.map == "4") == 1 and line.first_shappy_pos != line.second_shappy_pos:
        lines_to_delete.append(line)

for line in lines_to_delete:
    del Q_table[line]


# for result in rewards:
#     print(result)

# RESULTS
f = open("oneDBoxes_MDP_policy_100.txt", "w+")
for line in Q_table:
    # print(line, "   ", np.argmax(Q(line)), "   ", Q(line))
    # if np.argmax(Q(state)) == 0:
    #     action = "LEFT"
    # elif np.argmax(Q(state)) == 1:
    #     action = "STAY"
    # else:
    #     action = "RIGHT"

    f.write("%s   %s    %s \r" % (line, np.argmax(Q(line)), Q(line)))
f.close()
