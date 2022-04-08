import datetime
import os
import time
from os.path import isfile
from pathlib import Path
from threading import Thread

from logic.app_logger import logger


class FileDeleter:
    """
    This deletes old files.
    """
    MAX_FILE_AGE_SECONDS: float = datetime.timedelta(minutes=1).seconds
    TICK_SECONDS: float = datetime.timedelta(minutes=5).seconds

    def __init__(self, path: Path):
        self.path: Path = path
        self.deleter_thread: Thread = Thread(target=self.delete_old_files)

    def delete_old_files(self):
        while True:
            only_files = [f for f in os.listdir(self.path) if isfile(self.path / f)]
            now: float = time.time()
            for file in only_files:
                modification_time: float = os.path.getmtime(self.path / file)
                if now - modification_time > FileDeleter.MAX_FILE_AGE_SECONDS:
                    logger.log(f"deleting {self.path / file}")
                    Path(self.path / file).unlink(missing_ok=True)
            time.sleep(FileDeleter.TICK_SECONDS)

    def start(self):
        self.deleter_thread.start()
