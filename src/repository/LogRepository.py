import json
from model.log import Log, LogEncoder

class LogRepository:
    def __init__(self, json_file):
        self.json_file = json_file

    def load_log_entries(self):
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_log_entry(self, log_entry):
        log_entries = self.load_log_entries()
        log_entries.append(log_entry)
        with open(self.json_file, 'w') as file:
            json.dump(log_entries, file, cls=LogEncoder)
