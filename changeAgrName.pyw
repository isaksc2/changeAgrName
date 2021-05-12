import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
import sys
import os
from datetime import date
from datetime import datetime
import threading

filename1 = "a.bvh"
filename2 = "output.agr"


class Watcher:
    def __init__(self, path, filename):
        self.observer = Observer()
        self.path = path
        self.filename = filename

    def run(self):
        event_handler = Handler(self.filename)
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(PatternMatchingEventHandler):
    def __init__(self, filename):
        super(Handler, self).__init__(
            patterns=[filename],
            ignore_patterns=["*.tmp"],
            ignore_directories=True,
            case_sensitive=False,
        )

    def rename(old):
        time.sleep(5)
        parts = old.split(".")
        type = parts[len(parts)-1]
        today = date.today()
        now = datetime.now()
        new = today.strftime("%Y-%m-%d ") + now.strftime("%H-%M-%S.") + type
        os.rename(old,new)

    def on_created(self, event):
        old = event.src_path
        print(old)
        Handler.rename(old)

    def on_moved(self, event):
        old = event.dest_path
        print(old)
        Handler.rename(old)



    def on_any_event(self, event):
        print(
            "[{}] noticed: [{}] on: [{}] ".format(
                time.asctime(), event.event_type, event.src_path
            )
        )

        


if __name__ == "__main__":
    print("changeAgrName started")
    path = "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/"
    w1 = Watcher(path, filename1)
    w2 = Watcher(path, filename2)

    t1 = threading.Thread(target=w1.run, args=())
    t2 = threading.Thread(target=w2.run, args=())
    t1.start()
    t2.start()