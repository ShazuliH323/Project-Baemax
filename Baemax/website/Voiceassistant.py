import speech_recognition as sr 
import datetime
import subprocess
import os
import pyttsx3
import webbrowser
import pyttsx3
import speech_recognition
from playsound import playsound

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
recognizer=sr.Recognizer()
text= ""
bye = False
import requests
import random
def speak(audio):
     
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')
     
    # setter method .[0]=male voice and 
    # [1]=female voice in set Property.
    engine.setProperty('voice', voices[0].id)
     
    # Method for the speaking of the assistant
    engine.say(audio)  
     
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()
def quote():
    response = requests.get(
        "https://zenquotes.io/api/quotes"
    )



    choose=random.randint(1,50)
    quote=response.json()[choose]["q"]
    name=response.json()[choose]["a"]
    print(quote, "- ", name)
    return quote



while bye != True:
    
    
    with sr.Microphone() as source:
        speak("Please give me a moment whilst I calibrate...")
        recognizer.adjust_for_ambient_noise(source,duration=0.5)
        speak('How can I help?')
        recordedaudio=recognizer.listen(source)
    try:
        text=recognizer.recognize_google(recordedaudio,language='en_US')
        text=text.lower()
        speak('Your message:',format(text))

    except Exception as ex:
        print(ex)
    
    if 'quote' in text:
        speak("Hi there, here is your daily quote:")
        speak(quote())
        
    if 'chrome'in text:
        a='Opening chrome..'
        engine.say(a)
        engine.runAndWait()
        programName = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([programName])
    
    if 'start' in text:
        os.system('python main.py')
    if 'dashboard' in text:
        
# Add a URL of JavaTpoint to open it in a browser  
        url= 'http://127.0.0.1:5000/'  
# Open the URL using open() function of module  
        webbrowser.open_new_tab(url)  
        
    if 'time' in text:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        engine.say(time)
        engine.runAndWait()
    if "goodbye" in text:
        print("goodbye")
        speak("Goodbye, I will now shut down")
        bye = True


