import os
import pickle
import tarfile
import numpy as np
from dictionary.dictionary_analyzer import DictionariesAnalyzer, HOME


def put_in_polyglot_dict(words: list, values: list):
    result = (words, values)
    with open('./data/tmp/sentiment/pt/pt.sent.pkl', 'wb+') as extracted_old_dict:
        pickle.dump(result, extracted_old_dict)

    tar = tarfile.open(f"{HOME}/polyglot_data/sentiment2/pt/pt.sent.pkl.tar.bz2", "w")
    tar.add("./data/tmp/sentiment/pt/pt.sent.pkl")
    tar.close()


def add_liwc_words_into_polyglot_dict():
    '''Adds LIWC words into Polyglot's dictionary'''
    print('Adding LIWC words into Polyglot\'s dictionary...')

    d = DictionariesAnalyzer()

    liwc_words, liwc_values = d.get_words_and_values_from_liwc_dict() 
    polyglot_words, polyglot_values = d.get_words_and_values_from_polyglot_sentiment_dict()
    
    for i in range(len(liwc_words)):
        if liwc_words[i] not in polyglot_words:
            polyglot_words.extend([liwc_words[i]])
            polyglot_values.extend([liwc_values[i]])

    put_in_polyglot_dict(polyglot_words, polyglot_values)
    print('LIWC words added!')


def replace_polyglot_dict_by_liwc_dict():
    d = DictionariesAnalyzer()
    liwc_words, liwc_values = d.get_words_and_values_from_liwc_dict()
    put_in_polyglot_dict(liwc_words, liwc_values)


def generate_liwc_pkl_dictionary_file():   
    '''Generates a pkl file from the LIWC dictionary, is stored a dict object in the pkl file'''

    words = dict()
    with open('./data/dictionaries/liwc-sentiment.dic', 'r') as file:
        for line in file.readlines():
            word = line.split(' ')[0]
            str_word_sentiment_value = line.split(' ')[1]
            
            if '-' in str_word_sentiment_value:
                int_word_sentiment_value = int(str_word_sentiment_value[2:4])
                words[word] = np.array([int_word_sentiment_value])
            else:
                int_word_sentiment_value = int(str_word_sentiment_value[2])
                words[word] = np.array([int_word_sentiment_value])
    
    pkl_file = open('./liwc-semtiment.pkl', 'wb')
    pickle.dump(words, pkl_file)
    pkl_file.close()


def generate_polyglot_txt_dictionary_file():
    '''Generates a txt file from the Polyglot dictionary'''

    analyzer = DictionariesAnalyzer()
    words, values = analyzer.get_words_and_values_from_polyglot_sentiment_dict()

    with open('./data/dictionaries/polyglot-sentiment.dic', 'w') as file:
        index = 0
        for word in words:
            line = f'{word} {values[index]}\n'
            file.write(line)
            index += 1
