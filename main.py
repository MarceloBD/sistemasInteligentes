from os import listdir
from os.path import isfile, join
import codecs
from itertools import groupby
import numpy as np

FILES_PATH = "./files"
MIN_WORD_LENGTH = 4

def get_file_class(filename):
    return filename.split("-")[0]

def get_filenames(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def open_file(filename, path):
    return codecs.open(f'{path}/{filename}', "r",encoding='utf-8', errors='ignore') 

def open_and_process_files(filenames, path):
    for filename in filenames:
        with open_file(filename, path) as file:
            text = file.read()
            text = remove_undesired_chars(text)
            get_words(file)
            file.close()

def remove_undesired_chars(text):
    undesired_chars = ['\n', '(', ')', '[', ']', '.', ',', '"', "'",
            ":", ";", "\x0c", "\x0f", '\r', '\t', '-', '/', '0', '1', '2', 
            '3', '4', '5', '6', '7', '8', '9', '{', '}', '@', '=',
            '+', '"\"', '#', '\x18', '`', '*', '?', '<', '>', '_', '!',
            '\bad', '\boosting', '\communication', '\gamma', '\good',
            '\lambda', '\omega', '\gamma', '\phi', '\phil', '\station',
            '\seed', '\sigma', '\weak', '\yes', '%', '', '', '',
            '~', '^']
    for char in undesired_chars:
        text = text.replace(char, ' ')
    return text

def get_words(text, min_length):
    words = list(filter(lambda x: len(x) >= min_length, text.split(' ')))
    lowered_words = [word.lower() for word in words]
    return lowered_words

def get_word_frequencies(words):
    words.sort()
    frequency_list = [{word: len(list(appearences))} for word, appearences in groupby(words)]
    frequency_dict = {}
    for word in frequency_list:
        key = list(word.keys())[0]
        frequency_dict[key] = word[key]
    return frequency_dict

def bag_of_words_insert(bag_of_words, filename, classname, word_frequencies):
    bag_of_words[filename] = {
        'class': classname,
        'filename': filename,
        'words': word_frequencies
    }



def make_bag_of_words(files_path, min_word_length):
    bag_of_words = {}
    filenames = get_filenames(files_path)
    for filename in filenames:
        with open_file(filename, files_path) as file:
            raw_text = file.read()
            processed_text = remove_undesired_chars(raw_text)
            words = get_words(processed_text, min_word_length)
            word_frequencies = get_word_frequencies(words)
            classname = get_file_class(filename)
            bag_of_words_insert(bag_of_words, filename, classname, word_frequencies)
    return bag_of_words


def make_vocabulary(bag_of_words):
    vocabulary_dict = {}
    for doc_name in bag_of_words:
        doc = bag_of_words[doc_name]
        for word in doc['words']:
            vocabulary_dict[word] = True
    vocabulary_list = []
    for word in vocabulary_dict:
        vocabulary_list.append(word)
    vocabulary_list.sort()
    #Gamb
    vocabulary_list = vocabulary_list[8:]
    return vocabulary_list

def make_class_vocabulary(bag_of_words, classname):
    vocabulary_dict = {}
    for doc_name in bag_of_words:
        doc = bag_of_words[doc_name]
        if doc['class'] == classname:
            for word in doc['words']:
                vocabulary_dict[word] = True
    vocabulary_list = []
    for word in vocabulary_dict:
        vocabulary_list.append(word)
    vocabulary_list.sort()
    #Gamb
    vocabulary_list = vocabulary_list[8:]
    return vocabulary_list

def get_all_classes(bag_of_words):
    classes_dict = {}
    for doc_name in bag_of_words:
        doc = bag_of_words[doc_name]
        classes_dict[doc['class']] = True
    classes_list = []
    for classname in classes_dict:
        classes_list.append(classname)
    return classes_list


def make_folds(bag_of_words, size):
    classes = get_all_classes(bag_of_words)
    corpus = {}
    for classname in classes:
        corpus[classname] = []
    for doc_name in bag_of_words:
        doc = bag_of_words[doc_name]
        corpus[doc['class']].append(doc)
    slices = []
    for i in range(size):
        slices.append({})
        for classname in classes:
            class_size = len(corpus[classname])
            for doc in corpus[classname][round((i/size)*class_size):round(((i+1)/size)*class_size)]:
                slices[i][doc['filename']] = doc
    folds = []
    for i in range(size):
        training_docs_dict = {}
        training_docs_list = slices[:i] + slices[i+1:]
        for slc in training_docs_list:
            training_docs_dict = dict(training_docs_dict, **slc)
        fold = {
                'training': training_docs_dict,
                'testing': slices[i]
                }
        folds.append(fold)
    return folds


def generate_arff(bag_of_words, vocabulary):
    with open("data.arff", "w") as file:
        file.write("@RELATION texts\n\n")
        for word in vocabulary:
            file.write("@ATTRIBUTE " + word + " NUMERIC\n")
        file.write("@ATTRIBUTE _class {CBR,ILP,RI}\n\n")


        file.write("@DATA\n")
        for filename in bag_of_words:
            line = ""
            doc = bag_of_words[filename]
            for word in vocabulary:
                line = line + str(doc['words'].get(word, 0)) + ','
            line = line + doc['class'] + '\n'
            file.write(line)
        file.close()

def get_classes_occurrencies(bag_of_words):
    classes = get_all_classes(bag_of_words)
    occurrencies = {}
    for classname in classes:
        occurrencies[classname] = 0
    for filename in bag_of_words:
        doc = bag_of_words[filename]
        occurrencies[doc['class']] += 1
    return occurrencies

def make_bag_of_words_by_class(bag_of_words):
    classes = get_all_classes(bag_of_words)
    bow_class = {} 
    for cname in classes:
        bow_class[cname] = {}
    for filename in bag_of_words:
        doc = bag_of_words[filename]
        for word in doc['words']:
            bow_class[doc['class']][word] = bow_class[doc['class']].get(word,0) + doc['words'][word]
    return bow_class


def get_probabilities(bag_of_words):
    vocabulary = make_vocabulary(bag_of_words)
    class_occurrencies = get_classes_occurrencies(bag_of_words)
    classes = get_all_classes(bag_of_words)
    class_vocabulary = {}
    class_probability = {}
    probability_word_given_class = {}
    bag_of_words_by_class = make_bag_of_words_by_class(bag_of_words)
    for classname in classes:
        probability_word_given_class[classname] = {}
        class_vocabulary[classname] = make_class_vocabulary(bag_of_words, classname)
        class_probability[classname] = class_occurrencies[classname] / len(bag_of_words)
        for word in vocabulary:
            word_occurrencies = bag_of_words_by_class[classname].get(word, 0)
            probability_word_given_class[classname][word] = (word_occurrencies + 1)/(len(vocabulary) + len(bag_of_words_by_class[classname]))
    return class_probability, probability_word_given_class


    
def classify(filename, bag_of_words, class_probability, probability_word_given_class):
    bag_of_words = make_bag_of_words(FILES_PATH, MIN_WORD_LENGTH)
    bag_of_words_by_class = make_bag_of_words_by_class(bag_of_words)
    vocabulary = make_vocabulary(bag_of_words)
    #generate_arff(bag_of_words, vocabulary)
    classes = get_all_classes(bag_of_words)
    probabilities = []
    for classname in classes:
        class_vocabulary = make_class_vocabulary(bag_of_words, classname)
        aux = 0
        for word in bag_of_words[filename]['words']:
            p_word = probability_word_given_class[classname].get(word, 1 / (len(vocabulary) + len(bag_of_words_by_class[classname])))
            aux += np.log10(p_word)
        probabilities.append(np.log10(class_probability[classname]) + aux)
    return classes[probabilities.index(max(probabilities))]



bag_of_words = make_bag_of_words(FILES_PATH, MIN_WORD_LENGTH)
folds = make_folds(bag_of_words, 10)
guessed_right = 0
guessed_wrong = 0
for fold in folds:
    class_probability, probability_word_given_class = get_probabilities(fold['training'])
    for filename in fold['testing']:
        print("text: " + filename)
        result = classify(filename, fold['testing'], class_probability, probability_word_given_class)
        if result == fold['testing'][filename]['class']:
            guessed_right += 1
        else:
            guessed_wrong += 1
        print("guessed: " + result)
        print(f"Right: {guessed_right}, wrong: {guessed_wrong}, precision: {guessed_right/(guessed_right+guessed_wrong)}")

