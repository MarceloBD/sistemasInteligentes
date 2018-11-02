class NaiveBayes():

	def __init__(self):
		return

	def laplace(self, number_examples_in_class , number_total_examples_of_class, number_of_possibilities):
		return (number_examples_in_class + 1)/(number_total_examples_of_class + number_of_possibilities)

	def probability_of_class(self, class_label, bag_of_words, class_distribuition):
		p_class = class_distribuition(class_label)
		p_mul_attribute = 1
		for word in bag_of_words:
			p_mul_attribute *= conditional_probability(attribute, class_label)
		return p_class*p_mul_attribute

	def conditional_probability(self, attribute, class_label):
		#TODO: get conditional probability from all data  
		# and case when is needed to use laplace smoothing
		return 

	def classify(self, bag_of_words, class_distribuition):
		p_cbr = self.probability_of_class('cbr', bag_of_words, class_distribuition)
		p_il = self.probability_of_class('il', bag_of_words, class_distribuition)
		p_pir = self.probability_of_class('pir', bag_of_words, class_distribuition)

		p = [p_cbr, p_il, p_pir]
		return p.index(max(p))