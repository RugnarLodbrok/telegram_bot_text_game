from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

SHOW_PICTURES = True


class SceneOption:
    def __init__(self, text, goto):
        self.text = text
        self.goto = goto

    @classmethod
    def from_data(cls, data):
        return cls(data['text'], data['goto'])


class Scene:
    def __init__(self, name, text, opts=None, picture=None, animation=None):
        self.name = name
        self.text = text
        self.opts = [SceneOption.from_data(data) for data in opts or []]
        self.picture = picture
        self.animation = animation

    @classmethod
    def from_data(cls, data):
        return cls(data['name'],
                   data['text'],
                   data.get('opts'),
                   data.get('picture'),
                   data.get('animation'))

    def show(self, game_context):
        if SHOW_PICTURES:
            try:
                if self.picture:
                    game_context.picture_sender.send_picture(game_context.chat_id, self.picture)
                if self.animation:
                    game_context.picture_sender.send_animation(game_context.chat_id, self.animation)
            except FileNotFoundError as e:
                print("file not found", e)
        reply_markup = None
        if self.opts:
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=opt.text)] for opt in self.opts])
        if not reply_markup:
            reply_markup = ReplyKeyboardRemove()
        game_context.bot.send_message(chat_id=game_context.chat_id,
                                      text=self.text,
                                      reply_markup=reply_markup)
