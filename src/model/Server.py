import json

class ServerEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Server):
            return o.__dict__
        return super().default(o)

class Server:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.status = "Unknown"

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, server_dict):
        server = cls(server_dict['name'], server_dict['ip'])
        server.status = server_dict['status']
        return server
