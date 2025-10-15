import json


class Constants:
    def __init__(self):
        self.reload_constants()
        self.system = None


    def reload_constants(self):
        self.config = json.load(open('config.json'))
        self.staff = self.config.get("STAFF")

    def upload_system(self):
        try:
            import win32clipboard
            self.system = "WINDOWS"
        except ImportError:
            self.system = None


constants = Constants()