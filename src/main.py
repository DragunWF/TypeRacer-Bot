import json
from pathlib import Path
from colored import fg

from bot import Bot
from session import Session
from utils import Utils

session = Session()
cyan, white = fg("light_cyan"), fg("white")


def change_settings() -> tuple:
    while True:
        try:
            races = int(input(cyan + "How many races would you like to run: " + white))
            universe = input(cyan + "Universe: " + white).strip().lower()
            registered = Utils.user_choose("Are you going to play in a registered account?")
            practice_mode = Utils.user_choose("Are you going to play in practice mode?")
            break
        except ValueError:
            Utils.colored_print("Make sure your input is an integer value...",
                                color="red")

    return (races, universe, registered, practice_mode)


def configure_bot() -> dict:
    default_settings = json.loads(Path("data/settings.json").read_text())[0]
    use_default = Utils.user_choose(
        "Would you like to use the default settings?")

    if not use_default:
        changes = change_settings()
        default_settings["races"] = changes[0]
        default_settings["universe"] = changes[1]
        default_settings["registered"] = changes[2]
        default_settings["practice_mode"] = changes[3]

    return default_settings


def main():
    config = json.loads(Path("data/settings.json").read_text())[1]
    settings = configure_bot()

    bot = Bot(config["username"], config["password"], session, settings)
    Utils.tts_print("Bot is now running!", color="green")
    bot.run()


if __name__ == "__main__":
    main()
