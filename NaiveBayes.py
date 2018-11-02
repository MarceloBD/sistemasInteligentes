# reference https://web.stanford.edu/class/cs124/lec/naivebayes.pdf

class NaiveBayes():

	def __init__(self, dictionary_of_classes):
		self.dictionary_of_classes = dictionary_of_classes
		self.count_words = self.count_words()
		return

	def laplace(self, frequency_attribute_in_class, number_total_attributes_in_class, number_of_possibilities):
		# frequency attribute in class = number of times the words appears in class 
		# number of possibilities = vocabulary 
		# number total attributes in class = number of words in class 
		return (frequency_attribute_in_class + 1)/(number_total_attributes_in_class + number_of_possibilities)

	def probability_of_class(self, class_label, bag_of_words, class_distribuition):
		p_class = class_distribuition(class_label)
		p_mul_attribute = 1
		for word in bag_of_words:
			p_mul_attribute *= conditional_probability(attribute, class_label)
		return p_class*p_mul_attribute

	def conditional_probability(self, attribute, class_label):
		#TODO: 
		#  use laplace smoothing
		counted_attribute = self.dictionary_of_classes[class_label][attribute]
		return count_attribute/self.counted_words[class_label]

	def count_words(self):
		count_words = {}
		counted_words['cbr'] = sum(self.dictionary_of_classes['cbr'].values())
		counted_words['ilp'] = sum(self.dictionary_of_classes['ilp'].values())
		counted_words['ir'] = sum(self.dictionary_of_classes['ir'].values())
		return count_words

	def classify(self, bag_of_words, class_distribuition):
		p_cbr = self.probability_of_class('cbr', bag_of_words, class_distribuition)
		p_ilp = self.probability_of_class('ilp', bag_of_words, class_distribuition)
		p_ir = self.probability_of_class('ir', bag_of_words, class_distribuition)

		p = [p_cbr, p_ilp, p_ir]
		return p.index(max(p))


