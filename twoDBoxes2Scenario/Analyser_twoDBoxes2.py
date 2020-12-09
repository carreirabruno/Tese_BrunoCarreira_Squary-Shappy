import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pickle
import copy
import math


class Analyser_twoDBoxes2(object):
    # def __init__(self, terrain_matrix, run_states, scenario_policies):
    #     self.terrain_matrix = terrain_matrix
    #     self.run_states = run_states
    #     self.scenario_policies = scenario_policies
    #
    #     # # Maximize Social Utility
    #     self.count_number_of_steps()
    #
    #     # # Count collisions
    #     self.count_boxes_caught()
    #
    #     # # Count collisions
    #     self.count_collisions()
    #
    #     # # Count communications
    #     self.count_communications()
    #
    #     # # Split Attention
    #     self.create_heatmaps()
    #
    # def count_number_of_steps(self):
    #     shappy3_steps = 0
    #     shappy4_steps = 0
    #     print(self.run_states[0])
    #     for i in range(1, len(self.run_states)):
    #         if not self.compare_arrays(self.run_states[i][0], self.run_states[i-1][0]):
    #             shappy3_steps += 1
    #         if not self.compare_arrays(self.run_states[i][1], self.run_states[i-1][1]):
    #             shappy4_steps += 1
    #         print(self.run_states[i])
    #
    #     print("Steps made by shappy 3 -> ", shappy3_steps)
    #     print("Steps made by shappy 4 -> ", shappy4_steps)
    #     print("Total steps made -> ", shappy3_steps + shappy4_steps)
    #
    # def compare_arrays(self, array1, array2):
    #     if len(array1) != len(array2):
    #         return False
    #     else:
    #         for i in range(len(array1)):
    #             if array1[i] != array2[i]:
    #                 return False
    #     return True
    #
    # def get_policy(self, policy_file, centralized):
    #     fp = open(policy_file, "rb")  # Unpickling
    #     if centralized:
    #         policy = pickle.load(fp)
    #     else:
    #         policy1, policy2 = pickle.load(fp)
    #     fp.close()
    #     if centralized:
    #         return policy
    #     else:
    #         return policy1, policy2
    #
    # def count_communications(self):
    #     shappy3_communication = 0
    #     shappy4_communication = 0
    #     policy3, policy4 = self.get_policy(self.scenario_policies[3], False)
    #     for state in self.run_states:
    #         state3 = copy.deepcopy(state)
    #         state4 = copy.deepcopy(state)
    #         if shappy3_communication == 0:
    #             state3[1] = [-1, -1]
    #         if shappy4_communication == 0:
    #             state4[0] = [-1, -1]
    #         for policy in policy3:
    #             if self.compare_arrays(state3, policy[0]) and np.argmax(policy[1]) == 5:
    #                 shappy3_communication += 1
    #                 break
    #         for policy in policy4:
    #             if self.compare_arrays(state4, policy[0]) and np.argmax(policy[1]) == 5:
    #                 shappy4_communication += 1
    #                 break
    #     print("Blue listened: ", shappy3_communication)
    #     print("Red listened: ", shappy4_communication)
    #
    # def count_collisions(self):
    #     collisions = 0
    #     for state in self.run_states:
    #         if self.compare_arrays(state[0], state[1]):
    #             collisions += 1
    #
    #     print("Collisions: ", collisions)
    #
    # def count_boxes_caught(self):
    #     shappy3_boxes = 0
    #     shappy4_boxes = 0
    #     for i in range(1, len(self.run_states)):
    #         for j in range(2, len(self.run_states[i-1])):
    #             if self.compare_arrays(self.run_states[i][0], self.run_states[i-1][j]):
    #                 shappy3_boxes += 1
    #             if self.compare_arrays(self.run_states[i][1], self.run_states[i-1][j]):
    #                 shappy4_boxes += 1
    #
    #     print("Boxes caught by shappy 3 -> ", shappy3_boxes)
    #     print("Boxes caught by shappy 4 -> ", shappy4_boxes)

    def __init__(self, filename_centralized, filename_individual, testRunStates, typeCentralized):

        self.centralized = []
        self.individual0 = []
        self.individual1 = []
        self.runStates = []

        self.individualActions = ["Nothing", "Left", "Right", "Up", "Down"]
        self.centralizedActions = [["Nothing", "Left"], ["Nothing", "Right"], ["Nothing", "Up"], ["Nothing", "Down"],
                                   ["Left", "Nothing"], ["Left", "Left"], ["Left", "Right"], ["Left", "Up"],
                                   ["Left", "Down"],
                                   ["Right", "Nothing"], ["Right", "Left"], ["Right", "Right"], ["Right", "Up"],
                                   ["Right", "Down"],
                                   ["Up", "Nothing"], ["Up", "Left"], ["Up", "Right"], ["Up", "Up"], ["Up", "Down"],
                                   ["Down", "Nothing"], ["Down", "Left"], ["Down", "Right"], ["Down", "Up"],
                                   ["Down", "Down"]]


        indDenominator = 0
        for i in range(1, len(self.individualActions) + 1):
            indDenominator += pow(math.e, -i)

        centDenominator = 0
        for i in range(1, len(self.centralizedActions) + 2):
            centDenominator += pow(math.e, -i)

        print((pow(math.e, -1) / indDenominator))
        print(pow(math.e, -1) / centDenominator)
        quit(123)

        self.readPolicies(filename_centralized, filename_individual)

        self.organizeTestRunStates(testRunStates, typeCentralized)

        self.compareCombined()

    def readPolicies(self, filename_centralized, filename_individual):
        cen = open(filename_centralized, 'rb')
        self.centralized = pickle.load(cen)
        cen.close()

        ind = open(filename_individual, 'rb')
        self.individual0, self.individual1 = pickle.load(ind)
        ind.close()

    def organizeTestRunStates(self, testRunStates, typeCentralized):
        # for index in range(1, len(testRunStates)):
        #     centAction = self.getAction(testRunStates[index-1], testRunStates[index])
        #     self.runStates.append([testRunStates[index-1], centAction])

        for index in range(len(testRunStates) - 1):
            centAction = self.getRunActions(testRunStates[index], typeCentralized)
            self.runStates.append([testRunStates[index], centAction])

    # def getAction(self, state0, state1):
    #     action = []
    #     if state0[0] == state1[0]:
    #         action.append("Nothing")
    #     elif state0[0][0] > state1[0][0]:
    #         action.append("Up")
    #     elif state0[0][0] < state1[0][0]:
    #         action.append("Down")
    #     elif state0[0][1] > state1[0][1]:
    #         action.append("Left")
    #     elif state0[0][1] < state1[0][1]:
    #         action.append("Right")
    #
    #     if state0[1] == state1[1]:
    #         action.append("Nothing")
    #     elif state0[1][0] > state1[1][0]:
    #         action.append("Up")
    #     elif state0[1][0] < state1[1][0]:
    #         action.append("Down")
    #     elif state0[1][1] > state1[1][1]:
    #         action.append("Left")
    #     elif state0[1][1] < state1[1][1]:
    #         action.append("Right")
    #
    #     return action

    def getRunActions(self, state, typeCentralized):
        if typeCentralized:
            for temp in self.centralized:
                if temp[0] == state:
                    return self.centralizedActions[np.argmax(temp[1])]
        else:
            temp0 = []
            temp1 = []
            for i in range(len(state)):
                if i != 1:
                    temp0.append(state[i])
                if i != 0:
                    temp1.append(state[i])

            for obj0 in self.individual0:
                if obj0[0] == temp0:
                    for obj1 in self.individual1:
                        if obj1[0] == temp1:
                            return [self.individualActions[np.argmax(obj0[1])],
                                    self.individualActions[np.argmax(obj1[1])]]

        return -1

    def compareCombined(self):
        centCount = 0
        indCount = 0

        # indDenominator = 0
        # for i in range(1, len(self.individualActions) + 1):
        #     indDenominator += pow(math.e, -i)
        #
        # centDenominator = 0
        # for i in range(1, len(self.centralizedActions) + 1):
        #     centDenominator += pow(math.e, -i)

        for state in self.runStates:
            # centCount += self.getVotingValueCentralized(state)/centDenominator
            # indCount += self.getVotingValueIndividual(state)/(2*indDenominator)
            centCount += self.getVotingValueCentralized(state)
            indCount += self.getVotingValueIndividual(state)

        maxValue = len(self.runStates) * (1 * 1)

        centCount = centCount/maxValue
        indCount = indCount/maxValue

        print("Centralized ", "{:0.2f}".format(centCount), " ", len(self.runStates))
        print("Individual ", "{:0.2f}".format(indCount), " ", len(self.runStates))

        # count = 0
        # for centralizedObj in self.centralized:
        #     centralizedAgent0, centralizedAgent1 = self.getIndividualStates(centralizedObj[0])
        #     centralizedAction = self.centralizedActions[np.argmax(centralizedObj[1])]
        #     for individualObj0 in self.individual0:
        #         if centralizedAgent0 == individualObj0[0]:
        #             for individualObj1 in self.individual1:
        #                 if centralizedAgent1 == individualObj1[0]:
        #                     individualAction = [self.individualActions[np.argmax(individualObj0[1])], self.individualActions[np.argmax(individualObj1[1])]]
        #                     if individualAction == centralizedAction:
        #                         count += 1
        #
        #
        # print(len(self.centralized))
        # print(len(self.individual0))
        # print(len(self.individual1))
        # print(count)

    def getVotingValueCentralized(self, state):
        vote = 0

        for temp in self.centralized:
            if temp[0] == state[0]:
                values = self.getCentralizedActionIndexOrdered(temp[1], state[1])
                vote = pow(math.e, -values[0]) + pow(math.e, -values[1])
                # vote = pow(math.e, -value)

        return vote

    def getCentralizedActionIndexOrdered(self, actionsQValues, stringActions):
        qActionsAgents0 = [1] * len(self.individualActions)
        qActionsAgents1 = [1] * len(self.individualActions)

        for i in range(len(actionsQValues)):
            for j in range(len(self.individualActions)):
                if self.centralizedActions[i][0] == self.individualActions[j]:
                    qActionsAgents0[j] += actionsQValues[i]
                if self.centralizedActions[i][1] == self.individualActions[j]:
                    qActionsAgents1[j] += actionsQValues[i]

        qActionsAgents0[0] = qActionsAgents0[0]/(len(qActionsAgents0)-1)
        qActionsAgents1[0] = qActionsAgents1[0]/(len(qActionsAgents1)-1)
        for v in range(1, len(self.individualActions)):
            qActionsAgents0[v] = qActionsAgents0[v]/len(qActionsAgents0)
            qActionsAgents1[v] = qActionsAgents1[v]/len(qActionsAgents1)

        return [self.getIndividualActionIndex(qActionsAgents0, stringActions[0]), self.getIndividualActionIndex(qActionsAgents1, stringActions[1])]

        # tempActionValues = copy.copy(actionsQValues)
        #
        # tempActionValues.sort()
        #
        # actionV = -1
        #
        # for i in range(len(actionsQValues)):
        #     if stringActions == self.centralizedActions[i]:
        #         actionV = actionsQValues[i]
        #
        # for i in range(len(tempActionValues) - 1, -1, -1):
        #     if actionV == tempActionValues[i]:
        #         print(i)
        #         return len(tempActionValues) - i
        # return -1

    def getIndividualStates(self, state):
        temp0 = []
        temp1 = []
        for i in range(len(state[0])):
            if i != 1:
                temp0.append(state[0][i])
            if i != 0:
                temp1.append(state[0][i])
        return temp0, temp1

    def getVotingValueIndividual(self, state):
        vote = 0

        indState = self.getIndividualStates(state)

        for temp in self.individual0:
            if temp[0] == indState[0]:
                vote += pow(math.e, -self.getIndividualActionIndex(temp[1], state[1][0]))

        for temp in self.individual1:
            if temp[0] == indState[1]:
                vote += pow(math.e, -self.getIndividualActionIndex(temp[1], state[1][1]))

        return vote

    def getIndividualActionIndex(self, actionQValues, stringAction):
        tempActionValues = copy.copy(actionQValues)

        tempActionValues.sort()

        actionV = -1

        for i in range(len(actionQValues)):
            if stringAction == self.individualActions[i]:
                actionV = actionQValues[i]

        for i in range(len(tempActionValues) - 1, -1, -1):
            if actionV == tempActionValues[i]:
                return len(tempActionValues) - i
        return -1
