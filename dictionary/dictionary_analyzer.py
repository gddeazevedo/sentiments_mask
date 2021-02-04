import os
import csv
import pickle
import tarfile
from tabulate import tabulate
from polyglot.downloader import downloader
from polyglot.text import Text


HOME = os.environ['HOME']


def get_dataset() -> list:
    dataset = []
    with open('./data/dataset.csv', 'r+', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            dataset.append(row[2:])

    return dataset


def get_phrases_by_polarity() -> dict:
    dataset = get_dataset()

    phrases_by_polarity = {
        'positive': [],
        'negative': [],
        'neuter': []
    }

    for data in dataset:
        phrase = data[0]
        polarity = int(data[1])

        if polarity == 1:
            phrases_by_polarity['positive'].append(phrase)
        elif polarity == -1:
            phrases_by_polarity['negative'].append(phrase)
        else:
            phrases_by_polarity['neuter'].append(phrase)

    return phrases_by_polarity


def compare_dict_polarity_with_dataset_polarity():
    phrases_by_polarity = get_phrases_by_polarity()

    headers = ['T Positivo', 'T Negativo', 'T Neutro']
    rows = [
        ['D Positivo', 0, 0, 0],
        ['D Negativo', 0, 0, 0],
        ['D Neutro', 0, 0, 0],
        ['D Erros', 0, 0, 0],
        ['Total']
    ]

    i = 1

    for polarity in ('positive', 'negative', 'neuter'):
        rows[-1].append(len(phrases_by_polarity[polarity]))
        for phrase in phrases_by_polarity[polarity]:
            text = Text(phrase)
            try:
                if text.polarity == 1:
                    rows[0][i] += 1
                elif text.polarity == -1:
                    rows[1][i] += 1
                else:
                    rows[2][i] += 1
            except:
                rows[3][i] += 1

        i += 1
    
    print(tabulate(rows, headers=headers))


class DictionariesAnalyzer:
    '''A class that analyzes the LIWC and the Polyglot's dictionary'''
    
    def __init__(self, language_code: str='pt'):
        self.__polyglot_path = f'{HOME}/polyglot_data/sentiment2/pt/pt.sent.pkl.tar.bz2'
        self.__liwc_path = './data/dictionaries/liwc-sentiment.pkl'
        self.__language_code = language_code
        self.liwc_dict = dict()
        self.polyglot_dict = dict()
        self.__init_liwc_and_polyglot_dict_structure()

    def __init_liwc_and_polyglot_dict_structure(self):
        polyglot_words, polyglot_values = self.get_words_and_values_from_polyglot_sentiment_dict()
        liwc_words, liwc_values = self.get_words_and_values_from_liwc_dict()

        index = 0
        for polyglot_word in polyglot_words:    
            self.polyglot_dict[polyglot_word] = polyglot_values[index]
            index += 1

        index = 0
        for liwc_word in liwc_words:
            self.liwc_dict[liwc_word] = liwc_values[index]
            index += 1
    
    def get_words_from_polyglot_sentiment_dict(self) -> list:
        if not os.path.exists(self.__polyglot_path):
            self.dowload_polyglot_sentiment_model(self.__language_code)

        tar = tarfile.open(self.__polyglot_path)
        tar.extractall()
        tar.close()
        with open('./data/tmp/sentiment/pt/pt.sent.pkl', 'rb') as f:
            pkl_file = pickle.Unpickler(f, encoding="latin1")
            words, _ = pkl_file.load()
            return list(words)

    def get_words_and_values_from_polyglot_sentiment_dict(self) -> (list, list):
        if not os.path.exists(self.__polyglot_path):
            self.dowload_polyglot_sentiment_model(self.__language_code)

        tar = tarfile.open(self.__polyglot_path)
        tar.extractall()
        tar.close()
        with open('./data/tmp/sentiment/pt/pt.sent.pkl', 'rb') as f:
            pkl_file = pickle.Unpickler(f, encoding="latin1")
            words, values = pkl_file.load()
            return list(words), list(values)

    def get_words_from_liwc_dict(self) -> list:
        pkl_file = open(self.__liwc_path, 'rb')
        words = pickle.load(pkl_file)
        pkl_file.close()
        return list(words.keys())

    def get_words_and_values_from_liwc_dict(self) -> (list, list):
        pkl_file = open(self.__liwc_path, 'rb')
        words = pickle.load(pkl_file)
        pkl_file.close()
        return list(words.keys()), list(words.values())

    def print_liwc_and_polyglot_statistics(self):
        polyglot_words = self.get_words_from_polyglot_sentiment_dict()
        liwc_words = self.get_words_from_liwc_dict()

        print(f"Quantity of words in Polyglot's dictionary: {len(polyglot_words)}")
        print(f"Quantity of words in LIWC's dictionary: {len(liwc_words)}")

        polyglot_words_set = set(polyglot_words)
        liwc_words_set = set(liwc_words)

        print(f"Quantity of words in LIWC but not in Polyglot: {len(liwc_words_set.difference(polyglot_words_set))}")
        print(f"Quantity of words in Polyglot but not in LIWC: {len(polyglot_words_set.difference(liwc_words_set))}")
        print(f"Quantity of words in LIWC and in Polyglot: {len(polyglot_words_set.intersection(liwc_words_set))}")
        print(f"Quantity of words in LIWC or in Polyglot: {len(polyglot_words_set.union(liwc_words_set))}")

    def dowload_polyglot_sentiment_model(self, language_code: str=None):
        language_code = self.__language_code or language_code
        downloader.download(f"sentiment2.{language_code}")

    def print_polyglot_sentiment_dict(self):
        for word, value in self.polyglot_dict.items():
            print(f'{word} {value}')

    def print_liwc_dict(self):
        for word, value in self.liwc_dict.items():
            print(f'{word} {value}')

    def __print_words_and_liwc_and_polyglot_polarity(self, text: str, words: list):
        print(text)
        print('{:<16}{:<16}{}'.format('Word', 'LIWC', 'Polyglot') + '\n' + '-'*50)
        for word in words:
            liwc_polarity = self.liwc_dict[word][0]
            polyglot_polarity = self.polyglot_dict[word][0]
            print('{:<16}{:<16}{:>2}'.format(word, liwc_polarity, polyglot_polarity))

    def compare_liwc_and_polyglot_common_words_polarity(self):
        words_with_same_polarity = []
        words_with_different_polarity = []

        for key, value in self.liwc_dict.items():
            if key in self.polyglot_dict:
                if value != self.polyglot_dict[key]:
                    words_with_different_polarity.append(key)
                else:
                    words_with_same_polarity.append(key)

        text_1 = '----WORDS WITH DIFFERENT POLARITY----\n'
        text_2 = '\n\n----WORDS WITH SAME POLARITY----\n'
        self.__print_words_and_liwc_and_polyglot_polarity(text_1, words_with_different_polarity)
        self.__print_words_and_liwc_and_polyglot_polarity(text_2, words_with_same_polarity)
