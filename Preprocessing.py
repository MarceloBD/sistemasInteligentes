import codecs
import string 
import glob
import copy as cp

class Preprocessing():

	def __init__(self):
		self.dictionary = {'cbr':{},
							'ilp':{},
							'ri':{}}
		return

	def convert_all_files(self):
		filenames = glob.glob('files/*.txt')
		[self.execute(filename) for filename in filenames]  

	def execute(self, filename):
		new_filename = self.decode2utf8(filename)

		with open(new_filename) as file:
		    words = [word for line in file for word in line.split()]
		    words = self.apply_filters(words)
		    
		    out = codecs.open(new_filename, 'w', 'utf-8')
		    out.write('\n'.join(words))
		    
		    bag_of_words = self.make_bag_of_words(words)
		    self.make_dictionary(bag_of_words, new_filename)

		    

	def make_dictionary(self, bag_of_words, new_filename):
		 if(new_filename[0:18] == 'processedFiles/CBR'):
		 	try:
		 		for key in bag_of_words:	
		 			self.dictionary['cbr'][key] = self.dictionary['cbr'].get(key, 0) + bag_of_words.get(key)

		 	except:
		 		pass
		 elif(new_filename[0:18] == 'processedFiles/ILP'):
		 	try:
			 	for key in bag_of_words:	
			 		self.dictionary['ilp'][key] = self.dictionary['ilp'].get(key, 0) + bag_of_words.get(key)
		 	except:
		 		pass
		 else:
		 	try:
		 		for key in bag_of_words:	
		 			self.dictionary['ri'][key] = self.dictionary['ri'].get(key, 0) + bag_of_words.get(key)
		 	except:
		 		pass

	def decode2utf8(self, filename):
		file = codecs.open(filename, 'r', 'cp1251')
		try:
			raw = file.read() 
		except:
			file = codecs.open(filename, 'r', 'koi8-r')
			raw = file.read() 
		new_filename = cp.deepcopy(filename)
		new_filename = new_filename.split('/')[1]
		new_filename = 'processedFiles/' + new_filename
		outFile = codecs.open(new_filename, 'w', 'utf-8')
		outFile.write(raw) 
		return new_filename

	def apply_filters(self, words):
		words = self.remove_terminal_ponctuation(words)
		words = list(filter(None, words)) 
		words = self.delete_lower_than(words, 4)
		return words

	def remove_terminal_ponctuation(self, words):
		words = [word.rstrip(string.punctuation) for word in words]
		words = [word[::-1].rstrip(string.punctuation) for word in words]
		return [word[::-1] for word in words]

	def delete_lower_than(self, words, length):
		remove = []
		for i in range(len(words)):
			if(len(words[i]) < 4):
				remove.append(words[i])
		for i in range(len(remove)):
				words.remove(remove[i])
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