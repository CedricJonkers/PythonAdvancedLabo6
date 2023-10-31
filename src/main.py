import sys
import time
from model.server import Server
from model.log import Log
from repository.serverRepository import ServerRepository
from repository.logRepository import LogRepository
from classes.serverChecker import ServerChecker
from classes.htmlGenerator import HTMLGenerator
from rich.console import Console
from rich.table import Table
import json
import os
from datetime import datetime


console = Console()
with open("config.json", "r") as config_file:
    config = json.load(config_file)
logs_file_path = os.path.join("..", config.get("logs_file"))
servers_file_path = os.path.join("..", config.get("servers_file"))
html_template_path = os.path.join("..", config.get("html_template"))

if not os.path.isfile(servers_file_path) or os.path.getsize(servers_file_path) == 0:
    with open(servers_file_path, "w") as servers_file:
        json.dump([], servers_file)

if not os.path.isfile(logs_file_path) or os.path.getsize(logs_file_path) == 0:
    with open(logs_file_path, "w") as logs_file:
        json.dump([], logs_file)


def main():
    if len(sys.argv) < 2:
        return

    mode = sys.argv[1]

    if mode == "management":
        while True:
            choice = input("Choose an action (add, remove, list, quit): ")
            if choice == "add":
                name = input("Enter server name: ")
                ip = input("Enter server IP: ")
                server = Server(name, ip)
                server_repo.add_server(server)
                console.print(f"Server '{server.name}' added.", style="bold green")
            elif choice == "remove":
                name = input("Enter server name to remove: ")
                server_repo.remove_server(name)
                console.print(f"Server '{name}' removed.", style="bold green")
            elif choice == "list":
                servers = server_repo.list_servers()
                table = Table(title="Registered Servers")
                table.add_column("Server Name", style="cyan")
                table.add_column("Server IP", style="green")
                for server in servers:
                    table.add_row(server['name'], server['ip'])
                console.print(table)
            elif choice == "quit":
                break
            else:
                console.print("Invalid choice. Please try again.", style="bold red")

    elif mode == "check":
        while True:
            servers = server_repo.list_servers()
            for server_data in servers:
                server = Server(server_data['name'], server_data['ip'])
                status = server_checker.ping_server(server)
                now = datetime.now()
                formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                log_entry = Log(formatted_time, server.name, status)
                log_repo.save_log_entry(log_entry)
                console.print(f"Server: {server.name}, Status: {status}", style="bold blue")
            html_report = html_generator.generate_html_report(logs_file_path)
            html_generator.serve_html(html_report, 8080)
            time.sleep(120)

if __name__ == "__main__":
    server_repo = ServerRepository(servers_file_path)
    log_repo = LogRepository(logs_file_path)
    server_checker = ServerChecker()
    html_generator = HTMLGenerator(html_template_path)
    main()