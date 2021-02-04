from polyglot.text import Text


message = 'Hola, buenos días. Yo soy una persona y estoy estudiando... Naturalmente no es legal.'

text = Text(message)

print(f'Language detected: Code={text.language.code}, Name={text.language.name}')
print(text)
print(text.language)
print(text.words)
print(text.sentences)
