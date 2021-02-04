import pickle
import tarfile
import os
from polyglot.detect import Detector
from polyglot.text import Text


HOME = os.environ['HOME']

sample_text = 'Barack Obama gave a fantastic speech last night. ' \
              'Reports indicate he will move next to New Hampshire to win the competition.'


def polyglot_entity_sentiment(user_text):
    phrase = Text(user_text)
    phrase_sentences = phrase.sentences
    print('Sentencas', phrase_sentences)
    for sentence in phrase_sentences:
        sentence_entities = sentence.entities
        for entity in sentence_entities:
            print('Entidade: ', entity)
            print('Valor positivo da frase: ', entity.positive_sentiment)
            print('Valor negativo da frase: ', entity.negative_sentiment)


def polyglot_text_polarity(user_text):
    user_text = Text(user_text)
    print(f'Text polarity: {user_text.polarity}')


def polyglot_word_polarity(user_text):
    phrase = Text(user_text)
    print("{:<16}{}".format("Word", "Polarity") + "\n" + "-" * 30)
    for w in phrase.words:
        print("{:<16}{:>2}".format(w, w.polarity))


def polyglot_detect_language(user_text):
    detector = Detector(user_text)
    print(detector.language)


def init_polyglot_sequence():
    print("Escreve um texto ai (Nao muito curto).\nOu deixe vazio para o texto de exemplo.")
    user_input = input('Texto: ')
    if user_input.strip() == '':
        user_input = sample_text
    return user_input


def add_new_words_to_dict():
    # Alterar caminho do arquivo
    tar = tarfile.open(f"{HOME}/polyglot_data/sentiment2/pt/pt.sent.pkl.tar.bz2")
    tar.extractall()
    tar.close()
   
    new_words = []
    new_words_values = []

    # Alterar caminho do arquivo
    with open('./pt.sent.pkl', 'rb') as f:
        u = pickle.Unpickler(f, encoding="latin1")
        dictionary_words, dictionary_words_values = u.load()
        print(len(dictionary_words))
    for index, word in enumerate(dictionary_words):
        new_words.append(word)
        new_words_values.append(dictionary_words_values[index])

    with open('data/tmp/sentiment/pt/pt.sent.pkl', 'rb') as extracted_old_dict:
        un = pickle.Unpickler(extracted_old_dict, encoding="latin1")
        dictionary_words, dictionary_words_values = un.load()

    dictionary_words = list(dictionary_words)
    dictionary_words_values = list(dictionary_words_values)

    # add new words to dictionary
    for i in range(len(new_words)):
        if new_words[i] not in dictionary_words:
            print('adding ', new_words[i], new_words_values[i])
            dictionary_words.extend([new_words[i]])
            dictionary_words_values.extend([new_words_values[i]])
        else:
            print('already exist word =', new_words[i], new_words_values[i])

    # escreve novas palavras no dicionario (ou cria novo dicionario)
    result = (dictionary_words, dictionary_words_values)
    with open('data/tmp/sentiment/pt/pt.sent.pkl', 'wb+') as extracted_old_dict:
        pickle.dump(result, extracted_old_dict)

    # Alterar caminho do arquivo
    tar = tarfile.open(f"{HOME}/polyglot_data/sentiment2/pt/pt.sent.pkl.tar.bz2", "w")
    tar.add("data/tmp/sentiment/pt/pt.sent.pkl")
    tar.close()


if __name__ == '__main__':
    text = init_polyglot_sequence()
    print('\n\n')
    polyglot_detect_language(text)
    print('\n\n')
    polyglot_entity_sentiment(text)
    print('\n\n')
    polyglot_word_polarity(text)
    print('\n\n')
    polyglot_text_polarity(text)
    print('\n\n')
    #add_new_words_to_dict()
