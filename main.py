from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import urllib.parse
import pathlib
import mimetypes
import json

class HttpHandler(BaseHTTPRequestHandler):
  __data_file__ = 'storage/data.json'

  def do_GET(self):
    pr_url = urllib.parse.urlparse(self.path)
    if pr_url.path == '/':
      self.send_html_file('index.html')
    elif pr_url.path == '/message':
      self.send_html_file('message.html')
    elif pr_url.path == '/read':
      self.send_data()
    else:
      if pathlib.Path().joinpath(pr_url.path[1:]).exists():
        self.send_static()
      else:
        self.send_html_file('error.html', 404)

  def do_POST(self):
    data_parse = urllib.parse.unquote_plus(self.rfile.read(int(self.headers['Content-Length'])).decode())
    data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
    print(data_dict)
    data = self.read_data()
    data[str(datetime.now())] = data_dict
    self.write_data(data)
    self.send_response(302)
    self.send_header('Location', '/read')
    self.end_headers()

  def send_html_file(self, filename, status=200):
    self.send_response(status)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    with open(filename, 'rb') as fd:
      self.wfile.write(fd.read())

  def send_static(self):
    self.send_response(200)
    mt = mimetypes.guess_type(self.path)
    if mt:
      self.send_header("Content-type", mt[0])
    else:
      self.send_header("Content-type", 'text/plain')
    self.end_headers()
    with open(f'.{self.path}', 'rb') as file:
      self.wfile.write(file.read())

  def send_data(self):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('read.tmpl')
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write(template.render(data=self.read_data(), ).encode('utf-8'))

  def read_data(self):
    with open(self.__data_file__, 'r') as data_file:
      data = json.load(data_file)
      return data

  def write_data(self, data):
    with open(self.__data_file__, 'w', encoding='utf-8') as data_file:
      json.dump(data, data_file, ensure_ascii=False, indent=4)

def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == '__main__':
    run()
