import pyttsx3
from colored import fg

voice_engine = pyttsx3.init("sapi5")
voices = voice_engine.getProperty("voices")
voice_engine.setProperty("voice", voices[0].id)


class Utilities:
    @staticmethod
    def text_to_speech(text):
        voice_engine.say(text)
        voice_engine.runAndWait()

    @staticmethod
    def colored_print(text, color):
        color_func = fg(f"light_{color}") if color != "white" else fg("white")
        print(color_func + text)

    @staticmethod
    def tts_print(text, color=None):
        Utilities.colored_print(text, color if color else "white")
        Utilities.text_to_speech(text)
