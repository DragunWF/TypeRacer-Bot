import json
import data.config as config
from .bot import Bot
from .session import Session
from .utils import Utilities

bot = Bot()
session = Session()


def main():
    bot.run(config.username, config.password, session)
    Utilities.text_to_speech("Bot is now running!")


if __name__ == "__main__":
    main()
