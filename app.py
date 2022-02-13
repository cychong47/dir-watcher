#!/usr/bin/env python3
import sys
import os
import time
import datetime
import pathlib
import frontmatter
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Log:
    def __init__(self):
        pass

    @staticmethod
    def _timestamp():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def debug(*msg):
        print(Log._timestamp(), *msg)

    def error(*msg):
        print("[E]", Log._timestamp(), *msg)

class Watcher:
    directory_to_watch = []

    def __init__(self, watch_path, notification=False):
        self.observer = Observer()

        for item in watch_path.split(','):
            if pathlib.Path(item).is_dir() == True:
                self.directory_to_watch.append(item)
            else:
                print(f"Skip {item}")

        self.notification = notification
        Log.debug(f"Directory to watch : {self.directory_to_watch}")
        if notification.lower() == "telegram":
            import telegram_send
            tg = telegram_send.MyTelegram()
            tg.send_msg(f"Directory watcher started")

        logging.basicConfig(level=logging.INFO,
                format='%(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')

    def run(self):
        event_handler = Handler(self.notification)

        for item in self.directory_to_watch:
            Log.debug(f"Start watching {item}")
            self.observer.schedule(event_handler, item, recursive=True)

        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, notification):
        notification = notification
        print(f"{notification}")

    @staticmethod
    def on_any_event(event):

        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            if pathlib.Path(event.src_path).suffix.find(".sw") == -1:

                # as file copy is not completed when the 'created' event is received,
                # loop until the file size it not increased and any other process
                # access it
                file_done = False
                file_size = -1
                count = 0


                # if file size is not increased for 5 seconds, believe it
                while count < 3:
                    try:
                        t_file_size = pathlib.Path(event.src_path).stat().st_size
                    except:
                        print(f"Abnormal : fail to get file size {event.src_path}")
                        return

                    if file_size != t_file_size:
                        file_size = t_file_size
                    else:
                        count += 1

                    time.sleep(1)

                while not file_done:
                    try:
                        os.rename(event.src_path, event.src_path)
                        file_done = True
                    except:
                        break

                if notification.lower() == "telegram":
                    import telegram_send
                    tg = telegram_send.MyTelegram()

                directory = pathlib.Path(event.src_path).parent
                if "privee" in str(directory):
                    return

                filename = pathlib.Path(event.src_path).name
                if pathlib.Path(event.src_path).suffix == ".md":
                    with open(event.src_path) as f:
                        post = frontmatter.load(f)
                        songs = [line for line in post.content if line.startswith('*')]

                        try:
                            duration = post.metadata["podcast"]["duration"]
                        except:
                            duration = 0

                    if notification.lower() == "telegram":
                        tg.send_msg(f"{filename}\n{duration}s   {len(songs)} songs\n\n{post.content}")
                    else:
                        Log.debug(f"{filename} {duration}s   {len(songs)} songs")
                else:
                    Log.debug(f"{event.src_path} ({file_size} Bytes)")

                    if notification.lower() == "telegram":
                        tg.send_msg(f"{filename}\n({file_size} Bytes)")
                    else:
                        Log.debug(f"{event.src_path} ({file_size} Bytes)")


#        elif event.event_type == 'modified':
#            # Taken any action here when a file is modified.
#            if pathlib.Path(event.src_path).suffix != ".swp":
#                print(f"{event.src_path} is updated")
#
#                import telegram_send
#                tg = telegram_send.MyTelegram()
#                tg.send_msg(f"{event.src_path} is updated")

if __name__ == '__main__':
    dir_to_watch = os.environ['DIR_TO_WATCH']
    notification = os.environ["NOTIFICATION"] 

    w = Watcher(dir_to_watch, notification)
    w.run()
