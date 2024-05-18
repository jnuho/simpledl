import mouse
import time
import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Controller, Listener


class GController:
  def __init__(self):
    self.kb = Controller()
    self.window = None
    self.monster = ["dosa", "3c","gotang"][0]
    self.resv_attack_cnt = {
      "dosa": {
        8: 0,
        2: 2,
        1: 0,
        4: 1,
        5: 1,
        # 6: 0,
      },
      "3c": {
        2: 0,
        1: 0,
        4: 0,
      },
      "gotang": {
        8: 0,
        2: 1,
        1: 0,
        4: 0,
        # 6: 0,
      },
    }


  def get_food(self):
    try:
      pos_found = pag.locateCenterOnScreen("macro/images/food" + str(1) + ".png", confidence=.93, grayscale=True)
      # 150 바 = 687-537
      # 248: 100%    # -310 일때 길이: 225
      x_diff = pos_found.x - self.window.left
      if x_diff < 224:
        self.kb.press(Key.alt)
        time.sleep(.05)
        for i in range(2):
          self.kb.press('2')
          time.sleep(.2)
          self.kb.release('2')
          time.sleep(.2)
        self.kb.release(Key.alt)
    except pag.ImageNotFoundException:
      print("NOT FOUND")


  def init(self):
    pag.FAILSAFE = True
    windows = gw.getWindowsWithTitle('Gersang')
    for w in windows:
      if w.title != 'Gersang':
        continue
      # w.activate()
      self.window = w


  def pressAndRelease(self, key):
    self.kb.press(key)
    time.sleep(.0183)
    self.kb.release(key)
    time.sleep(.0183)


  def retreat(self):
    self.kb.press(Key.esc)
    time.sleep(.1)
    self.kb.release(Key.esc)
    time.sleep(.1)
    self.kb.press(Key.esc)
    time.sleep(.1)
    self.kb.release(Key.esc)


  def debuf(self):
    self.pressAndRelease('w')
    time.sleep(.01)


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
    # if event.name == 'a':
    elif event == KeyCode.from_char(','):
      self.kb.press(Key.left)
      # time.sleep(.72)
      time.sleep(.55)
      self.kb.release(Key.left)
    # elif event.name == 'd':
    elif event == KeyCode.from_char('/'):
      self.kb.press(Key.right)
      time.sleep(.55)
      self.kb.release(Key.right)
    # elif event.name == 'w':
    elif event == KeyCode.from_char(';'):
      self.kb.press(Key.up)
      time.sleep(.55)
      self.kb.release(Key.up)
    # elif event.name == 's':
    elif event == KeyCode.from_char('.'):
      self.kb.press(Key.down)
      time.sleep(.55)
      self.kb.release(Key.down)

    # debuf & move
    # elif event.name == 'q':
    elif event == KeyCode.from_char('['):
      # pressAndRelease('9')
      # pressAndRelease('h')

      self.pressAndRelease('2')
      mouse.press(button='right')
      time.sleep(.015)
      mouse.release(button='right')
      time.sleep(.01)
      # q 디버프
      self.pressAndRelease('q')
      time.sleep(.05)
      self.debuf()

      self.pressAndRelease('`')
      mouse.press(button='right')
      time.sleep(.015)
      mouse.release(button='right')
      time.sleep(.01)
      self.pressAndRelease('=')

    # 보호
    # elif event.name == 'e':
    elif event == KeyCode.from_char(']'):
      self.pressAndRelease('8')
      self.pressAndRelease('r')
      self.pressAndRelease('9')
      self.pressAndRelease('r')

    # TODO: 연속 on+ 1re 2re e
    # elif event.name == 'c':
    elif event == KeyCode.from_char('\\'):
      for k, v in self.resv_attack_cnt[self.monster].items():
        self.pressAndRelease(f"{k}")
        self.pressAndRelease('r')
        # print(f"r pressed")
        for _ in range(v):
          self.pressAndRelease('e')
        time.sleep(0.01)

    # elif event.name == 'x':
    elif event == KeyCode.from_char('\''):
      self.retreat()

      time.sleep(1.65)
      self.get_food()


# https://superfastpython.com/asyncio-coroutines-faster-than-threads/#:~:text=A%20coroutine%20is%20just%20a,This%20should%20not%20be%20surprising.
# https://velog.io/@haero_kim/Thread-vs-Coroutine-%EB%B9%84%EA%B5%90%ED%95%B4%EB%B3%B4%EA%B8%B0
# https://stackoverflow.com/questions/1934715/difference-between-a-coroutine-and-a-thread
if __name__ == "__main__":
  controller = GController()
  controller.init()

  with Listener(on_press=controller.on_key_press) as listener:
    listener.join()

