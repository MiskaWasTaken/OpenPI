import speech_recognition as sr
import pyttsx3
import os
import pygame
from io import BytesIO
import openai
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
openai.api_key = "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"
API_KEY = "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"
r = sr.Recognizer()


def calibrate():
    with sr.Microphone() as source:
        print("calibrating")    
        r.adjust_for_ambient_noise(source, duration=5)
        threshold = r.energy_threshold
    return threshold

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'english_rp+f3')
    engine.runAndWait()

energy_threshold = calibrate()

def get_audio():
    with sr.Microphone() as source:
        r.energy_threshold = energy_threshold
        r.dynamic_energy_threshold = False
        print("Listening...")
        audio = r.listen(source)
        try:
            my_text = r.recognize_whisper_api(audio, api_key=API_KEY)
        except sr.UnknownValueError as b:
            speak("Sorry i dont understand what you mean, please repeat or try again later.")
            print("OpenAI Recognition could not understand audio; {0}".format(b))
            return
        except sr.RequestError as b:
            speak("Unable to contact services. Please contact a staff memeber")
            print("Could not request results from OpenAI; {0}".format(b))
            return
    return my_text.lower()


def ChatGPT(text):

    messages = [{"role": "user", "content": text}]

    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        )

        answer = response['choices'][0]['message']['content']
        print(answer)
        word_list = answer.split()
        if len(word_list) > 20:
            speak("Give me some time to think")
        else:
            speak(answer)

    except Exception as e:
        print(e)
        speak("An error occured while contacting ChatGPT. Please contact a staff member")