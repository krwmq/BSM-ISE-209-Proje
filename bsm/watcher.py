import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    DIRECTORY_TO_WATCH = "/home/krm/bsm/test"  # İzlenecek dizin

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        print(f"Watching for changes in: {self.DIRECTORY_TO_WATCH}")
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    LOG_FILE = "/home/krm/bsm/logs/changes.json"  # Log dosyasının yolu

    def on_any_event(self, event):
        if event.is_directory:
            return None
        else:
            print(f"Event: {event.event_type}, File: {event.src_path}")  # Konsola yazdırma
            log = {
                "event_type": event.event_type,
                "src_path": event.src_path,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.LOG_FILE, "a") as f:
                json.dump(log, f)
                f.write("\n")

if __name__ == '__main__':
    w = Watcher()
    w.run()
