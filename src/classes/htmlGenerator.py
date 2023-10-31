import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time 

class HTMLGenerator:
    def __init__(self, template_file):
        self.template_file = template_file

    def generate_html_report(self, log_file):
        with open(log_file, 'r') as file:
            logs = json.load(file)

        with open(self.template_file, 'r') as template:
            template_content = template.read()

        table_content = ""
        for log in logs:
            table_content += f"<tr><td>{log['timestamp']}</td><td>{log['server']}</td><td>{log['status']}</td></tr>"

        html_report = template_content.replace("{{table_content}}", table_content)

        return html_report

    def serve_html(self, html_content, port):
        server_address = ("", port)

        class HTMLRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html_content.encode("utf-8"))

        httpd = HTTPServer(server_address, HTMLRequestHandler)
        print(f"Serving HTML on port {port}")
        httpd.server_activate()
        httpd.handle_request()
        time.sleep(120)
        httpd.server_close()  


