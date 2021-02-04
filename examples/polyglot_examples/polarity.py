from polyglot.text import Text


# text = Text('Beautiful is better than ugly')

# print('{:<16}{}'.format('Word', 'Polarity') + '\n' + '-'*30)

# for word in text.words:
#     print('{:<16}{:>2}'.format(word, word.polarity))

in_text = input('Digite uma frase ai seu filho da puta: ')
text = Text(in_text)
for word in text.words:
    print(f'{word} {word.polarity}')
