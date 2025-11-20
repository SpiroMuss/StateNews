import json

try:
    import win32clipboard
    system = "WINDOWS"
except ImportError:
    system = None


config = json.load(open('config.json', encoding='utf-8'))

def write_config():
    json.dump(config, open('config.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
