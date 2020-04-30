import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


class Heatmap_twoDBoxes2(object):
    def __init__(self, terrain_matrix, run_states):
        # np.random.seed()
        # x = np.random.rayleigh(np.random.randint(0, 10), size=1)
        # y = np.random.rayleigh(np.random.randint(0, 10), size=1)
        # x = [4, 4, 5, 5, 5]
        # y = [5, 5, 5, 6, 7]

        wall_x = []
        wall_y = []
        for i in range(len(terrain_matrix)):
            for j in range(len(terrain_matrix[i])):
                if terrain_matrix[j][i] == 1:
                    wall_x.append(10 - j)
                    wall_y.append(i)
        plt.hist2d(wall_y, wall_x, bins=[np.arange(0, 11, 1), np.arange(1, 12, 1)], cmap=plt.cm.Greys)
        plt.colorbar()
        plt.show()

        shappy3_x = []
        shappy3_y = []
        shappy4_x = []
        shappy4_y = []

        for line in run_states:
            shappy3_x.append(10 - line[0][0])
            shappy3_y.append(line[0][1])
            shappy4_x.append(10 - line[1][0])
            shappy4_y.append(line[1][1])

        plt.hist2d(shappy3_y, shappy3_x, bins=[np.arange(0, 11, 1), np.arange(1, 12, 1)], cmap=plt.cm.Blues)
        plt.colorbar()
        plt.show()

        plt.hist2d(shappy4_y, shappy4_x, bins=[np.arange(0, 11, 1), np.arange(1, 12, 1)], cmap=plt.cm.Reds)
        plt.colorbar()
        plt.show()
