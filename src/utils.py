import pyttsx3
from colored import fg

voice_engine = pyttsx3.init("sapi5")
voices = voice_engine.getProperty("voices")
voice_engine.setProperty("voice", voices[0].id)


class Utils:
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
        Utils.colored_print(text, color if color else "white")
        Utils.text_to_speech(text)

    @staticmethod
    def user_choose(question: str) -> bool:
        cyan, white = fg("light_cyan"), fg("white"), fg("light_red")
        while True:
            option = input(cyan + f"{question} (y/n) " + white).strip().lower()
            if option == "y" or option == "yes":
                return True
            if option == "n" or option == "no":
                return False
            Utils.colored_print("Invalid input!", color="red")
