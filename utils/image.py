#!/usr/bin/env python3
import time
from vilib import Vilib

CAPTURE_PATH = f"/home/pi/pics"


def capture_image(filename):
    status = Vilib.take_photo(filename, path=CAPTURE_PATH)
    if status:
        print("Photo Captured!\nSaved as:%s/%s.jpg" % (CAPTURE_PATH, filename))
    else:
        print("Capture Failed :(")
    time.sleep(0.1)


def intialize():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)


def main():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)

    path = "/home/pi/Pictures/vilib/photos"

    while True:
        if input() == "q":
            _time = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())
            status = Vilib.take_photo(str(_time), path)
            if status:
                print("The photo save as:%s/%s.jpg" % (path, _time))
            else:
                print("Photo save failed")
            time.sleep(0.1)
