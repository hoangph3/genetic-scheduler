from core.scheduler import timetable
import os
import time
import json


if __name__ == "__main__":
    with open('data.json') as f:
        data = json.load(f)
    path = os.path.join("logs", str(int(time.time())))
    timetable(path, data)
