from flask import Flask
from threading import Thread

app = Flask('')

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def main(): return "webserver is up."

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()
