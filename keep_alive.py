from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "I am live"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()
