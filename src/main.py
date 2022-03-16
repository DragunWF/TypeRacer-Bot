import json
import config
from bot import Bot
from session import Session
from utils import Utilities

session = Session()
bot = Bot(config.username, config.password, session, 25)


def configure_bot():
    pass


def main():
    configure_bot()
    Utilities.text_to_speech("Bot is now running!")
    bot.run()


if __name__ == "__main__":
    main()
