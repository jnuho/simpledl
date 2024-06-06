import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import time
import base64
import random
import os
from dotenv import load_dotenv

load_dotenv()

class GController(object):
    def __init__(self, failsafe=False, monster_type=0, req_food=True):
        self.kb = KbController()
        self.mouse = MouseController()
        self.window = None
        self.req_food = req_food

        self.monster = ["dsa", "3c", "raide"][monster_type]
        self.resv_attack_cnt = {
            "dsa": {
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

        pag.FAILSAFE = failsafe

        title = base64.b64decode(os.getenv("WINDOW_TITLE")).decode("utf-8")
        windows = gw.getWindowsWithTitle(title)
        for w in windows:
            if w.title == title:
                self.window = w
                break

    def get_food(self):
        try:
            pos_found = pag.locateCenterOnScreen("util/images/food.png", confidence=.93, grayscale=True)
            # 150 바 = 687-537
            # 248: 100%        # -310 일때 길이: 225
            x_diff = pos_found.x - self.window.left
            if x_diff < 224:
                self.kb.press(Key.alt)
                time.sleep(random.gauss(mu=.05, sigma=.0005))
                for i in range(2):
                    self.kb.press('2')
                    time.sleep(random.gauss(mu=.2, sigma=.0005))
                    self.kb.release('2')
                    time.sleep(random.gauss(mu=.2, sigma=.0005))
                self.kb.release(Key.alt)
        except pag.ImageNotFoundException:
            print("not found")


    def pressAndRelease(self, key):
        # mu : mean
        # sigma : standard deviation, assuming a 6-sigma range for 99.7% coverage
        self.kb.press(key)
        time.sleep(random.gauss(mu=.018, sigma=.0001/6))
        self.kb.release(key)
        time.sleep(random.gauss(mu=.018, sigma=.0001/6))


    def retreat(self):
        self.kb.press(Key.esc)
        time.sleep(random.gauss(mu=.1, sigma=.0005))
        self.kb.release(Key.esc)
        time.sleep(random.gauss(mu=.1, sigma=.0005))
        self.kb.press(Key.esc)
        time.sleep(random.gauss(mu=.1, sigma=.0005))
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
            self.mouse.press(Button.left)
            time.sleep(random.gauss(mu=.02, sigma=.0005))
            self.mouse.release(Button.left)
            time.sleep(random.gauss(mu=.02, sigma=.0005))
        # if event.name == 'a':
        elif event == KeyCode.from_char(','):
            self.kb.press(Key.left)
            time.sleep(random.gauss(mu=.55, sigma=.0005))
            self.kb.release(Key.left)
        # elif event.name == 'd':
        elif event == KeyCode.from_char('/'):
            self.kb.press(Key.right)
            time.sleep(random.gauss(mu=.55, sigma=.0005))
            self.kb.release(Key.right)
        # elif event.name == 'w':
        elif event == KeyCode.from_char(';'):
            self.kb.press(Key.up)
            time.sleep(random.gauss(mu=.55, sigma=.0005))
            self.kb.release(Key.up)
        # elif event.name == 's':
        elif event == KeyCode.from_char('.'):
            self.kb.press(Key.down)
            time.sleep(random.gauss(mu=.55, sigma=.0005))
            self.kb.release(Key.down)
        # debuf & move
        # elif event.name == 'q':
        elif event == KeyCode.from_char('['):
            # q 디버프
            self.pressAndRelease('q')
            time.sleep(random.gauss(mu=.05, sigma=.0001))
            self.pressAndRelease('w')
            time.sleep(random.gauss(mu=.1, sigma=.0001))

            self.pressAndRelease('2')
            self.mouse.press(Button.right)
            time.sleep(random.gauss(mu=.015, sigma=.0001))
            self.mouse.release(Button.right)
            time.sleep(random.gauss(mu=.05, sigma=.0001))

            self.pressAndRelease('`')
            self.mouse.press(Button.right)
            time.sleep(random.gauss(mu=.02, sigma=.0001))
            self.mouse.release(Button.right)
            time.sleep(random.gauss(mu=.01, sigma=.0001))
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
                time.sleep(random.gauss(mu=.01, sigma=.0001))

        # elif event.name == 'x':
        elif event == KeyCode.from_char('\''):
            self.retreat()

            if self.req_food:
                time.sleep(random.gauss(mu=1.65, sigma=.001))
                self.get_food()


if __name__ == "__main__":
    # ["dsa", "3c", "raide"]
    controller = GController(monster_type=0, req_food=True)

    # The with statement is used to create a context in which the Listener object is active.
    # it ensures proper setup and cleanup of the Listener object
    # it is concurrent programming, but do not achieve true parallelism because it is a blocking operation 
    # make the main thread waits for Listener thread to __exit__()
    with Listener(on_press=controller.on_key_press) as listener:
        listener.join()
