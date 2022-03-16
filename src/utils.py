import time
import pyttsx3
from colored import fg

voice_engine = pyttsx3.init("sapi5")
voices = voice_engine.getProperty("voices")
voice_engine.setProperty("voice", voices[0].id)

green, yellow, red, white = fg("light_green"), fg(
    "light_yellow"), fg("light_red"), fg("white")


class Utilities:
    @staticmethod
    def text_to_speech(text):
        voice_engine.say(text)
        voice_engine.runAndWait()

    @staticmethod
    def colored_print(text, color):
        print(f"light_{color}" + text)

    @staticmethod
    def tts_print(text, color=None):
        Utilities.colored_print(text, color if color else white)
        Utilities.text_to_speech(text)
