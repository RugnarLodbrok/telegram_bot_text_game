import sys
import os
from telegram import Bot
from telegram.ext import Updater
import logging

sys.path.insert(1, os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.path.pardir
)))

from my_bot.consts import *
from my_bot.game import run_game

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

global_context = {"chat_id": None}


def main():
    Bot(TOKEN, base_url=API_URL)
    updater = Updater(
        token=TOKEN,
        base_url=API_URL,
        use_context=True,
        # bot=Bot(TOKEN, base_url=API_URL),
        workers=8
    )
    run_game(updater.dispatcher)
    updater.start_polling()


if __name__ == '__main__':
    main()
