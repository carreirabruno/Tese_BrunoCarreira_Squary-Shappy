import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as clr
import matplotlib.patches as mpatches

def makePosGraph(terrain, run_states):
    agent3_x = list()
    agent3_y = list()

    agent4_x = list()
    agent4_y = list()

    graphSize_max = len(terrain)

    for state in run_states:
        agent3_x.append(state[0][1])
        agent3_y.append(graphSize_max - state[0][0])

        agent4_x.append(state[1][1])
        agent4_y.append(graphSize_max - state[1][0])

    graphSize_min = 0
    graphSize_max = len(terrain)

    plt.figure()
    plt.plot(agent3_x, agent3_y, 'bo', label="Agent3")
    plt.plot(agent4_x, agent4_y, 'ro', label="Agent4")
    plt.xticks(np.arange(graphSize_min, graphSize_max), np.arange(graphSize_min, graphSize_max))
    plt.yticks(np.arange(graphSize_min, graphSize_max), np.arange(graphSize_min, graphSize_max))
    plt.legend(loc=8)
    plt.tick_params(axis='both', which='major', labelsize=15)

    ax = plt.gca()
    ax.set_xlim([graphSize_min, graphSize_max])
    ax.set_ylim([graphSize_min, graphSize_max])

    plt.savefig("teste.png", transparent=True)

    plt.show()


def makeHeatMapGraph(terrain, run_states):
    agent3_x = list()
    agent3_y = list()

    agent4_x = list()
    agent4_y = list()

    agents_x = list()
    agents_y = list()

    graphSize_max = len(terrain)

    for state in run_states:
        agent3_x.append(state[0][1])
        agent3_y.append(graphSize_max - state[0][0])

        agent4_x.append(state[1][1])
        agent4_y.append(graphSize_max - state[1][0])

        agents_x.append(state[0][1])
        agents_y.append(graphSize_max - state[0][0])
        agents_x.append(state[1][1])
        agents_y.append(graphSize_max - state[1][0])

    graphSize_min = 0
    graphSize_max = len(terrain)

    # bins = [np.arange(graphSize_min, graphSize_max, 1), np.arange(graphSize_min, graphSize_max, 1)]

    # plt.hist2d(agent3_x, agent3_y, bins=bins, cmap=plt.cm.Blues)
    # plt.colorbar()
    # plt.show()
    #
    # plt.hist2d(agent4_x, agent4_y, bins=bins, cmap=plt.cm.Reds)
    # plt.colorbar()
    # plt.show()

    # plt.hist2d(agents_x, agents_y, bins=bins, cmap=plt.cm.Greens)
    # plt.colorbar()
    # plt.show()

    fig = plt.figure(figsize=(5, 5))

    ax = fig.add_subplot(111)
    ax.set_xlim(graphSize_min, graphSize_max)
    ax.set_ylim(graphSize_min, graphSize_max)

    color_ratio = 4

    sequence_of_colors_agent4 = list()
    for i in range(color_ratio, len(agent4_x) + color_ratio):
        sequence_of_colors_agent4.append(clr.to_rgba_array(np.array([1, 1 - (color_ratio / i), 1 - (color_ratio / i)])))
    sequence_of_colors_agent4.reverse()

    for x, y, C in zip(agent4_x, agent4_y, sequence_of_colors_agent4):
        ax.scatter(x, y, marker="s", s=400, c=C)


    sequence_of_colors_agent3 = list()
    for i in range(color_ratio, len(agent3_x) + color_ratio):
        sequence_of_colors_agent3.append(clr.to_rgba_array(np.array([1 - (color_ratio / i), 1 - (color_ratio / i), 1])))
    sequence_of_colors_agent3.reverse()

    for x, y, C in zip(agent3_x, agent3_y, sequence_of_colors_agent3):
        ax.scatter(x, y, marker="s", s=300, c=C)

    pop_a = mpatches.Patch(color='#0000FF', label='Agent0')
    pop_b = mpatches.Patch(color='#FF0000', label='Agent1')

    plt.legend(handles=[pop_a, pop_b])

    # legend_blue = ax.legend(sequence_of_colors_agent3.index(len(sequence_of_colors_agent3)), loc="lower left", title="Agent0")
    # ax.add_artist(legend_blue)
    #
    # legend_red = ax.legend(np.arange(0, len(sequence_of_colors_agent4)), loc=10, title="Red agent Timesteps")
    # ax.add_artist(legend_red)
    # plt.legend()

    plt.show()








