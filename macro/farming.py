import datetime
import time

import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController


class GController:
  def __init__(self):
    self.kb = KbController()
    self.mouse = MouseController()
    self.window = None

  def init(self):
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
      while True:
        time.sleep(1)
        print(datetime.datetime.now())

        windows = []
        temp = gw.getWindowsWithTitle('Gersang')
        for w in temp:
          if w.title == 'Gersang':
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

          self.mouse_l_click(w.left + (w.width*.2049), w.top + (w.height*.4341))
          self.pressAndRelease(Key.enter)
          self.pressAndRelease(Key.esc)
          self.pressAndRelease('i')

          # Food
          pag.moveTo(w.left + (w.width*.5835), w.top + (w.height*.2484))
          time.sleep(.3)

          self.mouse_r_click()
          self.mouse_r_click()
          self.mouse_r_click()
          self.mouse_r_click()

          time.sleep(.3)
          self.pressAndRelease('j')
          time.sleep(.3)
          self.mouse_l_click(w.left + (w.width*.2049), w.top + (w.height*.4341))
          time.sleep(.3)
          self.pressAndRelease('j')

        time.sleep(25*60)


if __name__ == "__main__":
  controller = GController()
  controller.init()

  with Listener(on_press=controller.on_key_press) as listener:
    listener.join()
