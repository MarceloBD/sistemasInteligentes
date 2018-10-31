import codecs
import string 
import glob
import copy as cp

class Preprocessing():

	def __init__(self):
		return

	def execute(self, filename):
		file = codecs.open(filename, 'r', 'cp1251')
		#print(filename)
		try:
			u = file.read()   # now the contents have been transformed to a Unicode string
		except:
			file = codecs.open(filename, 'r', 'koi8-r')
			u = file.read() 
		newFilename = cp.deepcopy(filename)
		newFilename = newFilename.split('/')[1]
		newFilename = 'processedFiles/' + newFilename
		print(newFilename)
		out = codecs.open(newFilename, 'w', 'utf-8')
		out.write(u)   # and now the contents have been output as UTF-8

		with open(newFilename) as file:
		    words = [word for line in file for word in line.split()]
		    words = self.remove_final_ponctuation(words)
		    words = list(filter(None, words)) 
		    words = self.delete_lower_than(words, 4)
		    out = codecs.open(newFilename, 'w', 'utf-8')
		    out.write('\n'.join(words))

	def remove_final_ponctuation(self, words):
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

	def read(self, file_name):
		file = codecs.open(file_name, 'r', 'utf-8')
		data = file.read()
		print(data)

	def convert_all_files(self):
		filenames = glob.glob('files/*.txt')
		[self.execute(filename) for filename in filenames]  