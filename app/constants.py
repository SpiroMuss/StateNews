import json


class Constants:
    def __init__(self):
        self.reload_constants()
        self.system = None


    def reload_constants(self):
        self.config = json.load(open('config.json', encoding='utf-8'))
        self.staff = self.config.get("STAFF")
        self.activity = self.config.get("ACTIVITY")
        self.list_marks = self.config.get("LIST_MARKS")

    def upload_system(self):
        try:
            import win32clipboard
            self.system = "WINDOWS"
        except ImportError:
            self.system = None

    def delete_constant(self):
        pass

    def commit(self):
        json.dump(self.config, open("config.json", "w"), ensure_ascii=False, indent=2)


constants = Constants()