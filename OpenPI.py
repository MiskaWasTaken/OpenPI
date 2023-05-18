from functions import * 

def respond(text):
    x = text.replace("axe", "max")
    print("Spoken text: " + text)
    if 'max' not in x:
        return
    elif 'stop' in x:
        return
    elif(text):
        chat_gpt(text)
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