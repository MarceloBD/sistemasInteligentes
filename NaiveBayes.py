# reference https://web.stanford.edu/class/cs124/lec/naivebayes.pdf
import numpy as np 

class NaiveBayes():

	def __init__(self, dictionary_of_classes, class_distribuition):
		self.dictionary_of_classes = dictionary_of_classes
		self.class_distribuition = class_distribuition
		self.counted_words = self.count_words()
		self.conditional_probability = self.smooth_dictionary()
		return

	def smooth_dictionary(self):
		vocabulary = {}
		conditional_probability = {'cbr':{},
							'ilp':{},
							'ri':{}}
		for word in self.dictionary_of_classes['cbr']:
			vocabulary[word] = 0
		for word in self.dictionary_of_classes['ilp']:
			vocabulary[word] = 0
		for word in self.dictionary_of_classes['ri']:
			vocabulary[word] = 0

		for word in vocabulary:
			conditional_probability['cbr'][word] = self.laplace(self.dictionary_of_classes['cbr'].get(word, 0), len(self.dictionary_of_classes['cbr']), len(vocabulary)) 
			conditional_probability['ilp'][word] = self.laplace(self.dictionary_of_classes['ilp'].get(word, 0), len(self.dictionary_of_classes['ilp']), len(vocabulary))
			conditional_probability['ri'][word] = self.laplace(self.dictionary_of_classes['ri'].get(word, 0), len(self.dictionary_of_classes['ri']), len(vocabulary))
		return conditional_probability

	def laplace(self, frequency_attribute_in_class, number_total_attributes_in_class, number_of_possibilities):
		# frequency attribute in class = number of times the word appears in class 
		# number of possibilities = vocabulary 
		# number total attributes in class = number of words in class 
		return np.log((frequency_attribute_in_class + 1)/(number_total_attributes_in_class + number_of_possibilities))

	def probability_of_class(self, class_label, bag_of_words):
		p_class = self.class_distribuition[class_label]
		p_mul_attribute = 0
		for attribute in bag_of_words:
			p_mul_attribute += self.conditional_probability[class_label][attribute]
		
		return np.log(p_class)+p_mul_attribute

	#def conditional_probability(self, attribute, class_label):
	#	counted_attribute = self.dictionary_of_classes[class_label][attribute]
	#	return counted_attribute/self.counted_words[class_label]

	def count_words(self):
		counted_words = {}
		counted_words['cbr'] = sum(self.dictionary_of_classes['cbr'].values())
		counted_words['ilp'] = sum(self.dictionary_of_classes['ilp'].values())
		counted_words['ri'] = sum(self.dictionary_of_classes['ri'].values())
		return counted_words

	def classify(self, bag_of_words):
		p_cbr = self.probability_of_class('cbr', bag_of_words)
		p_ilp = self.probability_of_class('ilp', bag_of_words)
		p_ir = self.probability_of_class('ri', bag_of_words)

		p = [p_cbr, p_ilp, p_ir]
		print(p)
		return p.index(max(p))