import azure.cognitiveservices.speech as speechsdk
import pyttsx3
import re
my_dict = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "he": "e",
    "if": "f",
    "te": "d"
}


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
def recognize_from_mic():
    # Find your key and resource region under the 'Keys and Endpoint' tab in your Speech resource in Azure Portal
    # Remember to delete the brackets <> when pasting your key and region!
    speech_config = speechsdk.SpeechConfig(subscription="313fd49c341d4a1da426c9b69ba245ff", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # Asks user for mic input and prints transcription result on screen
    result = speech_recognizer.recognize_once_async().get()
    #print(str.lower(result.text))
    return (str.lower(result.text))

while True:
    input_move = recognize_from_mic()
    for key, value in my_dict.items():
        input_move = input_move.replace(key, value)
    print(input_move[0:4])

