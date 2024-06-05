
from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import time
import random

class GController(object):
    def __init__(self, monster_type=0):
        self.kb = KbController()
        self.mouse = MouseController()

        self.monster = ["def"][monster_type]
        self.resv_attack_cnt = {
            "def": {
                8: 0,
                2: 1,
                1: 0,
                4: 0,
                5: 1,
            },
        }

    def pressAndRelease(self, key):
        # mu : mean
        # sigma : standard deviation, assuming a 6-sigma range for 99.7% coverage
        self.kb.press(key)
        time.sleep(random.gauss(mu=.01835, sigma=.0001/6))
        self.kb.release(key)
        time.sleep(random.gauss(mu=.01835, sigma=.0001/6))


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
            self.pressAndRelease('2')
            self.mouse.press(Button.right)
            time.sleep(random.gauss(mu=.015, sigma=.0001))
            self.mouse.release(Button.right)
            time.sleep(random.gauss(mu=.015, sigma=.0001))
            # q 디버프
            self.pressAndRelease('q')
            self.pressAndRelease('w')

            self.pressAndRelease('`')
            self.mouse.press(Button.right)
            time.sleep(random.gauss(mu=.015, sigma=.0001))
            self.mouse.release(Button.right)
            time.sleep(random.gauss(mu=.015, sigma=.0001))
            self.pressAndRelease('=')

        # 보호
        # elif event.name == 'e':
        elif event == KeyCode.from_char(']'):
            self.pressAndRelease('9')
            self.pressAndRelease('r')

        # elif event.name == 'c':
        elif event == KeyCode.from_char('\\'):
            for k, v in self.resv_attack_cnt[self.monster].items():
                self.pressAndRelease(f"{k}")
                self.pressAndRelease('r')
                for _ in range(v):
                    self.pressAndRelease('e')
                time.sleep(random.gauss(mu=.01, sigma=.0001))

        # elif event.name == 'x':
        elif event == KeyCode.from_char('\''):
            self.retreat()


if __name__ == "__main__":
    controller = GController()

    with Listener(on_press=controller.on_key_press) as listener:
        listener.join()

