import keyboard
import mouse
import time
import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import Key, Controller
kb = Controller()

def init():
  pag.FAILSAFE = False

def mouse_l_click(x, y):
  pag.moveTo(x,y)
  mouse.press(button='left')
  time.sleep(.3)
  mouse.release(button='left')
  time.sleep(.5)

def pressAndRelease(key):
    keyboard.press(key)
    time.sleep(.3)
    keyboard.release(key)
    time.sleep(.5)

# pyautogui의 keyboard press는 막힘
def on_key_press(event):
  if event.name == 'a':
    time.sleep(1)

    windows = gw.getWindowsWithTitle('Gersang')

    for w in windows:
      if w.title != 'Gersang':
        continue

      print(w)
      w.minimize()
      time.sleep(.5)
      w.restore()
      time.sleep(.5)
      # w.activate()
      # time.sleep(.5)

      # game_window.activate()
      mouse_l_click(w.left + (w.width*.2049), w.top + (w.height*.4341))
      pressAndRelease('enter')
      pressAndRelease('i')
      
      # MOVE ITEMS
      mouse_l_click(w.left + (w.width*.2029), w.top + (w.height*.5747))
      mouse_l_click(w.left + (w.width*.5796), w.top + (w.height*.6261))
      mouse_l_click(w.left + (w.width*.7068), w.top + (w.height*.729))
      pressAndRelease('enter')

      mouse_l_click(w.left + (w.width*.2417), w.top + (w.height*.5747))
      mouse_l_click(w.left + (w.width*.5796), w.top + (w.height*.6261))
      mouse_l_click(w.left + (w.width*.7068), w.top + (w.height*.729))
      pressAndRelease('enter')
      
      mouse_l_click(w.left + (w.width*.2845), w.top + (w.height*.5747))
      mouse_l_click(w.left + (w.width*.5796), w.top + (w.height*.6261))
      mouse_l_click(w.left + (w.width*.7068), w.top + (w.height*.729))
      pressAndRelease('enter')

      # 아이템 삭제
      pressAndRelease('j')
      
      mouse_l_click(w.left + (w.width*.8524), w.top + (w.height*.6826))
      mouse_l_click(w.left + (w.width*.668), w.top + (w.height*.2472))
      mouse_l_click(w.left + (w.width*.799), w.top + (w.height*.3476))
      pressAndRelease('enter')
      pressAndRelease('enter')

      mouse_l_click(w.left + (w.width*.7097), w.top + (w.height*.2472))
      mouse_l_click(w.left + (w.width*.8417), w.top + (w.height*.3425))
      pressAndRelease('enter')
      pressAndRelease('enter')

      #다시시작
      pressAndRelease('j')
      mouse_l_click(w.left + (w.width*.2049), w.top + (w.height*.4341))
      pressAndRelease('j')

if __name__ == "__main__":
  init()

  keyboard.on_press(on_key_press)
  # Keep the program running until you press the Esc key
  # keyboard.add_hotkey('ctrl+c', quit)
  # keyboard.wait(hotkey=None, suppress=False, trigger_on_release=False)
  keyboard.wait('ctrl+c')

