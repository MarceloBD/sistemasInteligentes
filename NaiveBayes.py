# reference https://web.stanford.edu/class/cs124/lec/naivebayes.pdf

class NaiveBayes():

	def __init__(self, dictionary_of_classes):
		self.dictionary_of_classes = dictionary_of_classes
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
		#TODO: get conditional probability from all data  
		# and case when is needed to use laplace smoothing
		counted_attribute = self.count_attribute(attribute, class_label)
		counted_words = self.count_words(class_label)
		return count_attribute/count_words

	def count_words(self, class_label):


	def classify(self, bag_of_words, class_distribuition):
		p_cbr = self.probability_of_class('cbr', bag_of_words, class_distribuition)
		p_il = self.probability_of_class('il', bag_of_words, class_distribuition)
		p_pir = self.probability_of_class('pir', bag_of_words, class_distribuition)

		p = [p_cbr, p_il, p_pir]
		return p.index(max(p))


