import pyautogui as pag
import pygetwindow as gw

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


class GController(object):
    def __init__(self, monster="dosa", req_food=True):
        self.kb = KbController()
        self.mouse = MouseController()
        # self.window = None

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
            "1c": {
                2: 0,
                1: 0,
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

        if self.monster == "3c":
            position_windows()
  

    def get_food(self):
        try:
            # TODO region=()
            pos_1 = pag.locateCenterOnScreen("util/images/food_1.png", confidence=.93, grayscale=True)
            pos_0 = pag.locateCenterOnScreen("util/images/food_0.png", confidence=.93, grayscale=True)
            # 147 bar
            x_diff = pos_1.x - pos_0.x
            # < 90%
            if x_diff < 132:
                self.kb.press(Key.alt)
                tick(.05)
                for i in range(2):
                    self.kb.press('2')
                    tick(.2)
                    self.kb.release('2')
                    tick(.2)
                self.kb.release(Key.alt)
        except:
            print(traceback.format_exc())
            print("not found")


    def pressAndRelease(self, key):
        # mu : mean
        # sigma : standard deviation, assuming a 6-sigma range for 99.7% coverage
        self.kb.press(key)
        tick(.0181, .0001)
        self.kb.release(key)
        tick(.0181, .0001)


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
        # a: ,
        # d: /
        # w: ;
        # s: .
        # q: [
        # e: ]
        # c: \
        # x: '
        if event == Key.f11:
            print("> You pressed F11. Exiting gracefully.")
            raise KeyboardInterrupt
        elif event == Key.f10:
            # while True:
            #     for i in range(10):
            self.mouse.press(Button.left)
            tick(.02)
            self.mouse.release(Button.left)
            tick(.05)
        # if event.name == 'a':
        elif event == KeyCode.from_char(','):
            self.kb.press(Key.left)
            tick(.55)
            self.kb.release(Key.left)
        # elif event.name == 'd':
        elif event == KeyCode.from_char('/'):
            self.kb.press(Key.right)
            tick(.55)
            self.kb.release(Key.right)
        # elif event.name == 'w':
        elif event == KeyCode.from_char(';'):
            self.kb.press(Key.up)
            tick(.55)
            self.kb.release(Key.up)
        # elif event.name == 's':
        elif event == KeyCode.from_char('.'):
            self.kb.press(Key.down)
            tick(.55)
            self.kb.release(Key.down)
        # debuf & move
        # elif event.name == 'q':
        elif event == KeyCode.from_char('['):
            # q 디버프
            self.pressAndRelease('q')
            tick(.05)
            self.pressAndRelease('w')
            tick(.1)

            self.pressAndRelease('2')
            tick(.015)
            self.mouse.press(Button.right)
            tick(.015)
            self.mouse.release(Button.right)
            tick(.05)

            self.pressAndRelease('`')
            self.mouse.press(Button.right)
            tick(.02)
            self.mouse.release(Button.right)
            tick(.02)
            self.pressAndRelease('=')

        # 보호
        # elif event.name == 'e':
        elif event == KeyCode.from_char(']'):
            self.pressAndRelease('-')
            self.pressAndRelease('r')

        # elif event.name == 'c':
        elif event == KeyCode.from_char('\\'):
            for k, v in self.resv_attack_cnt.items():
                self.pressAndRelease(f"{k}")
                self.pressAndRelease('r')
                for _ in range(v):
                    self.pressAndRelease('e')
                tick(.02)

        # elif event.name == 'x':
        elif event == KeyCode.from_char('\''):

            if self.monster == "3c":
                pag.moveTo(1372, 1055)
                self.mouse.press(Button.left)
                tick(.02)
                self.mouse.release(Button.left)
                tick(.1)

                # find all instances of an image
                rectangles = getRectangles('util/images/logo.png')
                for i, (x, y, w, h) in enumerate(rectangles, start=1):
                    pag.moveTo(x+w/2, y+h/2)
                    self.mouse.press(Button.left)
                    tick(.03)
                    self.mouse.release(Button.left)
                    tick(.05)
                    self.retreat()
                    tick(.2)

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
            else:
                self.retreat()


            if self.req_food:
                tick(1.65)
                self.get_food()

            if self.monster == "3c" and self.req_food: 
                pag.moveTo(1372, 1055)
                self.mouse.press(Button.left)
                tick(.02)
                self.mouse.release(Button.left)
                tick(.1)

                # find all instances of an image
                rectangles = getRectangles('util/images/logo.png')
                for i, (x, y, w, h) in enumerate(rectangles, start=1):
                    pag.moveTo(x+w/2, y+h/2)
                    self.mouse.press(Button.left)
                    tick(.03)
                    self.mouse.release(Button.left)
                    tick(.2)
                    self.get_food()
                    tick(.2)


def position_windows():
    windows = []
    title = base64.b64decode(os.getenv("G_WINDOW_TITLE")).decode("utf-8")
    for w in gw.getWindowsWithTitle(title):
        if w.title == title:
            windows.append(w)
    for i, _ in enumerate(windows):
        w = windows[len(windows)-1-i]
        w.moveTo(60 +410*i, 3 + 110*i)
        # w.minimize()
        # w.restore()
        # w.activate()
        # tick(3)

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


def tick(mu, sigma=.001):
    # mu : mean
    # sigma : standard deviation, assuming a 6-sigma range for 99.7% coverage
    time.sleep(random.gauss(mu=mu, sigma=sigma))

# The with statement is used to create a context in which the Listener object is active.
# it ensures proper setup and cleanup of the Listener object
# it is concurrent programming, but do not achieve true parallelism because it is a blocking operation 
# make the main thread waits for Listener thread to __exit__()
def run_listener(controller):
    with Listener(on_press=controller.on_key_press) as listener:
        listener.join()


if __name__ == "__main__":
    # ["dosa", "1c", "3c", "raide"]
    monster = "dosa"
    req_food = 1
    c1 = GController(monster, req_food)

    # Assuming c1 and c2 are already defined and have an on_key_press method
    thread1 = threading.Thread(target=run_listener, args=(c1,))
    # thread2 = threading.Thread(target=run_listener, args=(c2,))

    thread1.start()
    # thread2.start()

    # Optionally, join the threads if you want to wait for them to finish
    thread1.join()
    # thread2.join()
