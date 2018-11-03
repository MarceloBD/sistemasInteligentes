from os import listdir
from os.path import isfile, join
import codecs
from itertools import groupby

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
            '+', '"\"', '#', '\x18', '`', '*', '?']
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



bag_of_words = make_bag_of_words(FILES_PATH, MIN_WORD_LENGTH)
folds = make_folds(bag_of_words, 10)
