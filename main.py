#!/usr/bin/env python3

import speech_recognition as sr
import requests
from audio import *

with no_alsa_error():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, snowboy_configuration=("./snowboy/examples/Python3", ["./snowboy/resources/models/neumann.pmdl"]))
        # audio = r.listen(source)
        play_audio_file()

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    words = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said " + words)
    wordsArray = words.split(" ")
    if wordsArray[1] == "turn":
        requests.post("https://localhost:3000/trigger", verify=False, json={
            "trigger": "lights",
            "data": {
                "action": wordsArray[2],
                "target": wordsArray[4],
            },
        })
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# recognize speech using Google Cloud Speech
#GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
#try:
#    print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
#except sr.UnknownValueError:
#    print("Google Cloud Speech could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Google Cloud Speech service; {0}".format(e))