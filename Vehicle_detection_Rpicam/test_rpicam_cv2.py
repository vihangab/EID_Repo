#!/usr/bin/env python

# OpenCV Python program to detect cars in video frame
# import libraries of python OpenCV

import sys
sys.path.append('/usr/local/lib/python3.4/site-packages')
import cv2

from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(3)
camera.capture('/home/pi/Desktop/Vehicle_detection_Rpicam/image.jpg')

#Get the image in grayscale
cap = cv2.imread('test4.jpg',0)

#cv2.imshow('image',cap)
car_cascade = cv2.CascadeClassifier('cars.xml')

#ret, frames = cap.read()
    
# convert to gray scale of each frames
#gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
     
 
# Detects cars of different sizes in the input image
cars = car_cascade.detectMultiScale(cap, 1.1, 1)

     
# To draw a rectangle in each cars
for (x,y,w,h) in cars:
    cv2.rectangle(cap,(x,y),(x+w,y+h),(0,0,255),2)

print("Vehicle count= "+str(len(cars)))

#imshow(Windowname,image)
cv2.imshow('Image Preview',cap)

cv2.waitKey(0)

cv2.destroyAllWindows()

camera.stop_preview()

