import codecs
import string 
import glob
import copy as cp

class Preprocessing():

	def __init__(self):
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
		    if(new_filename == 'processedFiles/CBR-837Aam274-288.txt'):
		    	self.make_bag_of_words(words)

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
		words = []
		frequencies = []
		
		
		while(len(read_words) > 0):
			actual_word = read_words[0]
			words.append(actual_word)
			read_words.remove(actual_word)
			frequencies.append(1)
			for another_word in read_words:
				if(another_word == actual_word):
					frequencies[-1] += 1
					read_words.remove(actual_word)
		for i in range(len(words)):
			print(words[i], frequencies[i]) 




