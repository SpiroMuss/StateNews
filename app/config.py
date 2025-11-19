import json

try:
    import win32clipboard
    system = "WINDOWS"
except ImportError:
    system = None


config = json.load(open('config.json', encoding='utf-8'))
