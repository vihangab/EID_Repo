#!/usr/bin/env python

# OpenCV Python program to detect cars in video frame
# import libraries of python OpenCV

import sys
sys.path.append('/usr/local/lib/python3.4/site-packages')
import cv2
Count = 0
# capture frames from a video
cap = cv2.VideoCapture('video.avi')
#cv2.SetCaptureProperty(cap, 5, 30)
#cap.set(1,Count)
#getfps = cap.get(1)
#print(getfps)
 
# Trained XML classifiers describes some features of some object we want to detect
car_cascade = cv2.CascadeClassifier('cars.xml')
 
# loop runs if capturing has been initialized.
while True:
    # reads frames from a video
    ret, frames = cap.read()

    #getfps = cap.get(1)
    #print(getfps)
    
    # convert to gray scale of each frames
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
     
 
    # Detects cars of different sizes in the input image
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

     
    # To draw a rectangle in each cars
    for (x,y,w,h) in cars:
        cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)

    print("Vehicle count= "+str(len(cars)))
    
    # Display frames in a window 
    cv2.imshow('video2', frames)

    #Count += 5

    #cap.set(1,Count)
     
    # Wait for Esc key to stop
    if cv2.waitKey(33) == 27:
        break
 
# De-allocate any associated memory usage
cv2.destroyAllWindows()
