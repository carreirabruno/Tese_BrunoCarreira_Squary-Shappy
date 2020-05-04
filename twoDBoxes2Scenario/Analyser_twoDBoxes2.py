import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


class Analyser_twoDBoxes2(object):
    def __init__(self, terrain_matrix, run_states):
        self.terrain_matrix = terrain_matrix
        self.run_states = run_states

        # # Maximize Social Utility
        self.count_number_of_steps()

        # # Split Attention
        # self.create_heatmaps()

    def create_heatmaps(self):

        wall_x = []
        wall_y = []
        for i in range(len(self.terrain_matrix)):
            for j in range(len(self.terrain_matrix[i])):
                if self.terrain_matrix[j][i] == 1:
                    wall_x.append(10 - j)
                    wall_y.append(i)
        plt.hist2d(wall_y, wall_x, bins=[np.arange(0, 11, 1), np.arange(1, 12, 1)], cmap=plt.cm.Greys)
        plt.colorbar()
        plt.show()

        box_x = []
        box_y = []
        for i in range(len(self.terrain_matrix)):
            for j in range(len(self.terrain_matrix[i])):
                if self.terrain_matrix[j][i] == 2:
                    box_x.append(10 - j)
                    box_y.append(i)
        plt.hist2d(box_y, box_x, bins=[np.arange(0, 11, 1), np.arange(1, 12, 1)], cmap=plt.cm.Greens)
        plt.colorbar()
        plt.show()

        shappy3_x = []
        shappy3_y = []
        shappy4_x = []
        shappy4_y = []

        for line in self.run_states:
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

    def count_number_of_steps(self):
        shappy3_steps = 0
        shappy4_steps = 0
        for i in range(1, len(self.run_states)):
            if not self.compare_arrays(self.run_states[i][0], self.run_states[i-1][0]):
                shappy3_steps += 1
            if not self.compare_arrays(self.run_states[i][1], self.run_states[i-1][1]):
                shappy4_steps += 1

        print("Steps made by shappy 3 -> ", shappy3_steps)
        print("Steps made by shappy 4 -> ", shappy4_steps)
        print("Total steps made -> ", shappy3_steps + shappy4_steps)

    def compare_arrays(self, array1, array2):
        if len(array1) != len(array2):
            return False
        else:
            for i in range(len(array1)):
                if array1[i] != array2[i]:
                    return False
        return True
