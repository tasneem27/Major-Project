#import speech_recognition as sr
#r = sr.Recognizer()
#with sr.WavFile("audiotrump.wav") as source:              # use "test.wav" as the audio source
 #   audio = r.record(source)                        # extract audio data from the file

#try:
 #   print("Transcription: " + r.recognize_sphinx(audio))   # recognize speech using Google Speech Recognition
#except LookupError:                                 # speech is unintelligible
 #   print("Could not understand audio")


#!/usr/bin/env python3

import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "Short_clip3.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
