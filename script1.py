#!/usr/bin/env python3
from picrawler import Picrawler
from vilib import Vilib
from robot_hat import TTS, Music
from robot_hat import Ultrasonic
from robot_hat import Pin
from time import localtime, strftime, sleep
import readchar
from image import capture_image

# crawler movement
crawler = Picrawler()
sonar = Ultrasonic(Pin("D2"), Pin("D3"))
alert_distance = 15

# tts and audio
tts = TTS()
tts.lang("en-US")
music = Music()

# camera and video
VIDEO_PATH = f"/home/pi/recs"
CAPTURE_PATH = f"/home/pi/pics"

manual = """
Script1 build off of keyboard_control.py from examples
Ideas for script expansion:

- vision ()
- tts ()

Press keys on keyboard to control PiCrawler!
    W: Forward
    A: Turn left
    S: Backward
    D: Turn right
    X: Sit/Stand

    1-0: Set speed (10-100). Default: 80
      NOTE: Speed is set in increments of 10. Cannot be set to 0

    T: activate TTS engine (WIP)
    H: "Hello, I am PiCrawler!" (audio description manual)
    C: activate camera (alpha)
    SPACE: take a photo (alpha)
      NOTE: Saved under '~/pics/'
    'Q': record video (WIP)
      NOTE: Saved under '~/recs/'
      NOTE: Once started, press 'Q' again to pause/resume the recording

    Ctrl^C: Quit
"""

def show_info():
    print("\033[H\033[J", end="")  # clear terminal windows
    print(manual)

# camera functions
def camera_activate(cam_on):
    if cam_on == False:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=False, web=True)
        print("\nCamera Activated!")
    elif cam_on == True:
        Vilib.camera_close()
        print("\nCamera Deactivated")

def capture_image(filename):
    status = Vilib.take_photo(filename, path=CAPTURE_PATH)
    if status:
        print("Photo Captured!\nSaved as:%s/%s.jpg" % (CAPTURE_PATH, filename))
    else:
        print("Capture Failed :(")

# main running loop function
def main():
    # flags
    cam_on = False
    rec_flag = "stop"  # [start, stop, pause]
    standing = True

    # settings
    speed = 80
    Vilib.rec_video_set["path"] = VIDEO_PATH

    # crawler.do_step(STAND, speed)
    crawler.do_step("stand", speed)

    show_info()
    while True:
        key = readchar.readkey()
        key = key.lower()
        # movement
        if key in ("wsad"):
            if "w" == key:
                crawler.do_action("forward", 1, speed)
            elif "s" == key:
                crawler.do_action("backward", 1, speed)
            elif "a" == key:
                crawler.do_action("turn left", 1, speed)
            elif "d" == key:
                crawler.do_action("turn right", 1, speed)
            sleep(0.05)
            show_info()

        # sit/stand
        elif key == "x":
            if standing:
                crawler.do_step(SIT, speed)
                standing = False
            else:
                crawler.do_step(STAND, speed)
                standing = True
            sleep(0.5)

        elif key in ("123456789"):
            speed = int(key) * 10
            print(f"Speed set to {speed}")

        # camera activation
        elif key == "c":
            camera_activate(cam_on)
            cam_on = not cam_on  # toggle camera state
            sleep(0.5)

        # capture image
        elif key == readchar.key.SPACE:
            curr_time = strftime("%Y-%m-%d-%H.%M.%S", localtime())
            capture_image(curr_time)
            sleep(0.5)

        # record video
        elif key == "q":
            # start
            if rec_flag == "stop":
                rec_flag = "start"
                # set name
                vname = strftime("%Y-%m-%d-%H.%M.%S", localtime())
                Vilib.rec_video_set["name"] = vname
                # start record
                Vilib.rec_video_run()
                Vilib.rec_video_start()
                print("Recording Started!")
            # pause
            elif rec_flag == "start":
                rec_flag = "pause"
                Vilib.rec_video_pause()
                print("Recording Paused!")
            # resume
            elif rec_flag == "pause":
                rec_flag = "start"
                Vilib.rec_video_start()
                print("Recording Resumed!")

        # stop recording
        elif key == "e" and rec_flag != "stop":
            rec_flag = "stop"
            Vilib.rec_video_stop()
            print(
                "The video saved as %s%s.avi\n" % (Vilib.rec_video_set["path"], vname)
            )

        # TTS
        elif key == "t":
            greetings = "Hello, I am PiCrawler!"
            explain = "I am a robot designed for educational purposes. I can move in all directions, take photos, and record videos. I am controlled by a Raspberry Pi, and I am programmed in Python."
            warning = (
                "But be careful and don't let me out... I might take over the world!"
            )

            crawler.do_step("sit", speed)
            tts.say(greetings)
            sleep(0.5)
            tts.say(explain)
            sleep(0.5)
            tts.say(warning)
            sleep(0.05)
            crawler.do_step("stand", speed)
            music.music_play("rsrc/warning.mp3")
            sleep(0.5)
            tts.say("Just kidding! I am here to help you!")
            crawler.do_action("wave", speed)

        # quit
        elif key == readchar.key.CTRL_C or key in readchar.key.ESCAPE_SEQUENCES:
            crawler.do_step("sit", speed)
            if rec_flag != "stop":
                Vilib.rec_video_stop()
            print("\nQuit")
            break

        sleep(0.02)


if __name__ == "__main__":
    main()
