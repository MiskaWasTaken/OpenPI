from functions import * 
import os


def respond(text):
    if 'max' in text.replace("axe", "max") and 'stop' not in text:
        print("Spoken text: " + text)
        chat_gpt(text)

while True:
    try:
        text = get_audio()
        respond(text)
    except (TypeError, UnboundLocalError) as e:
        print(e)
        speak("An issue occured with the code. Please contact a staff member")