import pyautogui as pag
import pygetwindow as gw

from pynput.keyboard import KeyCode, Key, Listener
from pynput.keyboard import Controller as KbController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

import cv2
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime

from Sichuan import Sichuan as sc

class GController(object):
    def __init__(self):
        self.kb = KbController()
        self.mouse = MouseController()
        self.window = None

        pag.FAILSAFE = True

    def on_key_press(self, event):
        if event == Key.f11:
            print("> You pressed F11. Exiting gracefully.")
            raise KeyboardInterrupt
        elif event == KeyCode.from_char('\\'):
            # Get Active Window
            w = gw.getActiveWindow()

            # Save as an image
            file = round(datetime.now().timestamp())
            path = 'utils/images/s_{}.png'.format(file)
            """
            #region = (w.left + round(w.width*291/1030), w.top + round(w.height*243/797),
            #           round(w.width*448/1030), round(w.height*335/797))
            """
            region = (w.left, w.top, w.width, w.height)
            pag.screenshot(f'{path}', region=region)

            # img = self.process_image(path)
            # print(img)

            s = sc()
            img = cv2.imread(path)
            Array = s.getSichuanArray(img)
            # order = s.getSichuanOrder(Array)
            # print(order)

    def process_image(self, path):
        img = cv2.imread(path)

        # invert
        img = ~img

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Gray imgae
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0) # GaussianBlur image

        # cv2.threshold(img, threshold_value, value, flag)
        # img: Grayscale 이미지
        # threshold_value: 픽셀 문턱값
        # value: 픽셀 문턱값보다 클 때 적용되는 최대값(적용되는 플래그에 따라 픽셀 문턱값보다 작을 때 적용되는 최대값)
        # flag: 문턱값 적용 방법 또는 스타일
        ret, img_th = cv2.threshold(img_blur, 70,255, cv2.THRESH_BINARY_INV)

        # 남은 픽셀들의 집합에 사각형 입히기
        contours, hierachy= cv2.findContours(img_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = [cv2.boundingRect(each) for each in contours]
        # print(rects)
        for rect in rects:
            # Draw the rectangles
            cv2.rectangle(img, (rect[0], rect[1]),(rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1) 
        plt.figure(figsize=(7,7))
        plt.imshow(img)

        output_path = 'utils/images/test.png'
        cv2.imwrite(output_path, img_th)

        return img_th



if __name__ == "__main__":
    controller = GController()

    with Listener(on_press=controller.on_key_press) as listener:
        listener.join()
