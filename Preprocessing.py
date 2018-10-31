import codecs
import string 
class Preprocessing():

	def __init__(self):
		return

	def execute(self):
		file = codecs.open('files/CBR-837Aam274-288.txt', 'r', 'cp1251')
		u = file.read()   # now the contents have been transformed to a Unicode string
		out = codecs.open('processedFiles/CBR-837Aam274-288.txt', 'w', 'utf-8')
		out.write(u)   # and now the contents have been output as UTF-8

		with open('files/CBR-837Aam274-288-UTF8.txt') as file:
		    words = [word for line in file for word in line.split()]
		    words = self.remove_final_ponctuation(words)
		    words = list(filter(None, words)) 
		    words = self.delete_lower_than(words, 4)
		    out = codecs.open('processedFiles/CBR-837Aam274-288.txt', 'w', 'utf-8')
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
		file_name = 'processedFiles/CBR-837Aam274-288.txt'
		file = codecs.open(file_name, 'r', 'utf-8')
		data = file.read()
		print(data)