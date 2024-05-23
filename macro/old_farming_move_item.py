import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import time
import base64


class GController(object):
  def __init__(self):
    self.kb = KbController()
    self.mouse = MouseController()
    self.window = None

    pag.FAILSAFE = True


  def mouse_l_click(self, x, y):
    pag.moveTo(x,y)
    self.mouse.press(Button.left)
    time.sleep(.3)
    self.mouse.release(Button.left)
    time.sleep(.5)


  def mouse_r_click(self):
    self.mouse.press(Button.right)
    time.sleep(.3)
    self.mouse.release(Button.right)
    time.sleep(.5)

  def pressAndRelease(self, key):
    self.kb.press(key)
    time.sleep(.3)
    self.kb.release(key)
    time.sleep(.3)


  def on_key_press(self, event):
    if event == Key.f11:
      print("> You pressed F11. Exiting gracefully.")
      raise KeyboardInterrupt
    elif event == KeyCode.from_char('a'):
      time.sleep(1)

      windows = []
      title = base64.b64decode("R2Vyc2FuZw==").decode("utf-8")
      temp = gw.getWindowsWithTitle(title)
      for w in temp:
        if w.title == title:
          windows.append(w)
      del temp

      for i, _ in enumerate(windows):
        w = windows[len(windows)-1-i]

        time.sleep(.5)
        w.minimize()
        w.restore()
        # w.activate()
        w.moveTo(60 +30*i, 10)
        print(w)
        time.sleep(.8)

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

  with Listener(on_press=controller.on_key_press) as listener:
    listener.join()
