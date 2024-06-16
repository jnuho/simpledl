import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import Key
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import time
import base64
import threading
import random
import os
from dotenv import load_dotenv

load_dotenv()

class GController(object):
    def __init__(self):
        self.kb = KbController()
        self.mouse = MouseController()
        self.window = None
        self.running = True

        pag.FAILSAFE = False

    def mouse_l_click(self, x, y):
        x = random.gauss(mu=x, sigma=.03)
        y = random.gauss(mu=y, sigma=.03)
        pag.moveTo(x,y)
        self.mouse.press(Button.left)
        tick(.33)
        self.mouse.release(Button.left)
        tick(.5)

    def mouse_r_click(self):
        self.mouse.press(Button.right)
        tick(.33)
        self.mouse.release(Button.right)
        tick(.5)

    def pressAndRelease(self, key):
        self.kb.press(key)
        tick(.33)
        self.kb.release(key)
        tick(.3)

    def stop(self):
        self.running = False

    def cleanup(self):
        # while self.running:
        if self.running:

            windows = []
            title = base64.b64decode(os.getenv("G_WINDOW_TITLE")).decode("utf-8")
            for w in gw.getWindowsWithTitle(title):
                if w.title == title:
                    windows.append(w)

            for i, _ in enumerate(windows):
                w = windows[len(windows)-1-i]

                tick(.5)
                w.minimize()
                w.restore()
                # w.activate()
                w.moveTo(60 +30*i, 3)
                print(w)
                tick(.8)

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

def tick(mu):
    time.sleep(random.gauss(mu=mu, sigma=.001))

if __name__ == "__main__":
    c1 = GController()

    # Create two threads
    cleanup_thread = threading.Thread(target=c1.cleanup)

    # Start both threads
    cleanup_thread.start()

    # Wait for both threads to finish (which won't happen in this case)
    cleanup_thread.join()
