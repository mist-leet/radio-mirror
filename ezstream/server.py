import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        # self.path - path
        print(f'GET: {self.path}')
        Utils.send_signal()
        self.send_response(200)
        self.end_headers()


class Utils:

    @classmethod
    def get_ezstream_pid(cls) -> int:
        return int(subprocess.check_output(['pidof', '-s', 'ezstream']))

    @classmethod
    def send_signal(cls):
        subprocess.run("pkill -USR1 ezstream", shell=True, check=True)


webServer = HTTPServer(('0.0.0.0', 8888), Server)
print('sys-utils server start on: http://ezstream:8888/')
webServer.serve_forever()