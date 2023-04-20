import cv2 as cv

import numpy as np
from time import gmtime, strftime, sleep, time
import logging
import nanocamera as nano
import sys
import math
import RPi.GPIO as GPIO

#red_led = 31
#green_led = 35
#blue_led = 33

GPIO.setmode(GPIO.BOARD)
#GPIO.setup(red_led, GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(green_led, GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(blue_led, GPIO.OUT, initial=GPIO.LOW)

# Create the Camera instance for 640 by 480
camera = nano.Camera()

if __name__=='__main__':

    print('Started')
    print ("Beginning Transmitting to channel: Happy_Robots")
    now = time()
    params = cv.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 100
    params.filterByColor = True
    params.blobColor = 0
    detector = cv.SimpleBlobDetector_create(params)
    
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    while True:
        try:
            #fetching each frame
            frame = camera.read()
            if frame is None:
                print("frame is none")
                break
            frame_width = frame.shape[1]
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            mask = cv.inRange(gray, 60, 255)
            red_mask = cv.inRange(hsvFrame, red_lower, red_upper)

            keypoints = detector.detect(frame)
            
            blank = np.zeros((1, 1))
            blobs = cv.drawKeypoints(frame, keypoints, blank, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            
            number_of_blobs = len(keypoints)
            text = "Number of Circular Blobs: " + str(len(keypoints))
            cv.putText(blobs, text, (20, 550), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
            if (len(keypoints) > 0): # if blob is seen
                x = keypoints[0].pt[0]
                if x < frame_width/3: #on left 1/3
                    print("Exists in left 1/3 of frame")
                    #GPIO.output(red_led, GPIO.HIGH)
                    #GPIO.output(green_led, GPIO.LOW)
                    #GPIO.output(blue_led, GPIO.LOW)

                elif x > (frame_width/3) * 2: #on right 1/3
                    print("Exists in right 1/3 of frame")
                    #GPIO.output(green_led, GPIO.HIGH)
                    #GPIO.output(red_led, GPIO.LOW)
                    #GPIO.output(blue_led, GPIO.LOW)

                else: #on middle 1/3
                    print("Exists in middle 1/3 of frame")
                    #GPIO.output(blue_led, GPIO.HIGH)
                    #GPIO.output(red_led, GPIO.LOW)
                    #GPIO.output(green_led, GPIO.LOW)

                print(number_of_blobs, "blob(s) detected")
            else:
                print("white")
                #GPIO.output(red_led, GPIO.LOW)
                #GPIO.output(green_led, GPIO.LOW)
                #GPIO.output(blue_led, GPIO.LOW)

            cv.imshow('Blobs', blobs)
            cv.imshow('Red', red_mask)

            keyboard = cv.waitKey(30)
            if keyboard == 'q' or keyboard == 27:
                break
        except KeyboardInterrupt:
            GPIO.cleanup()
            break

    # cleanup
    camera.release()
    cv.destroyAllWindows()
    del camera
    print('Stopped')
    
