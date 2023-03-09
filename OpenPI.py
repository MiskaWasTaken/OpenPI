import speech_recognition as sr
from gtts import gTTS
import os
import pygame
from io import BytesIO
import openai
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
openai.api_key = "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"
r = sr.Recognizer()


# get mic audio
def calibrate():
    with sr.Microphone() as source:
        print("calibrating")
        r.adjust_for_ambient_noise(source, duration=5)
        threshold = r.energy_threshold
    return threshold


energy_threshold = calibrate()


def get_audio():
    with sr.Microphone() as source:
        r.energy_threshold = energy_threshold
        r.dynamic_energy_threshold = False
        print("Listening...")
        audio = r.listen(source)
        try:
            my_text = r.recognize_vosk(audio, language='en')
            text_obj = json.loads(my_text)
            my_text = text_obj["text"]
        except sr.UnknownValueError as b:
            speak("Sorry i dont understand what you mean, please repeat or try again later.")
            print("Vosk Recognition could not understand audio; {0}".format(b))
            return
        except sr.RequestError as b:
            speak("Unable to contact services. Please contact a staff memeber")
            print("Could not request results from Vosk; {0}".format(b))
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

def ChatGPT(text):

    try:
        prompt_ai = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly: \n" + text

        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_ai,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
        )

        answer = response["choices"][0]["text"]
        print(answer)
        speak(answer)

    except Exception as e:
        print(e)
        speak("An error occured while contacting ChatGPT. Please contact a staff member")




def respond(text):
    print("Spoken text: " + text)
    if 'ava' not in text:
        return
    elif(text):
        ChatGPT(text)
    else:
        return


while True:
    try:
        text = get_audio()
    except TypeError as e:
        print("error getting audio, (no audio) Please contact a staff member; {0}".format(e))
        text = ""
        speak("An issue occured with the code. Please contact a staff member")
    except UnboundLocalError as e:
        print(e)
        text = ""
        speak("A local error has occured. Please contact a staff member")

    respond(text)