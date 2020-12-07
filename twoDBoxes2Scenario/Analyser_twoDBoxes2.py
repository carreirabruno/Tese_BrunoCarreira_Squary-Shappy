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

        for index in range(len(testRunStates)-1):
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
                            return [self.individualActions[np.argmax(obj0[1])], self.individualActions[np.argmax(obj1[1])]]

        return -1

    def compareCombined(self):
        centCount = 0
        indCount = 0

        for state in self.runStates:
            equalCent = self.equalToCentralized(state)
            indCent = self.equalToIndividual(state)
            if equalCent[0]:
                centCount += self.getVotingValueCentralized(equalCent[1], state[1])/len(self.runStates)
            if self.equalToIndividual(state):
                indCount += self.getVotingValueIndividual(indCent[1], indCent[2], state[1])/len(self.runStates)

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

    def equalToCentralized(self, state):
        for temp in self.centralized:
            if temp[0] == state[0]:
                # if self.centralizedActions[np.argmax(temp[1])] == state[1]:
                return True, temp[1]
        return False

    def getVotingValueCentralized(self, Qactions, Aactions):
        Qaction = self.centralizedActions[np.argmax(Qactions)]

        vote = 0
        if Qaction[0] == Aactions[0]:
            vote += 0.5
        if Qaction[1] == Aactions[1]:
            vote += 0.5
        return vote

        # denominator = 0
        # for i in range(1, len(Qactions)+1):
        #     denominator += pow(math.e, -i)
        #
        # actionIndex = self.getCentralizedActionIndex(Aactions)
        #
        # tempQactions = copy.copy(Qactions)
        # tempQactions.sort()
        #
        # vote = 0
        #
        # for i in range(len(tempQactions)):
        #     if tempQactions[i] == Qactions[actionIndex]:
        #         vote = i
        #
        # if vote == len(Qactions)-1:
        #     vote = 1
        # else:
        #     vote = 0
        #
        #
        # # Voto com index/totalAcoes
        # # vote = (vote+1)/len(Qactions)
        #
        # return vote

    def equalToIndividual(self, state):
        temp0 = []
        temp1 = []
        for i in range(len(state[0])):
            if i != 1:
                temp0.append(state[0][i])
            if i != 0:
                temp1.append(state[0][i])

        for obj0 in self.individual0:
            if obj0[0] == temp0:
                for obj1 in self.individual1:
                    if obj1[0] == temp1:
                        # if self.individualActions[np.argmax(obj0[1])] == state[1][0] and self.individualActions[np.argmax(obj1[1])] == state[1][1]:
                        return True, obj0[1], obj1[1]
        return False

    def getVotingValueIndividual(self, Q0actions, Q1actions, Aactions):

        Qaction0 = self.individualActions[np.argmax(Q0actions)]
        Qaction1 = self.individualActions[np.argmax(Q1actions)]

        vote = 0
        if Qaction0 == Aactions[0]:
            vote += 0.5
        if Qaction1 == Aactions[1]:
            vote += 0.5
        return vote

        # denominator = 0
        # for i in range(1, len(Q0actions)+1):
        #     denominator += pow(math.e, -i)
        #
        # action0index = self.getIndividualActionIndex(Aactions[0])
        # action1index = self.getIndividualActionIndex(Aactions[1])
        #
        # tempQ0actions = copy.copy(Q0actions)
        # tempQ1actions = copy.copy(Q1actions)
        #
        # tempQ0actions.sort()
        # tempQ1actions.sort()
        #
        # vote0 = 0
        # vote1 = 0
        #
        # for i in range(len(tempQ0actions)):
        #     if tempQ0actions[i] == Q0actions[action0index]:
        #         vote0 = i
        #     if tempQ1actions[i] == Q1actions[action1index]:
        #         vote1 = i


        # Voto com os e^-index
        # vote0 = pow(math.e, - (len(Q0actions) - vote0))/denominator
        # vote1 = pow(math.e, - (len(Q1actions) - vote1))/denominator

        # Voto com index/totalAcoes
        # vote0 = (vote0+1)/len(Q0actions)
        # vote1 = (vote1+1)/len(Q1actions)
        # return (vote0 / 2) + (vote1 / 2)

        # vote = 0
        # if vote0 == len(Q0actions)-1 and vote1 == vote0:
        #     vote = 1

        # return vote



    def getIndividualActionIndex(self, stringAction):
        for i in range(len(self.individualActions)):
            if stringAction == self.individualActions[i]:
                return i
        return -1

    def getCentralizedActionIndex(self, stringAction):
        for i in range(len(self.centralizedActions)):
            if stringAction[0] == self.centralizedActions[i][0] and stringAction[1] == self.centralizedActions[i][1]:
                return i
        return -1
