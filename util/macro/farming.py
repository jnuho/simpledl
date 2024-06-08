import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import Key
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import datetime
import time
import base64
import threading
import random
import os
from dotenv import load_dotenv

load_dotenv()

class GController(object):
    def __init__(self, failsafe=False):
        self.kb = KbController()
        self.mouse = MouseController()
        self.window = None
        self.running = True

        pag.FAILSAFE = failsafe

    def mouse_l_click(self, x, y):
        pag.moveTo(x,y)
        self.mouse.press(Button.left)
        time.sleep(random.gauss(mu=.3, sigma=.001))
        self.mouse.release(Button.left)
        time.sleep(random.gauss(mu=.5, sigma=.001))


    def mouse_r_click(self):
        self.mouse.press(Button.right)
        time.sleep(random.gauss(mu=.3, sigma=.001))
        self.mouse.release(Button.right)
        time.sleep(random.gauss(mu=.5, sigma=.001))

    def pressAndRelease(self, key):
        self.kb.press(key)
        time.sleep(random.gauss(mu=.3, sigma=.001))
        self.kb.release(key)
        time.sleep(random.gauss(mu=.3, sigma=.001))

    def stop(self):
        self.running = False

    def handle_interrupt(signum, frame):
        controller.stop()

    def get_food(self):
        while self.running:
            time.sleep(random.gauss(mu=1, sigma=.001))
            print(datetime.datetime.now())

            windows = []
            title = base64.b64decode(os.getenv("WINDOW_TITLE")).decode("utf-8")
            temp = gw.getWindowsWithTitle(title)
            for w in temp:
                if w.title == title:
                    windows.append(w)
            del temp

            for i, _ in enumerate(windows):
                w = windows[len(windows)-1-i]

                time.sleep(random.gauss(mu=.5, sigma=.001))
                w.minimize()
                w.restore()
                # w.activate()
                w.moveTo(60 +30*i, 3)
                print(w)
                time.sleep(random.gauss(mu=.8, sigma=.001))

                self.mouse_l_click(w.left + (w.width*.2049), w.top + (w.height*.4341))
                self.pressAndRelease(Key.enter)
                self.pressAndRelease(Key.esc)
                self.pressAndRelease('i')

                # Food
                pag.moveTo(w.left + (w.width*.5835), w.top + (w.height*.2484))
                time.sleep(random.gauss(mu=.3, sigma=.001))

                self.mouse_r_click()
                self.mouse_r_click()
                self.mouse_r_click()
                self.mouse_r_click()

                time.sleep(random.gauss(mu=.3, sigma=.001))
                self.pressAndRelease('j')
                time.sleep(random.gauss(mu=.3, sigma=.001))
                self.mouse_l_click(w.left + (w.width*.2049), w.top + (w.height*.4341))
                time.sleep(random.gauss(mu=.3, sigma=.001))
                self.pressAndRelease('j')

            time.sleep(random.gauss(mu=25*60, sigma=1))


    def cleanup(self):
        while self.running:

            time.sleep(random.gauss(mu=24*60*60, sigma=.5))

            windows = []
            title = base64.b64decode(os.getenv("WINDOW_TITLE")).decode("utf-8")
            temp = gw.getWindowsWithTitle(title)
            for w in temp:
                if w.title == title:
                    windows.append(w)
            del temp

            for i, _ in enumerate(windows):
                w = windows[len(windows)-1-i]

                time.sleep(random.gauss(mu=.5, sigma=.001))
                w.minimize()
                w.restore()
                # w.activate()
                w.moveTo(60 +30*i, 3)
                print(w)
                time.sleep(random.gauss(mu=.8, sigma=.001))

                # game_window.activate()
                self.mouse_l_click(w.left + (w.width*.2049), w.top + (w.height*.4341))
                self.pressAndRelease(Key.enter)
                self.pressAndRelease('i')
                
                # MOVE ITEMS
                self.mouse_l_click(w.left + (w.width*.2029), w.top + (w.height*.5747))
                self.mouse_l_click(w.left + (w.width*.5796), w.top + (w.height*.6261))
                # self.mouse_l_click(w.left + (w.width*.7068), w.top + (w.height*.729))
                self.pressAndRelease('5')
                self.pressAndRelease('0')
                self.pressAndRelease('0')


                self.pressAndRelease(Key.enter)

                self.mouse_l_click(w.left + (w.width*.2417), w.top + (w.height*.5747))
                self.mouse_l_click(w.left + (w.width*.5796), w.top + (w.height*.6261))
                # self.mouse_l_click(w.left + (w.width*.7068), w.top + (w.height*.729))
                self.pressAndRelease('5')
                self.pressAndRelease('0')
                self.pressAndRelease('0')
                self.pressAndRelease(Key.enter)
                
                self.mouse_l_click(w.left + (w.width*.2845), w.top + (w.height*.5747))
                self.mouse_l_click(w.left + (w.width*.5796), w.top + (w.height*.6261))
                # self.mouse_l_click(w.left + (w.width*.7068), w.top + (w.height*.729))
                self.pressAndRelease('5')
                self.pressAndRelease('0')
                self.pressAndRelease('0')
                self.pressAndRelease(Key.enter)

                # 아이템 삭제
                self.pressAndRelease('j')
                
                self.mouse_l_click(w.left + (w.width*.8524), w.top + (w.height*.6826))
                self.mouse_l_click(w.left + (w.width*.668), w.top + (w.height*.2472))
                # self.mouse_l_click(w.left + (w.width*.799), w.top + (w.height*.3476))
                self.pressAndRelease('5')
                self.pressAndRelease('0')
                self.pressAndRelease('0')
                self.pressAndRelease(Key.enter)
                self.pressAndRelease(Key.enter)

                self.mouse_l_click(w.left + (w.width*.7097), w.top + (w.height*.2472))
                # self.mouse_l_click(w.left + (w.width*.8417), w.top + (w.height*.3425))
                self.pressAndRelease('5')
                self.pressAndRelease('0')
                self.pressAndRelease('0')
                self.pressAndRelease(Key.enter)
                self.pressAndRelease(Key.enter)

                #다시시작
                self.pressAndRelease('j')
                self.mouse_l_click(w.left + (w.width*.2049), w.top + (w.height*.4341))
                self.pressAndRelease('j')


if __name__ == "__main__":
    controller = GController()

    # Create two threads
    food_thread = threading.Thread(target=controller.get_food)
    cleanup_thread = threading.Thread(target=controller.cleanup)

    # Start both threads
    food_thread.start()
    cleanup_thread.start()

    # Wait for both threads to finish (which won't happen in this case)
    food_thread.join()
    cleanup_thread.join()
