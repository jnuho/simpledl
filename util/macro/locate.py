import pyautogui as pag
import pygetwindow as gw

# import pydirectinput
from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import threading

import time
import base64
import random
import os
import traceback
from dotenv import load_dotenv

from PIL import ImageGrab
import cv2
import numpy as np

load_dotenv()

class LocateController(object):
    def __init__(self, monster="dosa", req_food=True):
        self.kb = KbController()
        self.mouse = MouseController()
        self.window = None

        self.monster = monster
        self.req_food = req_food
        self.resv_attack_cnt = {
            "dosa": {
                8: 0,
                2: 1,
                1: 0,
                4: 1,
                5: 1,
                6: 0,
            },
            "3c": {
                2: 0,
                1: 0,
                4: 0,
            },
            "raide": {
                8: 0,
                2: 1,
                1: 0,
                4: 0,
                5: 0,
            },
        }[self.monster]

        pag.FAILSAFE = False


    def pressAndRelease(self, key):
        # mu : mean
        # sigma : standard deviation, assuming a 6-sigma range for 99.7% coverage
        self.kb.press(key)
        tick(.018)
        self.kb.release(key)
        tick(.018)


    def retreat(self):
        self.kb.press(Key.esc)
        tick(.1)
        self.kb.release(Key.esc)
        tick(.1)
        self.kb.press(Key.esc)
        tick(.1)
        self.kb.release(Key.esc)


    # pag.keyboard not working
    def on_key_press(self, event):
        if event == Key.f11:
            print("> You pressed F11. Exiting gracefully.")
            raise KeyboardInterrupt
        elif event == KeyCode.from_char('\\'):
            try:
                # TODO region=()
                pos_100 = pag.locateCenterOnScreen("util/images/food_100.png", confidence=.93, grayscale=True)
                pos_0 = pag.locateCenterOnScreen("util/images/food_0.png", confidence=.93, grayscale=True)
                # 150 바 = 687-537
                # 248: 100%        # -310 일때 길이: 225
                x_diff = pos_100.x - pos_0.x
                print(x_diff)
                if x_diff < 224:
                    print("LALALAL")
            except:
                print(traceback.format_exc())
                print("not found")

            # pag.moveTo(400, 1050)
            # self.mouse.press(Button.left)
            # tick(.02)
            # self.mouse.release(Button.left)
            # tick(.1)
            # find all instances of an image
            # rectangles = getRectangles('util/images/logo.png')
            # for i, (x, y, w, h) in enumerate(rectangles, start=1):
            #     pag.moveTo(x+w/2, y+h/2)
            #     self.mouse.press(Button.left)
            #     tick(.03)
            #     self.mouse.release(Button.left)
            #     tick(.3)


            # # Print the locations
            # if len(rectangles) == 0:
            #     print("No instances of 'util/images/logo.png' found on the screen.")
            # else:
            #     print(f"Found {len(rectangles)} instances of 'util/images/logo.png' on the screen:")
            #     for i, (x, y, w, h) in enumerate(rectangles, start=1):
            #         print(f"Instance {i}: x={x}, y={y}, width={w}, height={h}")

            # # Optional: Draw rectangles on the screen capture to visualize the matches
            # for (x, y, w, h) in rectangles:
            #     cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # # Show the screen capture with rectangles drawn
            # cv2.imshow('Matches', screen)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

def getRectangles(image_path):
    # Capture the screen
    screen = np.array(ImageGrab.grab())

    # Convert the screen capture to grayscale
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # Load the template image
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    # Perform template matching
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)

    # Define a threshold
    threshold = 0.8

    # Get the locations of the matched regions
    loc = np.where(result >= threshold)

    # List to hold the rectangles where the template matches
    rectangles = []
    for pt in zip(*loc[::-1]):
        rectangles.append([int(pt[0]), int(pt[1]), int(w), int(h)])
        rectangles.append([int(pt[0]), int(pt[1]), int(w), int(h)])

    # Use groupRectangles to group overlapping rectangles
    rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
    return rectangles


def tick(mu):
    time.sleep(random.gauss(mu=mu, sigma=.001))


# The with statement is used to create a context in which the Listener object is active.
# it ensures proper setup and cleanup of the Listener object
# it is concurrent programming, but do not achieve true parallelism because it is a blocking operation 
# make the main thread waits for Listener thread to __exit__()
def run_listener(controller):
    with Listener(on_press=controller.on_key_press) as listener:
        listener.join()

if __name__ == "__main__":
    # [0,      1,    2,      3,      4  ]
    # ["dosa", "1c", "3c", "raide", "cho"]
    # controller = GController(monster="dosa", req_food=True)
    c1 = LocateController(monster="3c", req_food=False)


    # Assuming controller1 and controller2 are already defined and have an on_key_press method
    thread1 = threading.Thread(target=run_listener, args=(c1,))

    thread1.start()

    # Optionally, join the threads if you want to wait for them to finish
    thread1.join()
