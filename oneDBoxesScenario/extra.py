import numpy as np
import random
from copy import deepcopy


class State:

    def __init__(self, grid, shappy_x_pos):
        self.grid = grid
        self.shappy_x_pos = shappy_x_pos

    def __eq__(self, other):
        return isinstance(other, State) and self.grid == other.grid and self.shappy_x_pos == other.shappy_x_pos

    def __hash__(self):
        return hash(str(self.grid) + str(self.shappy_x_pos))

    def __str__(self):
        return f"State(grid={self.grid}, shappy_x_pos={self.shappy_x_pos})"


# Environment
BOX = "b"
COL_SHAPPY = "c"
NON_COL_SHAPPY = "n"
EMPTY = "*"

grid = [BOX, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BOX, EMPTY, COL_SHAPPY, EMPTY, BOX]

# Actions
LEFT = 0
STAY = 1
RIGHT = 2

ACTIONS = [LEFT, STAY, RIGHT]

pos = -1

for i in range(len(grid)):
    if grid[i] == "c":
        pos = i

start_state = State(grid=grid, shappy_x_pos=pos)


def act(state, action):
    def new_shappy_x_pos(state, action):
        p = deepcopy(state.shappy_x_pos)
        if action == LEFT:
            p = max(0, p - 1)
        elif action == STAY:
            p = p
        elif action == RIGHT:
            p = min(len(grid) - 1, p + 1)
        else:
            raise ValueError(f"Unknown action {action}")
        return p

    p = new_shappy_x_pos(state, action)
    grid_item = state.grid[p]

    new_grid = deepcopy(state.grid)
    if "b" not in grid:
        is_done = True
    elif grid_item == BOX:
        reward = 10
        is_done = False
        old = state.shappy_x_pos
        new_grid[old] = EMPTY
        new_grid[p] = COL_SHAPPY
    elif grid_item == EMPTY:
        reward = -1
        is_done = False
        old = state.shappy_x_pos
        new_grid[old] = EMPTY
        new_grid[p] = COL_SHAPPY
    elif grid_item == COL_SHAPPY:
        reward = -1
        is_done = False
    else:
        raise ValueError(f"Unknown grid item {grid_item}")

    return State(grid=new_grid, shappy_x_pos=p), reward, is_done


random.seed(42)  # for reproducibility
N_STATES = len(grid)
N_EPISODES = 100

MAX_EPISODE_STEPS = 100

MIN_ALPHA = 0.02

alphas = np.linspace(1.0, MIN_ALPHA, N_EPISODES)
gamma = 1.0
eps = 0.2

q_table = dict()


def q(state, action=None):
    if state not in q_table:
        q_table[state] = np.zeros(len(ACTIONS))

    if action is None:
        return q_table[state]

    return q_table[state][action]


def choose_action(state):
    if random.uniform(0, 1) < eps:
        return random.choice(ACTIONS)
    else:
        return np.argmax(q(state))


#############################################

for e in range(N_EPISODES):

    state = start_state
    total_reward = 0
    alpha = alphas[e]

    #  for _ in range(MAX_EPISODE_STEPS):
    parar = False
    first = True
    while not parar:
        if first:
            first = False
        elif not first:
            count = 0

            for letter in state.grid:
                if letter is 'b':
                    count += 1
            if count == 0:
                parar = True

        action = choose_action(state)
        next_state, reward, done = act(state, action)
        total_reward += reward

        q(state)[action] = q(state, action) + \
                           alpha * (reward + gamma * np.max(q(next_state)) - q(state, action))
        state = next_state
        if done:
            break
    # print(f"Episode {e + 1}: total reward -> {total_reward}")

print(start_state)
r = q(start_state)
print(f"left={r[LEFT]}, stay={r[STAY]} ,right={r[RIGHT]}")

action_to_take = LEFT
if r[STAY] > r[action_to_take]:
    action_to_take = STAY
if r[RIGHT] > r[action_to_take]:
    action_to_take = RIGHT

new_state, reward, done = act(start_state, action_to_take)

print(new_state)
r = q(new_state)
print(f"left={r[LEFT]}, stay={r[STAY]} ,right={r[RIGHT]}")

while True:
    if "b" not in new_state.grid:
        break

    action_to_take = LEFT
    if r[STAY] > r[action_to_take]:
        action_to_take = STAY
    if r[RIGHT] > r[action_to_take]:
        action_to_take = RIGHT

    new_state, reward, done = act(new_state, action_to_take)

    print(new_state)

    r = q(new_state)
    print(f"left={r[LEFT]}, stay={r[STAY]} ,right={r[RIGHT]}")
