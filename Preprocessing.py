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
		newFilename = self.decode2utf8(filename)

		with open(newFilename) as file:
		    words = [word for line in file for word in line.split()]
		    words = self.apply_filters(words)
		    
		    out = codecs.open(newFilename, 'w', 'utf-8')
		    out.write('\n'.join(words))
	
	def decode2utf8(self, filename):
		file = codecs.open(filename, 'r', 'cp1251')
		try:
			raw = file.read() 
		except:
			file = codecs.open(filename, 'r', 'koi8-r')
			raw = file.read() 
		newFilename = cp.deepcopy(filename)
		newFilename = newFilename.split('/')[1]
		newFilename = 'processedFiles/' + newFilename
		outFile = codecs.open(newFilename, 'w', 'utf-8')
		outFile.write(raw) 
		return newFilename

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