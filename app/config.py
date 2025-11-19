import json

try:
    import win32clipboard
    system = "WINDOWS"
except ImportError:
    system = None


class ConfigItem:
    def __init__(self, item):
        self.item = item
        self.frame = None

    def item(self):
        return self.item

file = json.load(open('config.json', encoding='utf-8'))
config = {}
for key, value in file.items():
    config[key] = []
    for item in value:
        config[key].append(ConfigItem(item))
