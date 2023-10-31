import json 

class LogEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Log):
            return o.__dict__
        return super().default(o)

class Log:
    def __init__(self, timestamp, server, status):
        self.timestamp = timestamp
        self.server = server
        self.status = status

    def to_dict(self):
        return self.__dict__