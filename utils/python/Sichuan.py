
# coding: utf-8

# In[3]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import copy

class Sichuan:
    class node:
        def __init__(self, img):
            self.img = img
            self.num =-1
            
    def _mse(self, imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err
    
    def _Relative_error(self,a, b):
        return abs(a-b) * 100 / a

    def getSichuanArray(self,img):
        img = ~img
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Gray imgae
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0) # GaussianBlur image
        
        ret, img_th = cv2.threshold(img_blur, 70,255, cv2.THRESH_BINARY_INV)
        
        # image, contours, hierachy= cv2.findContours(img_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours, hierachy= cv2.findContours(img_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = [cv2.boundingRect(each) for each in contours]
        rects = [(x,y,w,h) for (x,y,w,h) in rects if ((w*h>500)and(w*h<600))]
        rects.sort()
        
        start = rects[1][0]
        nodeRaw = 0    
        for rect in rects:
            if(self._Relative_error(start,rect[0]) < 3):
                nodeRaw = nodeRaw + 1
        nodeNum = len(rects);
        nodeColum = int(nodeNum / nodeRaw)
        
        img_arr = []
        for rect in rects:
            newimg = img[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
            img_arr.append(self.node(img=newimg))
        count = 0    
        for subimg_i in img_arr:
            if(subimg_i.num == -1):
                subimg_i.num = count
                count = count + 1
                for subimg_j in img_arr:
                    if(self._mse(subimg_i.img,subimg_j.img)<1000):
                        subimg_j.num = subimg_i.num
                
        Matrix = [['*']*(nodeColum + 2) for i in range(nodeRaw+2)]
        for j in range(nodeColum ):
            for i in range(nodeRaw ):
                Matrix[i+1][j+1] = chr(img_arr[j*nodeRaw+i].num+65)

        for subimg_i in Matrix:
            print(subimg_i)
        return Matrix


    def _checkContent(self,target_xy,next_x,next_y,direction,trun_num, matrix, order, orderNum):
        if (trun_num >2):
            return orderNum
        else:
            if((0 <= next_x and next_x < len(matrix)) and (0 <= next_y and next_y < len(matrix[0]))):
                if(direction == 0):  # 처음
                    new_orderNum = self._checkContent(target_xy, next_x, next_y + 1, 1, trun_num, matrix, order, orderNum)
                    if(new_orderNum != orderNum):
                        return new_orderNum
                    new_orderNum = self._checkContent(target_xy, next_x, next_y - 1, 2, trun_num, matrix, order, orderNum) 
                    if(new_orderNum != orderNum):
                        return new_orderNum
                    new_orderNum = self._checkContent(target_xy, next_x + 1, next_y, 3, trun_num, matrix, order, orderNum)
                    if(new_orderNum != orderNum):
                        return new_orderNum
                    new_orderNum = self._checkContent(target_xy, next_x - 1, next_y, 4, trun_num, matrix, order, orderNum)
                    if(new_orderNum != orderNum):
                        return new_orderNum
                    return orderNum

                elif(direction == 1):
                    if(matrix[next_x][next_y] == '*'):
                        new_orderNum = self._checkContent(target_xy, next_x, next_y + 1, 1, trun_num, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        new_orderNum = self._checkContent(target_xy, next_x + 1, next_y, 3, trun_num + 1, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        new_orderNum = self._checkContent(target_xy, next_x - 1, next_y, 4, trun_num + 1, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        return orderNum
                    elif(matrix[target_xy[0]][target_xy[1]] == matrix[next_x][next_y]):
                        order[target_xy[0]][target_xy[1]] = orderNum
                        order[next_x][next_y] = orderNum + 1
                        matrix[target_xy[0]][target_xy[1]] = '*'
                        matrix[next_x][next_y] = '*'
                        return orderNum + 2
                    else:
                        return orderNum 

                elif(direction == 2):
                    if(matrix[next_x][next_y] == '*'):
                        new_orderNum = self._checkContent(target_xy, next_x, next_y - 1, 2, trun_num, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        new_orderNum = self._checkContent(target_xy, next_x + 1, next_y, 3, trun_num + 1, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        new_orderNum = self._checkContent(target_xy, next_x - 1, next_y, 4, trun_num + 1, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        return orderNum
                    elif(matrix[target_xy[0]][target_xy[1]] == matrix[next_x][next_y]):
                        order[target_xy[0]][target_xy[1]] = orderNum
                        order[next_x][next_y] = orderNum + 1
                        matrix[target_xy[0]][target_xy[1]] = '*'
                        matrix[next_x][next_y] = '*'
                        return orderNum + 2
                    else:
                        return orderNum 

                elif(direction == 3):
                    if(matrix[next_x][next_y] == '*'):
                        new_orderNum = self._checkContent(target_xy, next_x, next_y + 1, 1, trun_num + 1, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        new_orderNum = self._checkContent(target_xy, next_x, next_y - 1, 2, trun_num + 1, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        new_orderNum = self._checkContent(target_xy, next_x + 1, next_y, 3, trun_num, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        return orderNum
                    elif(matrix[target_xy[0]][target_xy[1]] == matrix[next_x][next_y]):
                        order[target_xy[0]][target_xy[1]] = orderNum
                        order[next_x][next_y] = orderNum + 1
                        matrix[target_xy[0]][target_xy[1]] = '*'
                        matrix[next_x][next_y] = '*'
                        return orderNum + 2
                    else:
                        return orderNum 

                elif(direction == 4):
                    if(matrix[next_x][next_y] == '*'):
                        new_orderNum = self._checkContent(target_xy, next_x, next_y + 1, 1, trun_num + 1, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        new_orderNum = self._checkContent(target_xy, next_x, next_y - 1, 2, trun_num + 1, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        new_orderNum = self._checkContent(target_xy, next_x - 1, next_y, 4, trun_num, matrix, order, orderNum)
                        if(new_orderNum != orderNum):
                            return new_orderNum
                        return orderNum
                    elif(matrix[target_xy[0]][target_xy[1]] == matrix[next_x][next_y]):
                        order[target_xy[0]][target_xy[1]] = orderNum
                        order[next_x][next_y] = orderNum + 1
                        matrix[target_xy[0]][target_xy[1]] = '*'
                        matrix[next_x][next_y] = '*'
                        return orderNum + 2

                    else:
                        return orderNum 
            else:
                return orderNum

    def _checkLoop(self,start_x,start_y,matrix,order,num):
        new_num = num
        target_num = (len(matrix[0])-2)*(len(matrix)-2)
        for i in (list(range(start_x,len(matrix))) + list(range(0,start_x))):
            for j in (list(range(start_y,len(matrix[0]))) + list(range(0,start_y))) :		
                if(matrix[i][j] == '*'):
                    continue
                else:
                    new_num = self._checkContent((i,j),i,j,0,0,matrix,order,new_num)
                    if(new_num-1 == (target_num)):
                        break
            if(new_num-1 == (target_num)):
                break

        while(True):
            if(new_num != num):
                if(new_num-1 == (target_num)):
                    return new_num
                else:
                    num = new_num
                    new_num = self._checkLoop(start_x,start_y,matrix,order,new_num)
            else:
                return new_num


    def getSichuanOrder(self,matrix):
        result = None
        targetNum = (len(matrix[0])-2)*(len(matrix)-2)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                order = [[0] * len(matrix[0]) for i in range(len(matrix))]
                copyMetrix = copy.deepcopy(matrix)
                result = self._checkLoop(i,j,copyMetrix,order,1)
                if( result== targetNum):
                    break;
            if( result== targetNum):
                    break;
        return order


# In[10]:


# s = Sichuan()
# img = cv2.imread("./utils/images/img_sichuan/03.png")
# img = img[241:578, 288:737]  

# Array = s.getSichuanArray(img)
# Array


# # In[11]:


# order = s.getSichuanOrder(Array)
# order

