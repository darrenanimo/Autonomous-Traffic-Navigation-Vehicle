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
    params.minArea = 25
    params.filterByColor = True
    params.blobColor = 255
    detector = cv.SimpleBlobDetector_create(params)
    
    red_lower = np.array([160, 100, 100], np.uint8)
    red_upper = np.array([179, 200, 255], np.uint8)

    #red_lower = np.array([0, 100, 20], np.uint8)
    #red_upper = np.array([10, 255, 255], np.uint8)

    red_lower2 = np.array([160, 100, 20], np.uint8)
    red_upper2 = np.array([179, 255, 255], np.uint8)

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
            red_mask2 = cv.inRange(hsvFrame, red_lower2, red_upper2)
            full_red_mask = red_mask + red_mask2
            red_mask_result = cv.bitwise_and(frame, frame, mask=full_red_mask)

            keypoints = detector.detect(red_mask)
            
            blank = np.zeros((1, 1))
            blobs = cv.drawKeypoints(frame, keypoints, blank, (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            
            number_of_blobs = len(keypoints)
            print(number_of_blobs)

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
    
