import keyboard
import mouse
import time
import pygetwindow as gw

from pynput.keyboard import Key, Controller

# GLOBAL scope
kb = Controller()
monster = ["default"][0]
resv_attack_cnt = {
  "default": {
    2: 1,
    1: 1,
    5: 1,
    4: 1,
  },
}

def pressAndRelease(key):
  keyboard.press(key)
  time.sleep(.0183)
  keyboard.release(key)
  time.sleep(.0183)


def retreat():
  keyboard.press('esc')
  time.sleep(.1)
  keyboard.release('esc')
  time.sleep(.1)
  keyboard.press('esc')
  time.sleep(.1)
  keyboard.release('esc')



def debuf():
  pressAndRelease('w')
  time.sleep(.01)


# pyautogui의 keyboard press는 막힘
def on_key_press(event):

  # a: ,
  # d: /
  # w: ;
  # s: .
  # q: [
  # e: ]
  # c: \
  # x: '
  # if event.name == 'a':
  if event.name == ',':
    kb.press(Key.left)
    # time.sleep(.72)
    time.sleep(.55)
    kb.release(Key.left)
  # elif event.name == 'd':
  elif event.name == '/':
    kb.press(Key.right)
    time.sleep(.55)
    kb.release(Key.right)
  # elif event.name == 'w':
  elif event.name == ';':
    kb.press(Key.up)
    time.sleep(.55)
    kb.release(Key.up)
  # elif event.name == 's':
  elif event.name == '.':
    kb.press(Key.down)
    time.sleep(.55)
    kb.release(Key.down)

  # debuf & move
  # elif event.name == 'q':
  elif event.name == '[':
    # pressAndRelease('9')
    # pressAndRelease('h')

    pressAndRelease('2')
    mouse.press(button='right')
    time.sleep(.015)
    mouse.release(button='right')
    time.sleep(.01)
    # q 디버프
    pressAndRelease('q')
    time.sleep(.05)
    debuf()

    pressAndRelease('`')
    mouse.press(button='right')
    time.sleep(.015)
    mouse.release(button='right')
    time.sleep(.01)
    pressAndRelease('=')

  # 보호
  # elif event.name == 'e':
  elif event.name == ']':
    pressAndRelease('8')
    pressAndRelease('r')
    pressAndRelease('9')
    pressAndRelease('r')

  # TODO: 연속 on+ 1re 2re e
  # elif event.name == 'c':
  elif event.name == '\\':
    for k, v in resv_attack_cnt[monster].items():
      pressAndRelease(f"{k}")
      pressAndRelease('r')
      # print(f"r pressed")
      for _ in range(v):
        pressAndRelease('e')
      time.sleep(0.01)

  # elif event.name == 'x':
  elif event.name == '\'':
    retreat()


if __name__ == "__main__":
  keyboard.on_press(on_key_press)
  keyboard.wait('ctrl+c')
