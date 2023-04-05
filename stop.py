import speech_recognition as sr
from gtts import gTTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from io import BytesIO
import openai
import json
openai.api_key = "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"
API_KEY = "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"
r = sr.Recognizer()
import subprocess

process = subprocess.Popen(["python", "OpenPi.py"])


# get mic audio
def calibrate():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        energy_threshold = r.energy_threshold
    return energy_threshold


energy_threshold = calibrate()

def get_audio():
    with sr.Microphone() as source:
        r.energy_threshold = energy_threshold
        r.dynamic_energy_threshold = False
        audio = r.listen(source)
        try:
            my_text = r.recognize_whisper_api(audio, api_key=API_KEY)
        except sr.UnknownValueError as e:
            return
        except sr.RequestError as e:
            return
    return my_text.lower()


# speak converted audio to text
def speak(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



def respond(text):
    stop_elements = ['stop']
    res = any(ele in text for ele in stop_elements)
    if "True" in str(res):
        process.terminate()
        subprocess.Popen(["python", "OpenPi.py"])
        print("-----PROCESS RESTARTED------")
    else:
        return


while True:
    try:
        text = get_audio()
    except TypeError as e:
        print("error getting audio, (no audio); {0}".format(e))
        text = ""
        speak("An issue occured with the code")
    except UnboundLocalError as e:
        print(e)
        text = ""
        speak("A local error has occured")

    respond(text)