#keeps the bot running on abi's uptime robot account

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "<h1>Hello. I am alive!</h1><br><body>Trapbot Extended</body>"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()