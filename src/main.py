import json
from pathlib import Path
from colored import fg

import config
from bot import Bot
from session import Session
from utils import Utilities

session = Session()
cyan, white, red = fg("light_cyan"), fg("white"), fg("light_red")


def user_choose(question) -> bool:
    option = input(cyan + f"{question} (y/n) " + white).strip().lower()
    if option == "y" or option == "yes":
        return True
    if option == "n" or option == "no":
        return False
    Utilities.colored_print("Invalid input!", color="red")
    user_choose(question)


def change_settings() -> tuple:
    while True:
        try:
            races = int(input(cyan + "How many races would you like to run: "+ white))
            universe = input(cyan + "Universe: " + white).strip().lower()
            registered = user_choose("Are you going to play in a registered account?")
            practice_mode = user_choose("Are you going to play in practice mode?")
            break
        except ValueError:
            Utilities.colored_print("Make sure your input is an integer value...",
                                    color="red")

    return (races, universe, registered, practice_mode)


def configure_bot() -> dict:
    default_settings = json.loads(Path("data/settings.json").read_text())[0]
    use_default = user_choose("Would you like to use the default settings?")

    if not use_default:
        changes = change_settings()
        default_settings["races"] = changes[0]
        default_settings["universe"] = changes[1]
        default_settings["registered"] = changes[2]
        default_settings["practice_mode"] = changes[3]

    return default_settings


def main():
    settings = configure_bot()
    bot = Bot(config.username, config.password, session, settings)
    Utilities.tts_print("Bot is now running!", color="green")
    bot.run()


if __name__ == "__main__":
    main()
