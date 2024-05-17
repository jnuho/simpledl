import keyboard
import time
import mouse
import pyautogui as pag
import pygetwindow as gw
from pynput.keyboard import Controller

import signal
import os


kb = Controller()

window = None
npc = ["bok", "yim", "seorae", "baekmin", "jakup", "baekjun"][0]
quest_idx = 0
conv_cnt = {
  "bok": {
    0: 4, # 10 dogs
    1: 3, # food 4000
    2: 3, # enlist 3
  },
  "yim": {
    0: 4, # dunsan
  },
  "seorae": {
  },
  "baekmin": {
  },
  "jakup": {
  },
  "baekjun": {
  },
}[npc][quest_idx]


def init():
  global window
  pag.FAILSAFE = False

  w = gw.getActiveWindow()
  window = w
  print("INIT DONE")

def pressAndRelease(key):
  keyboard.press(key)
  time.sleep(.03)
  keyboard.release(key)
  time.sleep(.03)

def mouse_l_click(x, y):
  pag.moveTo(x,y)
  mouse.press(button='left')
  time.sleep(.3)
  mouse.release(button='left')
  time.sleep(.5)

def locateToClick(keyword):
  for _ in range(conv_cnt):
    try:
      accept = pag.locateCenterOnScreen("macro/images/" + keyword + ".png", confidence=.93, grayscale=True)
      mouse_l_click(accept.x, accept.y)
      pag.moveTo(0,0)
      return True
    except pag.ImageNotFoundException:
      print("`" + keyword + "`" + "NOT FOUND")
      return False

def on_key_press(event):
  # global window
  global npc
  global conv_cnt

  # elif event.name == 'c':
  if event.name == '\\':
    # file = round(datetime.now().timestamp())
    # pag.screenshot(f'macro/images/s_{file}.png', region=(window.left, window.top, window.width, window.height))
    for _ in range(conv_cnt):
      if locateToClick("accept"):
        continue

      if locateToClick("next"):
        continue

      if locateToClick("ok"):
        continue

      time.sleep(1)

    pressAndRelease('q')
    time.sleep(1)
    locateToClick("check_quest")
    time.sleep(1)
    pressAndRelease('q')
    os.kill(os.getpid(), signal.SIGINT)



if __name__ == "__main__":
  time.sleep(2)
  init()

  keyboard.on_press(on_key_press)
  keyboard.wait('ctrl+c')

