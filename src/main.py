import json
import config
from bot import Bot
from session import Session
from utils import Utilities

session = Session()


def configure_bot():
    try:
        while True:
            races = int(input("$ How many races would you like to run: "))
            settings = {"race_runs": races}
            break
    except ValueError:
        Utilities.colored_print("Invalid Input", color="red")

    return settings


def main():
    configuration = configure_bot()
    bot = Bot(config.username, config.password,
              session, configuration["race_runs"])
    Utilities.text_to_speech("Bot is now running!")
    bot.run()


if __name__ == "__main__":
    main()
