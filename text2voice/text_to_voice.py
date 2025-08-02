import pyttsx3

class text_to_voice:
    def __init__(self):
        self.engine = pyttsx3.init(driverName='sapi5')  # For Windows
        # Set properties before adding anything to speak
        self.engine.setProperty('rate', 150)  # Speed percent (can go over 100)
        self.engine.setProperty('volume', 0.9)  # Volume 0-1

    def speak(self, text=None):
        self.engine.say(text)
        self.engine.runAndWait()
