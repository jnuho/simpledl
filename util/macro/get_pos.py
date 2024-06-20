import pyautogui as pag
import pygetwindow as gw

# import pydirectinput
from pynput import keyboard,mouse
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
            exit(1)
            # raise KeyboardInterrupt
        
        elif event == KeyCode.from_char('\\'):
            pag.moveTo(400, 1050)
            self.mouse.press(Button.left)
            tick(.02)
            self.mouse.release(Button.left)
            tick(.1)



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

    def on_click(self, x, y, button, pressed):
        if button == Button.left and pressed:
            print(f"Mouse clicked at ({x}, {y})")


def tick(mu):
    time.sleep(random.gauss(mu=mu, sigma=.001))


# The with statement is used to create a context in which the Listener object is active.
# it ensures proper setup and cleanup of the Listener object
# it is concurrent programming, but do not achieve true parallelism because it is a blocking operation 
# make the main thread waits for Listener thread to __exit__()
def run_listener(controller):
    with keyboard.Listener(on_press=controller.on_key_press) as keyboard_listener, mouse.Listener(on_click=controller.on_click) as mouse_listener:
        keyboard_listener.join()
        mouse_listener.join()

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
