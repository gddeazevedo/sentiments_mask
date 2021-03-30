from led_matrix.led_matrix import LedMatrix
from pyfirmata import Arduino
from natural_language_understanding.natural_language_understanding import fetch_watson_and_return_sentiment_label
from speech_to_text.speech_to_text import get_text_converted_from_speech


usb_port = 'COM3'
data_in = 2
load = 4
clock = 3

smile_face = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

sad_face = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

neutral_face = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]


def main():
    text = get_text_converted_from_speech()
    sentiment_label = fetch_watson_and_return_sentiment_label(text)

    print(f'\n----You said: {text}')
    print(f'\n----Sentence sentiment: {sentiment_label}\n')

    board = Arduino(usb_port)
    matrix = LedMatrix(board, data_in, load, clock)
    matrix.setup()

    if sentiment_label == 'positive':
        matrix.draw_matrix(smile_face)
    elif sentiment_label == 'negative':
        matrix.draw_matrix(sad_face)
    else:
        matrix.draw_matrix(neutral_face)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
