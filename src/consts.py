import yaml as _yaml

with open('config.yml', 'rt') as f:
    cfg = _yaml.load(f, Loader=_yaml.BaseLoader)

if cfg['proxy']:
    _proxy_host = cfg['proxy']['host']
    _proxy_port = cfg['proxy'].get('port', 8888)
    API_URL = f"http://{_proxy_host}:{_proxy_port}/tg_api/bot"
else:
    API_URL = f"https://api.telegram.org/bot"
TOKEN = cfg['token']
ADMIN_ID = int(cfg['admin_id'])
API_ID = int(cfg.get('api_id'))
API_HASH = cfg.get('api_hash')
print(cfg)
