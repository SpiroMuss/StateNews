import json
import os

import platform
system = platform.system()

from dotenv import load_dotenv
load_dotenv()

url = os.getenv("WEBHOOK")


config = json.load(open('config.json', encoding='utf-8'))

def write_config():
    json.dump(config, open('config.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
