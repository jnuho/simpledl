import time
import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import signal
import os


class GController(object):
    def __init__(self, failsafe=False):
        self.kb = KbController()
        self.mouse = MouseController()
        self.window = None
        self.conv_cnt = 7

        pag.FAILSAFE = failsafe




    def pressAndRelease(self, key):
        self.kb.press(key)
        time.sleep(.01)
        self.kb.release(key)
        time.sleep(.01)


    def mouse_l_click(self, x, y):
        pag.moveTo(x,y)
        self.mouse.press(Button.left)
        time.sleep(.08)
        self.mouse.release(Button.left)
        time.sleep(.1)


    def locateToClick(self, keyword):
        # for _ in range(self.conv_cnt):
        try:
            accept = pag.locateCenterOnScreen("util/images/" + keyword + ".png", confidence=.93, grayscale=True)
            self.mouse_l_click(accept.x, accept.y)
            pag.move(100,100)
            return True
        except pag.ImageNotFoundException:
            print("`" + keyword + "`" + "NOT FOUND")
            return False

    def check_quest(self):
        self.pressAndRelease('q')
        time.sleep(1)
        self.locateToClick("check_quest")
        time.sleep(.5)
        self.pressAndRelease('q')

    def on_key_press(self, event):
        if event == Key.f11:
            print("> You pressed F11. Exiting gracefully.")
            raise KeyboardInterrupt
        elif event == KeyCode.from_char('\\'):

            self.window = gw.getActiveWindow()
            # self.kb.press(Key.left)
            # # time.sleep(.72)
            # time.sleep(.55)
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
                time.sleep(1)

            # self.check_quest()
            # os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    controller = GController()

    with Listener(on_press=controller.on_key_press) as listener:
        listener.join()
