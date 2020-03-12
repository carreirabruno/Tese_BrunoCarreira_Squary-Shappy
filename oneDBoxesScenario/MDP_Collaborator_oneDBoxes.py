import numpy as np
import random
import copy

class State:

    def __init__(self, map, shappy_pos):
        self.map = map
        self.shappy_pos = shappy_pos

    def __eq__(self, other):
        return isinstance(other, State) and self.map == other.map and self.shappy_pos == other.shappy_pos

    def __hash__(self):
        return hash(str(self.map) + str(self.shappy_pos))

    def __str__(self):
        return f"State(grid={self.map}, shappy_x_pos={self.shappy_pos})"


random.seed(42)

# Environment
WALL = "w"
BOX = "b"
COL_SHAPPY = "c"
NON_COL_SHAPPY = "n"
EMPTY = "*"

map = [WALL, BOX, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BOX, EMPTY, BOX, COL_SHAPPY, EMPTY, BOX, WALL]

# Actions
LEFT = 0
STAY = 1
RIGHT = 2
ACTIONS = [LEFT, STAY, RIGHT]
n_actions = len(ACTIONS)

pos = -1
for i in range(len(map)):
    if map[i] == "c":
        pos = i

start_state = State(map=map, shappy_pos=pos)

gamma = 0.9
learning_rate = 0.1  # alpha

n_states = len(map)  # * n_actions * 4       #4 é o numero de boxes

#Q_table = np.zeros((n_states, n_actions))
Q_table = dict()

def choose_action(state):
    if state not in Q_table:
        Q_table[state] = np.zeros(len(ACTIONS))

    if random.random() < 0.1:  # exploration
        return random.choices(ACTIONS)
    else:  # exploitation
        return np.argmax(Q_table[state])


def take_action(state, action):
    def new_shappy_pos(state, action):
        pos = copy.deepcopy(state.shappy_pos)
        if action == LEFT:
            if state.map[pos - 1] == WALL:  # colidiu com uma wall
                pos = pos
            else:
                pos = max(0, pos - 1)
        elif action == STAY:
            pos = pos
        elif action == RIGHT:
            if state.map[pos + 1] == WALL:  # colidiu com uma wall
                pos = pos
            else:
                pos = min(len(state.map) - 1, pos + 1)
        else:
            raise ValueError(f"Unknown action {action}")
        return pos

    new_pos = new_shappy_pos(state, action)
    map_item = state.map[new_pos]

    new_map = copy.deepcopy(state.map)
    if map_item == BOX:
        reward = 10
        old_pos = state.shappy_pos
        new_map[old_pos] = EMPTY
        new_map[new_pos] = COL_SHAPPY
    elif map_item == EMPTY:
        reward = -1
        old_pos = state.shappy_pos
        new_map[old_pos] = EMPTY
        new_map[new_pos] = COL_SHAPPY
    elif map_item == COL_SHAPPY:
        reward = -1
    else:
        raise ValueError(f"Unknown grid item {map_item}")

    return State(map=new_map, shappy_pos=pos), reward


def learn(state, action, reward, new_state):
    # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
    print(state, action, reward, new_state)
    print(Q_table[state])
    Q_table(state)[action] = Q_table[state, action] + learning_rate * \
                             (reward + gamma * np.max(Q_table[new_state]) - Q_table[state, action])

    # Devia aqui alterar a tabela das transições P(state, action, new state)
    # Devia aqui alterar a tabela das rewards para cada estado R[state]

    # Q[si, a] = Q[si, a] + alpha * (r + gamma * max(Q[nsi, :]) - Q[si, a])
    # P[a, si, nsi] += 1
    # R[si] = r


total_episodes = 10
total_test_episodes = 10
rewards = []

for episode in range(total_episodes):

    state = start_state
    episode_rewards = []

    while True:

        if "b" not in state.map:
            break

        action = choose_action(state)

        new_state, reward = take_action(state, action)

        learn(state, action, reward, new_state)

        episode_rewards.append(reward)

        state = new_state

    rewards.append(np.mean(episode_rewards))


print("done")
