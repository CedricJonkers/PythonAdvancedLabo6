import json
from model.server import Server, ServerEncoder

class ServerRepository:
    def __init__(self, json_file):
        self.json_file = json_file
        self.servers = self.load_servers()

    def load_servers(self):
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file, object_hook=Server.from_dict)
        except FileNotFoundError:
            return []

    def save_servers(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.servers, file, cls=ServerEncoder)

    def add_server(self, server):
        self.servers.append(server)
        self.save_servers()

    def remove_server(self, name):
        self.servers = [s for s in self.servers if s.name != name]
        self.save_servers()

    def list_servers(self):
        return [server.to_dict() for server in self.servers]