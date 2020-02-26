from random import random
from math import exp




class Perceptron:

	def __init__(self, num_inputs, num_outputs, learning_rate, epochs):

		self.epochs = epochs
		prov_dendrites = []
		prov_telo_dendrites = []
		self.output_dendrites = []
		for i in range(num_inputs):
			prov_dendrites.append(Dendrite())

		for i in range(num_outputs):
			self.output_dendrites.append(Dendrite)
			prov_telo_dendrites.append(Telo_dendrite(self.output_dendrites[i-1], 1))

		prov_axon = Axon(prov_telo_dendrites)

		self.neuron = Neuron(prov_dendrites, prov_axon, learning_rate)


	def train(self, inputs, outputs):

		for epoch in range(self.epochs):
			instance_num = 0
			for instance in inputs:
				output_num = 0
				for output_value in outputs[instance_num]:
					self.neuron.axon.telo_dendrites[output_num].expected_value = output_value
					output_num += 1
				input_num = 0
				for input_value in instance:
					self.neuron.dendrites[input_num].input_value = input_value
					input_num += 1
				self.neuron.learn()
				instance_num += 1

	def test(self, inputs):

		output = []
		instance_num = 0
		for instance in inputs:
				input_num = 0
				for input_value in instance:
					self.neuron.dendrites[input_num].input_value = input_value
					input_num += 1
				output.append(self.neuron.sinapse())
				instance_num += 1
		return output


class Neuron:

	def __init__(self, dendrites, axon, learning_rate):

		self.dendrites = dendrites
		for dendrite in dendrites:
			dendrite.neuron = self
		self.axon = axon
		self.b_potential = random()
		self.learning_rate = learning_rate



	def activation_function(self, potential):
		print(potential)
		print(exp(0.0 - potential))
		return 1.0/(1.0 + exp(-potential))




	def sinapse(self):

		potential = self.b_potential

		for dendrite in self.dendrites:
			potential += dendrite.weight * dendrite.input_value
		self.axon.sinapse(self.activation_function(potential))
		return self.activation_function(potential)




	def learn(self):

		obtained = self.sinapse()

		error = self.axon.expected() - obtained
		self.b_potential += self.learning_rate * error

		for dendrite in self.dendrites:
			dendrite.weight += self.learning_rate * error * dendrite.input_value

	def expected(self):
		return self.axon.expected()







class Dendrite:

	def __init__(self):
		self.weight = random()
		self.input_value = 0
		self.neuron = None

	def expected(self):
		return self.neuron.expected()



class Telo_dendrite:

	def __init__(self, dendrite, is_output):
		self.dendrite = dendrite
		self.is_output = is_output
		self.expected_value = 0

	def expected(self):
		if self.is_output:
			return self.expected_value
		else:
			return self.dendrite.expected()




class Axon:

	def __init__(self, telo_dendrites):
		self.telo_dendrites = telo_dendrites

	def expected(self):
		prov_result = 0
		for telo_dendrite in self.telo_dendrites:
			prov_result += telo_dendrite.expected()
		return prov_result/len(self.telo_dendrites)

	def sinapse(self, value):
		for telo_dendrite in self.telo_dendrites:
			telo_dendrite.dendrite.input_value = value





# input_m = [[1,2,1],[2,1,1],[3,1,2],[2,1,2],[1,5,3],[5,1,8],[7,2,1],[4,4,9],[3,1,9],[1,10,10]]
# output_m = [[0],[0],[0],[0],[1],[1],[1],[1],[1],[1]]
# test_m = [[1,2,1],[1,4,5],[1,4,9]]

# percy = Perceptron(3,1,0.3,100)
# percy.train(input_m, output_m)
# print(percy.test(test_m))














