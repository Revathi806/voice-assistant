import datetime
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
import sys

recognizer = sr.Recognizer()#initializing the speech recognition process/engine
engine = pyttsx3.init()#initializing the text to speech converter


#The speak function  is responsible 
# for converting text into speech using a text-to-speech (TTS) engine.
def speak(text):
    engine.say(text)#The say method prepares the text to be spoken.queues the text to be spoken
    engine.runAndWait()#stops the program until the text is completely said

#the listen function is responsible for listening to 
# what the user said and converting it into text
def listen():
    with sr.Microphone() as source:#source represents the microphone input
        print("Listening...")
        audio = recognizer.listen(source)#listens for audio input from the microphone and records it. The recorded audio is stored in the audio .
        try:
            query = recognizer.recognize_google(audio)#convert the recorded audio into text using Google’s Speech Recognition API.result stored in query
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:#engine cannot understand the audio input 
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:#connection issues with google speech recognition
            print("Could not request results from Google Speech Recognition service.")
            return None

#function responsble for tellin time
def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"The time is {current_time}")   

#function responsible for opening youtube        
def open_youtube():
    speak("Do you want me to open youtube?")
    response = listen()
    if response:
        try:
            if response and "open" in response.lower():
                webbrowser.open("https://www.youtube.com/")
                speak("Opening youtube for you.")
        except Exception as e:
            speak("error while loading youtube")
            print(e)


#function responsible for opening google
def open_google():
    speak("Do you want me to open google?")
    response = listen()
    if response:
        try:
            if response and "open" in response.lower():
                webbrowser.open("google.com")
                speak("Opening google for you.")
        except Exception as e:
            speak("error while loading google")
            print(e)

#function responsible for searching in google
def search_google():
    speak("What do you want to search for?")
    query = listen()  
    if query: 
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}.")


def tell_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")  # Format: Month Day, Year
    speak(f"Today's date is {current_date}") 


def handle_wikipedia():
    speak("What do you want to know about?")
    topic = listen()  # listen to question
    if topic:  # if topic is valid
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results for that. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find any information on that topic.")

# The main function is responsible for the main logic/working of the voice assistant
def voice_assistant():
    speak("Hello! I am Sam, your voice assistant. How can I help you today?")
    while True:
        query = listen()  # listen to user
        if query:
            if "exit" in query.lower():  # if user says exit, stop the program
                speak("Goodbye!")
                break
            elif "hello" in query.lower():
                speak("hello, how can i help you?")
            elif "thank you" in query.lower():
                speak("your welcome")
            elif "wikipedia" in query.lower():  # if user says wikipedia
                handle_wikipedia()
            elif "youtube" in query.lower():  # if user says youtube
                open_youtube()
            elif "time" in query.lower():  # if user asks for time
                tell_time()
            elif "date" in query.lower():  # if user asks for date
                tell_date()
            elif "search" in query.lower() or "google" in query.lower():  # if user wants to search Google
                search_google()
            else:
                speak("I can only search Wikipedia for you, open YouTube, tell you the time and date, or search Google. Please ask me about something else.")


class VoiceAssistantApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Voice Assistant')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Press the button to start the voice assistant.', self)
        layout.addWidget(self.label)

        self.start_button = QPushButton('Start Voice Assistant', self)
        self.start_button.clicked.connect(self.start_voice_assistant)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def start_voice_assistant(self):
        self.label.setText('Voice Assistant is starting...')
        self.start_button.setEnabled(False)  # Disable the button while the assistant is running
        voice_assistant()  # Start the voice assistant

        self.label.setText('Voice Assistant has stopped.')
        self.start_button.setEnabled(True)  # Re-enable the button

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceAssistantApp()
    ex.show()
    sys.exit(app.exec_())