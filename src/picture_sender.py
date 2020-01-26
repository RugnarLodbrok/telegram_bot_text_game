import os
import io
import yaml

CACHE_FILE = 'picture_cache.yml'


def _read_cache():
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rt') as f:
            cache = yaml.load(f, yaml.BaseLoader)
    assert isinstance(cache, dict)
    for k, v in cache.items():
        assert isinstance(k, str)
        assert isinstance(v, str)
    return cache


def _write_cache(data):
    with open(CACHE_FILE, 'wt') as f:
        yaml.dump(data, f)


class PictureSender:
    def __init__(self, bot):
        self._bot = bot
        self._cache = _read_cache()

    def send_picture(self, chat_id, f_name):
        if f_name not in self._cache:
            with open(f'assets/{f_name}', 'rb') as f:
                r = self._bot.send_photo(chat_id=chat_id, photo=f)
            print("upload")
            self._cache[f_name] = r['photo'][-1]['file_id']
            _write_cache(self._cache)
        else:
            f_id = self._cache[f_name]
            print("use cached")
            self._bot.send_photo(chat_id=chat_id, photo=f_id)

    def send_animation(self, chat_id, f_name):
        if f_name not in self._cache:
            with open(f'assets/{f_name}', 'rb') as f:
                r = self._bot.send_animation(chat_id=chat_id, animation=f)
            print("upload")
            self._cache[f_name] = r['animation']['file_id']
            _write_cache(self._cache)
        else:
            f_id = self._cache[f_name]
            print("use cached")
            self._bot.send_animation(chat_id=chat_id, animation=f_id)
