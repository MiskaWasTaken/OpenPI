import speech_recognition as sr
import pyttsx3
import os
import openai
import time
import wolframalpha

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
openai.api_key = "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"
API_KEY = "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"
r = sr.Recognizer()

app_id = "KX96V7-KVKHL73WP5"

client = wolframalpha.Client(app_id)

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def calibrate():
    speak("I am getting ready. Please wait a moment")
    time.sleep(1)
    with sr.Microphone() as source:
        print("calibrating")    
        r.adjust_for_ambient_noise(source, duration=5)
        threshold = r.energy_threshold
    return threshold


energy_threshold = calibrate()
speak("I am ready. Let's begin")

time.sleep(1)

def get_audio():
    with sr.Microphone() as source:
        r.energy_threshold = energy_threshold
        r.dynamic_energy_threshold = False
        speak("Listening...")
        time.sleep(1)
        print("Listening...")
        audio = r.listen(source)
        try:
            my_text = r.recognize_whisper_api(audio, api_key=API_KEY)
        except sr.UnknownValueError as b:
            speak("Sorry i dont understand what you mean, please repeat or try again later.")
            print("OpenAI Recognition could not understand audio; {0}".format(b))
            return
        except sr.RequestError as b:
            speak("Unable to contact services. Please contact a staff member")
            print("Could not request results from OpenAI; {0}".format(b))
            return
    return my_text.lower()


def check_answer_keywords(answer, keywords_list):
    for keyword in keywords_list:
        if keyword in answer:
            return True 
    return False 

def chat_gpt(text):
    def wolfram(text):
        try:
            text_moda = text.replace('max', '')
            text_modb = text_moda.replace(',', '')

            client = wolframalpha.Client(app_id)

            res = client.query(text_modb)

            answer = next(res.results).text
            print(answer)
            speak(answer)
        except:
            print("An error occured with WolframAlpha")

    messages = [{"role": "user", "content": text}]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        answer = response['choices'][0]['message']['content'] 
        keywords_list = ["real-time", "up-to-date", "latest", "capability"]
        if check_answer_keywords(answer, keywords_list):
            print("Keyword match found!")
            wolfram(text)
        else:
            speak(answer)

    except Exception as e:
        print(e)
        speak("An error occurred while contacting ChatGPT. Please contact a staff member")


