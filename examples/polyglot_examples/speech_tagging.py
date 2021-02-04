from polyglot.text import Text


text = Text('I do not want to know about it.')

print('{:<16}{}'.format('Word', 'POS Tag'))
print('-'*30)

for word, tag in text.pos_tags:
    print('{:<16}{:>2}'.format(word, tag))
