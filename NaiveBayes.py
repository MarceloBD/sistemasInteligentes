# reference https://web.stanford.edu/class/cs124/lec/naivebayes.pdf

class NaiveBayes():

	def __init__(self, dictionary_of_classes, class_distribuition):
		self.dictionary_of_classes = dictionary_of_classes
		self.class_distribuition = class_distribuition
		self.counted_words = self.count_words()
		return

	def laplace(self, frequency_attribute_in_class, number_total_attributes_in_class, number_of_possibilities):
		# frequency attribute in class = number of times the words appears in class 
		# number of possibilities = vocabulary 
		# number total attributes in class = number of words in class 
		return (frequency_attribute_in_class + 1)/(number_total_attributes_in_class + number_of_possibilities)

	def probability_of_class(self, class_label, bag_of_words):
		p_class = self.class_distribuition[class_label]
		p_mul_attribute = 1
		for attribute in bag_of_words:
			p_mul_attribute *= self.conditional_probability(attribute, class_label)
		return p_class*p_mul_attribute

	def conditional_probability(self, attribute, class_label):
		#TODO: 
		#  use laplace smoothing
		counted_attribute = self.dictionary_of_classes[class_label].get(attribute, 1)
		return counted_attribute/self.counted_words[class_label]

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
		return p.index(max(p))