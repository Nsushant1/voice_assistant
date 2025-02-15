import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')


def speakFunction(audio):
    """Speaks the given text."""
    engine.say(audio)
    engine.runAndWait()


def introduction():
    """Gives a greeting based on the time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speakFunction("Good Morning")
    elif 12 <= hour < 18:
        speakFunction("Good Afternoon")
    else:
        speakFunction("Good Evening")
    
    speakFunction("I am Sushant. How can I help you?")


def get_recognition():
    """Recognizes voice input from the user."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5)  # Added timeout
            print("Recognizing...")
            input_query = recognizer.recognize_google(audio, language='en-NP')
            print(f'You said: {input_query}')
            return input_query.lower()
        except sr.WaitTimeoutError:
            print("No speech detected. Try again.")
        except sr.UnknownValueError:
            print("Could not understand audio. Try again.")
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")

    return None


def change_voice():
    """Changes the voice of the assistant."""
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        return 1  # Female voice
    return 0  # Default voice


def messages():
    """Handles conversation with the user."""
    while True:
        input_data = get_recognition()
        if input_data is None:
            continue

        if "what is your name" in input_data:
            speakFunction("My name is Sushant. What is your name?")
        elif "my name is" in input_data:
            speakFunction("Nice to meet you!")
        elif "do you love me" in input_data:
            speakFunction("Yes, I love you.")
        elif "okay" in input_data:
            speakFunction("Thank you.")
            break  # Exit loop on "okay"
        else:
            speakFunction("Sorry, I can't understand what you said. Please say it again.")


if __name__ == "__main__":
    voice_id = change_voice()
    voices = engine.getProperty('voices')

    if 0 <= voice_id < len(voices):
        engine.setProperty('voice', voices[voice_id].id)
    else:
        print("Invalid voice ID, using default voice.")

    introduction()
    messages()
