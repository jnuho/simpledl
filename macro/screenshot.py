import keyboard
import time
import mouse
from datetime import datetime
import pyautogui as pag
import pygetwindow as gw
from pynput.keyboard import Key, Controller
kb = Controller()

window = None

def init():
    pag.FAILSAFE = False
    global window
    
    w = gw.getActiveWindow()
    window = w
    print("INIT DONE")

def on_key_press(event):
    global window
    global npc
    global conv_cnt

    # elif event.name == 'c':
    if event.name == '\\':
        file = round(datetime.now().timestamp())
        pag.screenshot(f'macro/images/s_{file}.png', region=(window.left, window.top, window.width, window.height))


if __name__ == "__main__":
    time.sleep(3)
    init()

    keyboard.on_press(on_key_press)
    keyboard.wait('ctrl+c')

