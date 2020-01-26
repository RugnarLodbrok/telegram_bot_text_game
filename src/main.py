import sys
import os
import yaml
import logging

from telegram import Bot
from telegram.ext import Updater

sys.path.insert(1, os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.path.pardir)))

from my_bot.consts import *
from my_bot.game import run_game

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

global_context = {"chat_id": None}


def main():
    with open('scenario_bear.yml', 'rt', encoding='utf8') as f:
        scenario_data = yaml.load(f, Loader=yaml.BaseLoader)

    Bot(TOKEN, base_url=API_URL)
    updater = Updater(
        token=TOKEN,
        base_url=API_URL,
        use_context=True,
        # bot=Bot(TOKEN, base_url=API_URL),
        workers=8
    )
    run_game(updater.dispatcher, scenario_data)
    updater.start_polling()


if __name__ == '__main__':
    main()
