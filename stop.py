import speech_recognition as sr
from gtts import gTTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from io import BytesIO
import openai
import json
openai.api_key = "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"
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
            my_text = r.recognize_vosk(audio, language='en')
            text_obj = json.loads(my_text)
            my_text = text_obj["text"]
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
    stop_elements = ['ava', 'stop']
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