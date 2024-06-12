import time
import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import random


class GController(object):
    def __init__(self, failsafe=False):
        self.kb = KbController()
        self.mouse = MouseController()
        self.window = None
        self.conv_cnt = 7

        pag.FAILSAFE = failsafe


    def pressAndRelease(self, key):
        self.kb.press(key)
        time.sleep(random.gauss(mu=.01, sigma=.001))
        self.kb.release(key)
        time.sleep(random.gauss(mu=.01, sigma=.001))


    def mouse_l_click(self, x, y):
        x = random.gauss(mu=x, sigma=.03)
        y = random.gauss(mu=y, sigma=.03)
        pag.moveTo(x,y)
        self.mouse.press(Button.left)
        time.sleep(random.gauss(mu=.08, sigma=.001))
        self.mouse.release(Button.left)
        time.sleep(random.gauss(mu=.1, sigma=.001))


    def locateToClick(self, keyword):
        # for _ in range(self.conv_cnt):
        try:
            found = pag.locateCenterOnScreen("util/images/" + keyword + ".png", confidence=.93, grayscale=True)
            found_x = random.gauss(mu=found.x, sigma=.03)
            found_y = random.gauss(mu=found.y, sigma=.03)
            self.mouse_l_click(found_x, found_y)

            default_x = self.window.left+self.window.width/2
            default_y = self.window.top +self.window.height/2
            default_x = random.gauss(mu=default_x, sigma=.03)
            default_y = random.gauss(mu=default_y, sigma=.03)
            pag.moveTo(default_x, default_y)

            return True
        except pag.ImageNotFoundException:
            print("`" + keyword + "`" + "NOT FOUND")
            return False

    def check_quest(self):
        self.pressAndRelease('q')
        time.sleep(random.gauss(mu=1, sigma=.001))
        self.locateToClick("check_quest")
        time.sleep(random.gauss(mu=.5, sigma=.001))
        self.pressAndRelease('q')

    def on_key_press(self, event):
        if event == Key.f11:
            print("> You pressed F11. Exiting gracefully.")
            raise KeyboardInterrupt
        elif event == KeyCode.from_char('\\'):

            self.window = gw.getActiveWindow()

            # self.kb.press(Key.left)
            # self.kb.release(Key.left)
            # file = round(datetime.now().timestamp())
            # pag.screenshot(f'util/images/s_{file}.png', region=(window.left, window.top, window.width, window.height))
            for _ in range(self.conv_cnt):
                if self.locateToClick("accept"):
                    break
                if self.locateToClick("next"):
                    continue
                if self.locateToClick("ok"):
                    break
                if self.locateToClick("close"):
                    break
                time.sleep(random.gauss(mu=1, sigma=.001))

            # self.check_quest()
            # os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    controller = GController()

    with Listener(on_press=controller.on_key_press) as listener:
        listener.join()
