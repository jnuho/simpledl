import time
import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import signal
import os


class GController:
  def __init__(self):
    self.kb = KbController()
    self.mouse = MouseController()
    self.window = None
    self.npc = ["bok", "yim", "seorae", "baekmin", "jakup", "baekjun", "hun"][6]
    self.quest_idx = 0
    self.conv_cnt = {
      "bok": {
        0: 4, # 10 dogs
        1: 3, # food 4000
        2: 3, # enlist 3
      },
      "yim": {
        0: 4, # dunsan
      },
      "seorae": {
        0: 4,
      },
      "baekmin": {
        0: 3, # millim
        1: 2, # rest of all
      },
      "jakup": {
        0: 2,
        1: 3, # rest of all
      },
      "baekjun": {
        0: 3,
        1: 2, # rest of all
      },
      "hun": {
        0: 2, # rest of all
      },
    }[self.npc][self.quest_idx]


  def init(self):
    pag.FAILSAFE = False
    self.window = gw.getActiveWindow()
    print("INIT DONE")

  def pressAndRelease(self, key):
    self.kb.press(key)
    time.sleep(.03)
    self.kb.release(key)
    time.sleep(.03)

  def mouse_l_click(self, x, y):
    pag.moveTo(x,y)
    self.mouse.press(Button.left)
    time.sleep(.3)
    self.mouse.release(Button.left)
    time.sleep(.5)

  def locateToClick(self, keyword):
    for _ in range(self.conv_cnt):
      try:
        accept = pag.locateCenterOnScreen("macro/images/" + keyword + ".png", confidence=.93, grayscale=True)
        self.mouse_l_click(accept.x, accept.y)
        pag.move(100,100)
        return True
      except pag.ImageNotFoundException:
        print("`" + keyword + "`" + "NOT FOUND")
        return False

  def on_key_press(self, event):
    if event == Key.f11:
      print("> You pressed F11. Exiting gracefully.")
      raise KeyboardInterrupt
    elif event == KeyCode.from_char('\\'):
      self.kb.press(Key.left)
      # time.sleep(.72)
      time.sleep(.55)
      self.kb.release(Key.left)
      # file = round(datetime.now().timestamp())
      # pag.screenshot(f'macro/images/s_{file}.png', region=(window.left, window.top, window.width, window.height))
      # for _ in range(self.conv_cnt):
      for _ in range(self.conv_cnt):
        if self.locateToClick("list_seorae"):
          continue
        if self.locateToClick("accept"):
          continue
        if self.locateToClick("next"):
          continue
        if self.locateToClick("ok"):
          continue

        time.sleep(1)

      self.pressAndRelease('q')
      time.sleep(1)
      self.locateToClick("check_quest")
      time.sleep(.5)
      self.pressAndRelease('q')
      os.kill(os.getpid(), signal.SIGINT)



if __name__ == "__main__":
  controller = GController()
  controller.init()

  with Listener(on_press=controller.on_key_press) as listener:
    listener.join()
