import threading
import time

import requests
import schedule
from flask import Flask

# this import needs to be relative (.views.ind...) as views is not a package
from .views.index import index_views


class BackgroundTasks(threading.Thread):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.base_url = "http://localhost:5000"

    def text_log(self, text):
        with open("log.txt", "a") as f:
            f.write(f"{time.ctime()} => {self.base_url} => {text}\n")

    def job(self):
        try:
            res = requests.get(self.base_url)
            self.text_log(f"{res.status_code}")
        except Exception as e:
            self.text_log(f"Error: {e}")
            return

    def run(self, *args, **kwargs):
        if self.count < 1:
            self.count += 1

            schedule.every(3).seconds.do(self.job)

            while True:
                schedule.run_pending()
                time.sleep(1)


bt = BackgroundTasks()


def create_app():
    app = Flask(__name__)

    index_views(app)

    bt.start()

    return app
