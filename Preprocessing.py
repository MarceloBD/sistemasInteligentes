import codecs
import string 
import glob
import copy as cp

MIN_WORD_LENGTH = 4

class Preprocessing():

	def __init__(self):
		self.dictionary = {'cbr':{},
							'ilp':{},
							'ri':{}}
		self.class_distribuition = {'cbr': 0,
							'ilp': 0,
							'ri': 0} 
		return

	def convert_all_files(self):
		filenames = glob.glob('files/*.txt')
		[self.execute(filename) for filename in filenames]  

	def execute(self, filename):
		new_filename = self.decode2utf8(filename)

		with open(new_filename) as file:
		    text = file.read()
		    text = self.remove_undesired_chars(text)
		    words = self.get_words(text, MIN_WORD_LENGTH)

		    out = codecs.open(new_filename, 'w', 'utf-8')
		    out.write('\n'.join(words))
		    
		    bag_of_words = self.make_bag_of_words(words)
		    self.make_dictionary(bag_of_words, new_filename)
		return bag_of_words

	def get_words(self, text, min_length):
		words = list(filter(lambda x: len(x) >= min_length, text.split(' ')))
		lowered_words = [word.lower() for word in words]
		return lowered_words

	def make_dictionary(self, bag_of_words, new_filename):
		 if(new_filename[0:18] == 'processedFiles/CBR'):
		 	self.class_distribuition['cbr'] += 1
		 	try:
		 		for key in bag_of_words:	
		 			self.dictionary['cbr'][key] = self.dictionary['cbr'].get(key, 0) + bag_of_words.get(key)

		 	except:
		 		pass
		 elif(new_filename[0:18] == 'processedFiles/ILP'):
		 	self.class_distribuition['ilp'] += 1
		 	try:
			 	for key in bag_of_words:	
			 		self.dictionary['ilp'][key] = self.dictionary['ilp'].get(key, 0) + bag_of_words.get(key)
		 	except:
		 		pass
		 else:
		 	self.class_distribuition['ri'] += 1
		 	try:
		 		for key in bag_of_words:	
		 			self.dictionary['ri'][key] = self.dictionary['ri'].get(key, 0) + bag_of_words.get(key)
		 	except:
		 		pass

	def decode2utf8(self, filename):
		file = codecs.open(filename, 'r', encoding='utf-8' , errors='ignore')
		raw = file.read() 
		new_filename = cp.deepcopy(filename)
		new_filename = new_filename.split('/')[1]
		new_filename = 'processedFiles/' + new_filename
		outFile = codecs.open(new_filename, 'w', 'utf-8')
		outFile.write(raw) 
		return new_filename


	def remove_undesired_chars(self, words):
		undesired_chars = ['\n', '(', ')', '[', ']', '.', ',', '"', "'",":", 
 		";", "\x0c", "\x0f", '\r', '\t', '-', '/', '0', '1', '2', 
    	'3', '4', '5', '6', '7', '8', '9', '{', '}', '@', '=',
    	'+', '"\"', '#', '\x18', '`', '*', '?','~','<','>',"\\"]
		for char in undesired_chars:
			words = words.replace(char, ' ')
		return words


	def make_bag_of_words(self, read_words):
		word_freq = {}

		while(len(read_words) > 0):
			actual_word = read_words[0]
			word_freq[actual_word] = 1	
			read_words.remove(actual_word)

			for another_word in read_words:
				if(another_word == actual_word):
					word_freq[actual_word] += 1
					read_words.remove(actual_word)

		return word_freq

	def print_dictionary(self):
		[print(item) for item in sorted(self.dictionary['cbr'].items())]
		print('----------------------------------------------------------')
		[print(item) for item in sorted(self.dictionary['ilp'].items())]
		print('----------------------------------------------------------')
		[print(item) for item in sorted(self.dictionary['ri'].items())]

	def get_dictionary(self):
		out = codecs.open('dictionary', 'w', 'utf-8')
		out.write('\n'.join(self.dictionary['cbr']))
		out.write('\n'.join(self.dictionary['ilp']))
		out.write('\n'.join(self.dictionary['ri']))
		return self.dictionary

	def get_class_distribuition(self):
		return self.class_distribuition



