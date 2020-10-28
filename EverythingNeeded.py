
import matplotlib.pyplot as plt
import numpy as np

def main():
    createPlot()


def createPlot():

    scenario = "scenario14"

    # type = "centralized"
    type = "individual"

    agent0 = open("C:/Users/bruno/Desktop/Ambiente de Trabalho/" + scenario + "_" + type + "_agent0.txt", "r")
    lines_agent0 = list(agent0)

    agent0_x = list()
    agent0_z = list()

    for pos_agent0 in lines_agent0:
        print(pos_agent0)
        pos_string_agent0 = str(pos_agent0).replace("<", "")
        pos_string_agent0 = pos_string_agent0.replace(">", "")
        pos_string_agent0 = pos_string_agent0.split(",")
        agent0_x.append(float(pos_string_agent0[0]))
        agent0_z.append(float(pos_string_agent0[2]))
    agent0.close()
    
    agent1 = open("C:/Users/bruno/Desktop/Ambiente de Trabalho/" + scenario + "_" + type + "_agent1.txt", "r")
    lines_agent1 = list(agent1)

    agent1_x = list()
    agent1_z = list()

    for pos_agent1 in lines_agent1:
        print(pos_agent1)
        pos_string_agent1 = str(pos_agent1).replace("<", "")
        pos_string_agent1 = pos_string_agent1.replace(">", "")
        pos_string_agent1 = pos_string_agent1.split(",")
        agent1_x.append(float(pos_string_agent1[0]))
        agent1_z.append(float(pos_string_agent1[2]))
    agent1.close()

    graphSize_min = 0
    graphSize_max = 11

    plt.figure()
    plt.plot(agent0_x, agent0_z, 'ro', label="Agent0")
    plt.plot(agent1_x, agent1_z, 'bo', label="Agent1")
    plt.xticks(np.arange(graphSize_min, graphSize_max), np.arange(graphSize_min, graphSize_max))
    plt.yticks(np.arange(graphSize_min, graphSize_max), np.arange(graphSize_min, graphSize_max))
    plt.legend(loc=8)

    ax = plt.gca()
    ax.set_ylim([graphSize_min, graphSize_max])
    ax.set_xlim([graphSize_min, graphSize_max])

    plt.savefig(scenario + "_" + type + ".png", transparent=True)

    plt.show()


if __name__ == "__main__":
    # call the main function
    main()
