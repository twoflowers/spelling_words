# coding=utf-8
import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1
from pygame import mixer
import pyglet
import scipy.io.wavfile
import wave
import subprocess

text_to_speech = TextToSpeechV1(
    username='4ef7923c-a9b1-43d6-b466-95f4bb32708c',
    password='q4BjDwfaeCOj',
    x_watson_learning_opt_out=True)  # Optional flag

# print(json.dumps(text_to_speech.voices(), indent=2))
wavefile = 'resources/tom.mp3'
with open(wavefile, 'wb') as audio_file:
    audio_file.write(text_to_speech.synthesize('ride', accept='audio/mp3',voice="en-US_AllisonVoice"))

return_code = subprocess.call(["afplay", wavefile])
