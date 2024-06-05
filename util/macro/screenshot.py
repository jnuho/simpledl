import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

from datetime import datetime


class GController(object):
    def __init__(self, failsafe=False):
        self.kb = KbController()
        self.mouse = MouseController()
        self.window = None

        pag.FAILSAFE = failsafe

    def on_key_press(self, event):
        if event == Key.f11:
            print("> You pressed F11. Exiting gracefully.")
            raise KeyboardInterrupt
        elif event == KeyCode.from_char('\\'):
            w = gw.getActiveWindow()

            file = round(datetime.now().timestamp())
            path = 'util/images/s_{}.png'.format(file)

            region = (w.left, w.top, w.width, w.height)
            pag.screenshot(f'{path}', region=region)


if __name__ == "__main__":
    controller = GController()

    with Listener(on_press=controller.on_key_press) as listener:
        listener.join()
