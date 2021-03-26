import time
from flask import Flask, render_template, request
import requests
import eventlet.wsgi
import time
from datetime import datetime
import json

app = Flask(__name__)


def log(msg):
    print(f"{datetime.now().strftime('%d:%m:%Y %H:%M:%S')} — {msg}")
    return True


while True:
    # get the branch id
    try:
        data = requests.post("http://localhost:9000/this/branch")
        if data.ok:
            try:
                if data.json():
                    data = data.json()
                    key = data["key_"]
                    sync = requests.post("http://localhost:1000/sync/init",json={"key":key})
                    log("Synced")
            except json.decoder.JSONDecodeError:
                log("Error!, could not obtain key")
    except requests.exceptions.ConnectionError:
        log("Server not Reachaable")

    time.sleep(20)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 9900)), app)
