import speech_recognition as sr
import pyttsx3
import openai
import wolframalpha
import platform

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.say(text)
    engine.runAndWait()

speak("Welcome to OpenPI. My name is Max and my goal is to assist you with your questions. To talk to me just include my name in every sentence you would like me to respond to. If my name is not in your question, I would not be able to respond to it. Here is an example: Max how is the weather like? Also ensure that you are using a stable wifi connection with atleast 10MB up and down speeds with minimal latency. For more details please go to this website: https://github.com/MiskaWasTaken/OpenPi")

if(platform.python_version() != "3.11.3"):
    print("Please use Python 3.11.3 for the best expereince you are currently using " + platform.python_version())

openai.api_key = "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"
API_KEY = "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"
r = sr.Recognizer()

app_id = "KX96V7-KVKHL73WP5"

client = wolframalpha.Client(app_id)

def calibrate():
    speak("I am getting ready. Please wait a moment")
    with sr.Microphone() as source:
        print("calibrating")    
        r.adjust_for_ambient_noise(source, duration=5)
        threshold = r.energy_threshold
    return threshold

energy_threshold = calibrate()
speak("I am ready. Let's begin")

def get_audio():
    with sr.Microphone() as source:
        r.energy_threshold = energy_threshold
        r.dynamic_energy_threshold = False
        speak("Listening...")
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
    return any(keyword in answer for keyword in keywords_list)

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