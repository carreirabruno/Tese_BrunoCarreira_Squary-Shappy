from random import random, uniform
from math import exp



class MultiLayeredPerceptron:

	def __init__(self, num_inputs, num_outputs, hidden_layer_vector, learning_rate, epochs):

		self.epochs = epochs
		prov_telo_dendrites = []
		self.output_dendrites = []
		self.input_axons = []
		self.neurons = []

		prev_layer = []
		current_layer = []

		prov_telo_dendrites = []
		for i in range(num_inputs):
			for hidden_j in range(hidden_layer_vector[0]):
				prov_telo_dendrites.append(Telo_dendrite(0))

			self.input_axons.append(Axon(prov_telo_dendrites))
			prov_telo_dendrites = []


		prov_telo_dendrites = []   # I think this can be removeds
		prov_dendrites = []
		prov_neuron = None
		for n_num in range(hidden_layer_vector[0]):
			for hidden_j in range(hidden_layer_vector[1]):
				prov_telo_dendrites.append(Telo_dendrite(0))
			for in_axon in self.input_axons:
				prov_dendrites.append(Dendrite(in_axon.telo_dendrites[n_num]))
			prov_axon = Axon(prov_telo_dendrites)
			prov_neuron = Neuron(prov_dendrites, prov_axon, learning_rate)
			prov_telo_dendrites = []
			prov_dendrites = []
			current_layer.append(prov_neuron)

		self.neurons.append(current_layer)


		for position, layer in enumerate(hidden_layer_vector[1:]):

			prev_layer = current_layer
			current_layer = []

			for n_num in range(layer):
				if (position + 2) >= len(hidden_layer_vector):
					for hidden_j in range(num_outputs):
						prov_telo_dendrites.append(Telo_dendrite(0))
				else:
					for hidden_j in range(hidden_layer_vector[position + 2]):
						prov_telo_dendrites.append(Telo_dendrite(0))
				for prev_neuron in prev_layer:
					prov_dendrites.append(Dendrite(prev_neuron.axon.telo_dendrites[n_num-1]))
				prov_axon = Axon(prov_telo_dendrites)
				prov_neuron = Neuron(prov_dendrites, prov_axon, learning_rate)
				prov_telo_dendrites = []
				prov_dendrites = []
				current_layer.append(prov_neuron)

			self.neurons.append(current_layer)

		prov_telo_dendrites = []
		prov_dendrites = []
		prev_layer = current_layer
		current_layer = []

		for i in range(num_outputs):

			for prev_neuron in prev_layer:
				prov_dendrites.append(Dendrite(prev_neuron.axon.telo_dendrites[i]))

			prov_telo = Telo_dendrite(1)
			prov_axon = Axon([prov_telo])
			prov_neuron = Neuron(prov_dendrites, prov_axon, learning_rate)
			self.output_dendrites.append(Dendrite(prov_telo))
			current_layer.append(prov_neuron)

		self.neurons.append(current_layer)




	def train(self, inputs, outputs):

		for epoch in range(self.epochs):
			print("Training epoch:")
			print(epoch)
			instance_num = 0
			for instance in inputs:
				output_num = 0
				for output_value in outputs[instance_num]:
					self.output_dendrites[output_num].telo_dendrite.expected_value = output_value
					output_num += 1
				input_num = 0
				for input_value in instance:
					self.input_axons[input_num].sinapse(input_value)
					input_num += 1

				for layer in self.neurons:
					for neuri in layer:
						neuri.sinapse()

				for layer in reversed(self.neurons):
					for neuri in layer:
						neuri.back_propagate()
				instance_num += 1


	def test(self, inputs):

		output = []
		for instance in inputs:

			input_num = 0
			for input_value in instance:
				self.input_axons[input_num].sinapse(input_value)
				input_num += 1

			for layer in self.neurons:
				for neuri in layer:
					neuri.sinapse()

			prov_output = []
			for o_dendrite in self.output_dendrites:
				prov_output.append(o_dendrite.input_value)

			output.append(prov_output)

		return output



	def printNetwork(self):

		count = 1
		for layer in self.neurons:
			print("Layer: " + str(count))
			for neuron in layer:
				print("	Neuron: ")
				print(neuron)

				print("		" + "Is connected to: ")
				for telo in neuron.axon.telo_dendrites:
					print(telo.dendrite.neuron)
					print("		" + "With the weight: ")
					print(telo.dendrite.weight)
					print(telo.dendrite.input_value)

			count += 1

class Perceptron:

	def __init__(self, num_inputs, num_outputs, learning_rate, epochs):

		self.epochs = epochs
		prov_dendrites = []
		prov_telo_dendrites = []
		self.output_dendrites = []
		for i in range(num_inputs):
			prov_dendrites.append(Dendrite(None))

		for i in range(num_outputs):
			prov_telo_dendrites.append(Telo_dendrite(1))
			self.output_dendrites.append(Dendrite(prov_telo_dendrites[i]))
			

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

	def printPerceptron(self):

		print("	Neuron: ")
		print(self.neuron)

		print("		" + "Has this dendrite: ")
		for dendrite in self.neuron.dedrites:
			print(dendrite)
			print("		" + "With the weight: ")
			print(dendrite.weight)

	def printOrderedWeights(self):

		weights = []
		count = 0
		for dendrite in self.neuron.dendrites:
			weights.append([dendrite.weight, count])
			count += 1

		res = sorted(weights, key=lambda x: x[0])
		print(res)
		return res



class Neuron:

	def __init__(self, dendrites, axon, learning_rate):

		self.dendrites = dendrites
		for dendrite in dendrites:
			dendrite.neuron = self
		self.axon = axon
		for telo_dendrite in axon.telo_dendrites:
			telo_dendrite.neuron = self
		self.b_potential = uniform(-0.3,0.3)
		self.learning_rate = learning_rate




	def activation_function(self, potential):

		print(potential)
		print(exp(-(2*potential)))
		return (2.0/(1.0 + exp(-(2*potential)))) -1

		#return (1.0 - exp(-potential))/(1.0 + exp(-potential))




	def sinapse(self):

		potential = self.b_potential

		for dendrite in self.dendrites:
			potential += dendrite.weight * dendrite.input_value
		self.axon.sinapse(self.activation_function(potential))
		return self.activation_function(potential)

	def fake_sinapse(self):

		potential = self.b_potential

		for dendrite in self.dendrites:
			potential += dendrite.weight * dendrite.input_value
		return self.activation_function(potential)

	def deep_learn(self):


		for telo in self.axon.telo_dendrites:

			error = telo.dendrite.neuron.deep_learn()
			#telo.dendrite.weight += telo.dendrite.neuron.deep_learn()


	def back_propagate(self):

		prov_expected = 0

		count = 0
		for telo_dendrite in self.axon.telo_dendrites:
			count += 1
			prov_expected += telo_dendrite.expected_value

		expected = prov_expected/count

		for dendrite in self.dendrites:
			dendrite.telo_dendrite.expected_value = expected

		obtained = self.fake_sinapse()

		error = expected - obtained
		self.b_potential += self.learning_rate * error

		for dendrite in self.dendrites:
			dendrite.gradient += self.learning_rate * error * dendrite.input_value
			dendrite.weight += dendrite.gradient



	def learn(self):

		obtained = self.fake_sinapse()

		error = self.axon.expected() - obtained
		self.b_potential += self.learning_rate * error

		for dendrite in self.dendrites:
			dendrite.gradient += self.learning_rate * error * dendrite.input_value
			dendrite.weight += dendrite.gradient
	 # WAS: 
		# for dendrite in self.dendrites:
		# 	dendrite.weight += self.learning_rate * error * dendrite.input_value


	def expected(self):
		return self.axon.expected()







class Dendrite:

	def __init__(self, telo_dendrite):
		self.weight = uniform(-0.3,0.3)
		self.input_value = 0
		self.neuron = None
		self.telo_dendrite = telo_dendrite
		if telo_dendrite != None:
			self.telo_dendrite.dendrite = self
		self.gradient = 0


	def expected(self):
		return self.neuron.expected()



class Telo_dendrite:

	def __init__(self, is_output):
		self.neuron = None
		self.dendrite = None
		self.is_output = is_output
		self.expected_value = 0

	def expected(self):
		if self.is_output:
			return self.expected_value
		else:
			######################################  Here we might have the backpropagation taking place
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
#			if telo_dendrite.is_output != 1:
#				telo_dendrite.dendrite.neuron.sinapse()     ################ Might have to change this




input_m = [[1,2,1],[2,1,1],[3,1,2],[2,1,2],[1,5,3],[5,1,8],[7,2,1],[4,4,9],[3,1,9],[1,10,10]]
output_m = [[0],[0],[0],[0],[1],[1],[1],[1],[1],[1]]
test_m = [[1,2,1],[1,4,5],[1,4,9]]

percy = Perceptron(3,1,0.3,100)
percy.train(input_m, output_m)
print(percy.test(test_m))














