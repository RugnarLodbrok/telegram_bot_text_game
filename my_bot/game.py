from contextlib import contextmanager

import yaml
from collections import defaultdict
from telegram.ext import MessageHandler, Filters, CommandHandler

from my_bot.picture_sender import PictureSender
from my_bot.scene import Scene


class GameContext:
    def __init__(self, bot):
        self.bot = bot
        self.chat_id = None  # not thread-safe
        self.players = defaultdict(dict)
        self.picture_sender = PictureSender(self.bot)
        self.scenario = {}
        with open('scenario_bear.yml', 'rt', encoding='utf8') as f:
            for scene_data in yaml.load(f, Loader=yaml.BaseLoader):
                scene = Scene.from_data(scene_data)
                self.scenario[scene.name] = scene

    @contextmanager
    def chat(self, chat_id):
        self.chat_id = chat_id
        yield
        self.chat_id = None

    def make_move(self, choice):
        player = self.players[self.chat_id]
        if not player:
            player['scene'] = self.scenario['start']

        scene = self.scenario[player['scene']]
        for opt in scene.opts:
            if opt.text == choice:
                player['scene'] = opt.goto
                return self.scenario[player['scene']].show(self)


def run_game(dispatcher):
    game = GameContext(dispatcher.bot)

    def start(update, context):
        bot = context.bot
        chat_id = update.effective_chat.id
        game.players[chat_id]['scene'] = 'start'
        with game.chat(chat_id):
            game.scenario['start'].show(game)

    def text_handler(update, context):
        with game.chat(update.effective_chat.id):
            game.make_move(update.message.text)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, text_handler))


def make_move(bot, chat_id, player, choice):
    if not player:
        player['scene'] = scenario['start']

    scene = scenario[player['scene']]
    for opt in scene.opts:
        if opt.text == choice:
            player['scene'] = opt.goto
            return scenario[player['scene']].show(bot, chat_id)
