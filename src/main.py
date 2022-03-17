import json
import config
from bot import Bot
from session import Session
from utils import Utilities
from colored import fg

session = Session()
cyan, white = fg("light_cyan"), fg("white")


def change_settings():
    while True:
        try:
            races = int(input(cyan + "$ How many races would you like to run: "
                              + white))
            universe = input(cyan + "$ Universe: " +
                             white).strip().lower()
            break
        except ValueError:
            Utilities.colored_print("Make input an integer value...",
                                    color="red")

    return races, universe


def configure_bot():
    while True:
        default = input(cyan + "Would you like to use the default settings? (y/n) "
                        + white).strip().lower()
        if default == "y" or default == "yes":
            races = 100
            universe = "play"
            break
        elif default == "n" or default == "no":
            races, universe = change_settings()
            break
        else:
            Utilities.colored_print("Invalid option!", color="red")

    return {"race_runs": races, "universe": universe}


def main():
    configuration = configure_bot()
    bot = Bot(config.username, config.password,
              session, configuration["race_runs"],
              configuration["universe"])
    Utilities.tts_print("Bot is now running!", color="green")
    bot.run()


if __name__ == "__main__":
    main()
