from Preprocessing import Preprocessing
from NaiveBayes import NaiveBayes

if __name__ == '__main__':
	prep = Preprocessing()
	prep.convert_all_files()
	prep.print_dictionary()

	naiveb = NaiveBayes(prep.get_dictionary(), prep.get_class_distribuition())
	prep2 = Preprocessing()
	class_found = naiveb.classify(prep2.execute('processedFiles/CBR-837Aam274-288.txt'))
	print(class_found)
