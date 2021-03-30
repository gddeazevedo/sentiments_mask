import os
import sounddevice
from scipy.io import wavfile
from api import keys, urls
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def record_audio_and_save_into_wav_file():
    '''Records an audio in .wav format and saves it into ./audios'''
    print('Say something')
    fs = 44100
    second = 6
    record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    wavfile.write('./audios/speech.wav', fs, record_voice)
    print('Audio recorded')


def get_text_converted_from_speech():
    '''
    Returns a string which is the text converted from a speech if no errors happen
    Else, it returns None
    '''

    # Authenticating Speech to Text API with personal key and url
    authenticator = IAMAuthenticator(keys.stt_key)
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(urls.stt_url)
    
    # Recording and saving an audio
    record_audio_and_save_into_wav_file()

    # Converting speech to text
    with open('./audios/speech.wav', 'rb') as f:
        try:
            print('Converting speech to text...')
            res = stt.recognize(audio=f, content_type='audio/wav', model='pt-BR_NarrowbandModel').get_result()
        except Exception as error:
            print('Erro!')
            print(error)
            os.remove('./audios/speech.wav')
            return None

    print('Done!')
    os.remove('./audios/speech.wav')
    return res['results'][0]['alternatives'][0]['transcript']
