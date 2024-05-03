import keyboard
import psutil
import time
import os
import pyautogui as pag
import pygetwindow as gw
from pywinauto import Application

from pynput.keyboard import Key, Controller


kb = Controller()
window = None


def kill_gitbash():
  # focus on window
  # windows = gw.getWindowsWithTitle('MINGW64:/c/Users/user/Repos')
  windows = gw.getWindowsWithTitle('MINGW64')

  for _, w in enumerate(windows):
    # Connect to the application using pywinauto and get the process ID
    app = Application().connect(handle=w._hWnd)
    pid = app.process
    
    # Kill the process
    os.system(f'taskkill /PID {pid} /F')


def run_gitbash():
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


def kill_ahk():
  PROCNAME = "AutoHotkey.exe"
  for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
      proc.kill()


def run_ahk():
  path = 'C:\\Users\\user\\Downloads\\etc\\esc_win11.ahk'
  os.system('start "" "' + path+ '"')
  time.sleep(.5)


def split_panes():
  # 0: LAPTOP, 1: MONITOR
  loc = 0

  if loc == 0:
    pag.write("tmux new-session \\; split-window -v \\; attach")
  elif loc ==1:
    # pag.write("tmux new-session \\; split-window -h \\; select-pane -L \\; split-window -v \\; select-pane -U \\; split-window -v \\; select-pane -R \\; split-window -v \\; ")
    pag.write("tmux new-session \\; split-window -h \\; select-pane -L \\; split-window -v \\; select-pane -R \\; split-window -v \\; attach")
    # Move back to the upper left pane
    # pag.write("select-pane -L \\; select-pane -U \\; attach")

  time.sleep(.2)
  keyboard.press("enter")
  time.sleep(.1)
  keyboard.release("enter")
  exit(0)


if __name__ == "__main__":

  kill_ahk()
  run_ahk()

  # kill_gitbash()
  # run_gitbash()
  # time.sleep(3)
  # split_panes()
