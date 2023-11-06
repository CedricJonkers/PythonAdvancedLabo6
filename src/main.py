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
import socket
from classes.inputHandler import InputHandler


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
            print("Choose an action:")
            print("1. Add by IP")
            print("2. Add by Hostname")
            print("3. Remove")
            print("4. List")
            print("5. Quit")
            choice = InputHandler.handle_numeric_choice("Enter the number of your choice: ", 5, "Invalid choice. Please try again.")
            if choice == 1:
                ip = InputHandler.handle_string_input("Enter server IP: ", lambda x: len(x) > 0, "Invalid IP. Please try again.")
                while True:
                    try:
                        name = socket.gethostbyaddr(ip)
                        break
                    except socket.gaierror:
                        ip = InputHandler.handle_string_input("Enter server IP: ", lambda x: len(x) > 0, "Invalid IP. Please try again.")
                server = Server(name[0], ip)
                server_repo.add_server(server)
                console.print(f"Server '{server.name}' added. with ip '{ip}'", style="bold green")
            elif choice == 2:
                hostname = InputHandler.handle_string_input("Enter server hostname: ", lambda x: len(x) > 0, "Invalid Hostname. Please try again.")
                while True:
                    try:
                        ip = socket.gethostbyname(hostname)
                        resolved_hostname = socket.gethostbyaddr(ip)
                        break
                    except socket.herror:
                        hostname = InputHandler.handle_string_input("Enter server hostname: ", lambda x: len(x) > 0, "Invalid Hostname. Please try again.")
                server = Server(resolved_hostname[0], ip)
                server_repo.add_server(server)
                console.print(f"Server '{server.name}' added. with ip '{ip}'", style="bold green")
            elif choice == 3:
                name = InputHandler.handle_string_input("Enter server name: ", lambda x: x in [server['name'] for server in server_repo.list_servers()], "Invalid server name. Please try again.")
                server_repo.remove_server(name)
                console.print(f"Server '{name}' removed.", style="bold green")
            elif choice == 4:
                servers = server_repo.list_servers()
                table = Table(title="Registered Servers")
                table.add_column("Server Name", style="cyan")
                table.add_column("Server IP", style="green")
                for server in servers:
                    table.add_row(server['name'], server['ip'])
                console.print(table)
            elif choice == 5:
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