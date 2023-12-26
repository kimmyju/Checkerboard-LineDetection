import numpy as np
import cv2
import math
import copy

src = cv2.imread('go2.jpg',1)
if src is None:
    print('Image load failed!')
    exit()

cv2.imshow('src', src)
cv2.waitKey(0)

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
hough_circle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 10, param1=150, param2=30, minRadius=0, maxRadius=40)

#dst = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
for i in hough_circle[0]:
    cv2.circle(src, (int(i[0]), int(i[1])),int(i[2])+1, (0,0,255),1) #원래두께는 1
   

cv2.imshow('circle', src)
cv2.waitKey(0)


gray2 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray2, 100, 150)# 198, 230)50,200,150
cv2.imshow('edge', edge)
cv2.waitKey(0)

for i in hough_circle[0]:
    cv2.circle(edge, (int(i[0]), int(i[1])), 1, 255, 4)
cv2.imshow('edge', edge)
cv2.waitKey(0)

lines = cv2.HoughLines(edge, 1, (math.pi / 180),160)
#dst2 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


if lines is not None:
    for i in range(lines.shape[0]):
        rho = lines[i][0][0] #rho
        theta = lines[i][0][1] #theta
        
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        x0, y0 = rho * cos_t, rho * sin_t
        alpha = 1500
        pt1 = (int(x0 - alpha * sin_t), int(y0 + alpha * cos_t))
        pt2 = (int(x0 + alpha * sin_t), int(y0 - alpha * cos_t))

        print(theta*180/math.pi)
        if theta*180/math.pi >= 89.5 and theta*180/math.pi <=90.5: #수평
            cv2.line(src, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)
        elif theta*180/math.pi <=0.5:  #9                       #수직
            cv2.line(src, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)
       

cv2.imshow('result', src)
cv2.waitKey(0)
cv2.imwrite("second_sub/hough_go2.jpg", src)
cv2.destroyAllWindows()