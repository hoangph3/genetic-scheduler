from utils.data import Data
from core.scheduler import timetable
import os
import time


if __name__ == "__main__":
    # Data()
    path = os.path.join("logs", str(int(time.time())))
    timetable(path)
