
# coding: utf-8

# In[16]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

img = cv2.imread("./images/img_sichuan/02.png")
plt.figure(figsize=(7,7))
plt.imshow(img);


# In[17]:


img = img[241:578, 288:737]  
img = ~img
plt.figure(figsize=(7,7))
plt.imshow(img);


# In[18]:


img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Gray imgae
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0) # GaussianBlur image
plt.figure(figsize=(7,7))
plt.imshow(img_gray)


# In[19]:


# cv2.threshold(img, threshold_value, value, flag)
# img: Grayscale 이미지
# threshold_value: 픽셀 문턱값
# value: 픽셀 문턱값보다 클 때 적용되는 최대값(적용되는 플래그에 따라 픽셀 문턱값보다 작을 때 적용되는 최대값)
# flag: 문턱값 적용 방법 또는 스타일

ret, img_th = cv2.threshold(img_blur, 70,255, cv2.THRESH_BINARY_INV)
plt.figure(figsize=(7,7))
plt.imshow(img_th);


# In[20]:


image, contours, hierachy= cv2.findContours(img_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
rects = [cv2.boundingRect(each) for each in contours]
print(rects)


# In[21]:


rects = [(x,y,w,h) for (x,y,w,h) in rects if ((w*h>500)and(w*h<600))]
rects.sort()


# In[22]:


for rect in rects:
    # Draw the rectangles
    cv2.rectangle(img, (rect[0], rect[1]),(rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1) 
plt.figure(figsize=(7,7))
plt.imshow(img)


# In[23]:


def Relative_error(a, b):
    return abs(a-b) * 100 / a

start = rects[1][0]
nodeRaw = 0    
for rect in rects:
    if(Relative_error(start,rect[0]) < 3):
        nodeRaw = nodeRaw + 1
nodeNum = len(rects);
nodeColum = int(nodeNum / nodeRaw)
print("%d = %d * %d" % (nodeNum, nodeRaw,nodeColum))

class node:
    def __init__(self, img):
        self.img = img
        self.num =-1
        
img_arr = []
for rect in rects:
    newimg = img[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
    img_arr.append(node(img=newimg))


# In[24]:


def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

count=0
for subimg_i in img_arr:
    if(subimg_i.num == -1):
        subimg_i.num = count
        count = count + 1
        for subimg_j in img_arr:
            if(mse(subimg_i.img,subimg_j.img)<1000):
                subimg_j.num = subimg_i.num
                
Matrix = [['*']*(nodeColum + 2) for i in range(nodeRaw+2)]
for j in range(nodeColum ):
    for i in range(nodeRaw ):
        Matrix[i+1][j+1] = chr(img_arr[j*nodeRaw+i].num+65)

for subimg_i in Matrix:
    print(subimg_i)

