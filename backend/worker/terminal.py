import keyboard
import mouse
import time
import os
import pyautogui as pag
import pygetwindow as gw
from pywinauto import Application
import subprocess

from pynput.keyboard import Key, Controller


kb = Controller()
window = None

# a =pag.position()
# pag.screenshot('python_work/1.png', region=(400,100, 1200, 1000))
# button7location = pag.locateCenterOnScreen('python_work/1.png', confidence=0.9, grayscale=True)
# print(button7location)


def kill_all():
  # focus on window
  # windows = gw.getWindowsWithTitle('MINGW64:/c/Users/user/Repos')
  windows = gw.getWindowsWithTitle('MINGW64')

  for _, w in enumerate(windows):
    # Connect to the application using pywinauto and get the process ID
    app = Application().connect(handle=w._hWnd)
    pid = app.process
    
    # Kill the process
    os.system(f'taskkill /PID {pid} /F')



def open_terminal():
  path = 'C:\\Program Files\\Git\\git-bash.exe'
  os.system('start "" "' + path+ '"')
  time.sleep(1.5)

  window = gw.getWindowsWithTitle('MINGW64')[0]
  window.maximize()
  window.activate()
  pag.write("tmux kill-server")
  time.sleep(.1)
  keyboard.press("enter")
  time.sleep(.1)
  keyboard.release("enter")


def split_panes():
  pag.write("tmux new-session \\; ")
  pag.write("split-window -h \\; ")
  pag.write("select-pane -L \\; ")
  pag.write("split-window -v \\; ")
  pag.write("select-pane -U \\; ")
  pag.write("split-window -v \\; ")
  pag.write("select-pane -R \\; ")
  pag.write("split-window -v \\; ")
  # pag.write("select-layout tiled \; ")
  # Move back to the upper left pane
  pag.write("select-pane -L \\; ")
  pag.write("select-pane -U \\; ")
  pag.write("select-pane -U \\; ")
  pag.write("attach")

  time.sleep(.1)
  keyboard.press("enter")
  time.sleep(.1)
  keyboard.release("enter")

  exit(0)


if __name__ == "__main__":
  kill_all()

  open_terminal()

  time.sleep(3)

  split_panes()