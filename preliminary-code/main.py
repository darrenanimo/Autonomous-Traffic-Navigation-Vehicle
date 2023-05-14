import cv2 as cv

import numpy as np
import time
#from time import gmtime, strftime, sleep, time
import logging
import nanocamera as nano
import sys
import math
import RPi.GPIO as GPIO
import serial

import definitions as cam

def ultrasonic(ltrigger, lecho, rtrigger, recho):
    GPIO.output(left_trigger, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(left_trigger, GPIO.LOW)

    duration = None
    whilestart= time.time()
    while not GPIO.input(left_echo):
        if (time.time() - whilestart >= 0.5):
            break
        continue
    start = time.monotonic()

    while GPIO.input(left_echo):
        continue
    duration = time.monotonic() - start

    #cm = (duration/2) / 29.1 * 1000000

    left_distance = duration * 0.017 * 1000000
    right_distance = duration * 0.017 * 1000000
    print("distance:", left_distance)
    time.sleep(0.5)
    return left_distance, right_distance

def lane_detection(frame):
    average = 200
    # apply some gaussian blur to the image
    kenerl_size = (3, 3)
    gauss_image = cv.GaussianBlur(frame, kenerl_size, 1)
    # here we convert to the HSV colorspace
    hsv_image = cv.cvtColor(gauss_image, cv.COLOR_BGR2HSV)
    # apply color threshold to the HSV image to get only black colors
    thres_1 = cv.inRange(hsv_image, lower_black, upper_black)
    # dilate the the threshold image
    thresh = cv.dilate(thres_1, rectKernel, iterations=1)
    # apply canny edge detection
    low_threshold = 200
    high_threshold = 400
    canny_edges = cv.Canny(gauss_image, low_threshold, high_threshold)
    # get a region of interest
    roi_image = cam.region_of_interest(canny_edges)
    line_segments = cam.detect_line_segments(roi_image)
    lane_lines = cam.average_slope_intercept(frame, line_segments)
    # overlay the line image on the main frame
    line_image = cam.display_lines(frame, lane_lines)
    #HoughLines
    c_canny_edges = cv.cvtColor(canny_edges, cv.COLOR_GRAY2BGR)
    c_canny_edgesP = np.copy(c_canny_edges)
    hlines = cv.HoughLines(canny_edges, 1, np.pi / 180, 110, None, 0, 0)
    if hlines is not None:
        angle = 0
        for i in range(0, len(hlines)):
            rho = hlines[i][0][0]
            theta = hlines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(c_canny_edges, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
            angle = angle + theta
        average = angle / len(hlines)
        average = average * 180.0 / 3.14
        print("angle =", average)
    return c_canny_edges, average

# UART setup

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
    # Wait a second to let the port initialize
time.sleep(1)

#GPIO setup
GPIO.setmode(GPIO.BOARD)

left_trigger = 24
left_echo = 26
right_trigger = 36
right_echo = 38

GPIO.setup(left_trigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(left_echo, GPIO.IN)
GPIO.setup(left_trigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(left_echo, GPIO.IN)

# Camera setup
camera = nano.Camera()

    # define a range of black color in HSV
lower_black = np.array([0, 0, 0])
upper_black = np.array([227, 100, 70])

    # Rectangular Kernel
rectKernel = cv.getStructuringElement(cv.MORPH_RECT,(7,7))


if __name__=='__main__':

    print('Started')
    now = time.time()
    # Servo Control, accepts L, S, R
    direction = "S"
    # Variable speed, 0-10 are valid values
    speed = "0"
    prevspeed = "1"

    serial_port.write("UART Demonstration Program\r\n".encode())
    try:
        while True:
            #fetching each frame
            frame = camera.read()
            if frame is None:
                print("frame is none")
                break

            cv.imshow('Blobs', frame)
            
            # lane detection
            canny, angle = lane_detection(frame)
            cv.imshow('Canny Edges', canny)
            # object detection
            #left_dist, right_dist = ultrasonic(left_trigger, left_echo, right_trigger, right_echo)
            
            # Motor Speed
            #if (left_dist < 10 or right_dist < 10):
            if frame is None:
                speed = "0"
            else:
                speed = "2"
            # turn
            if (angle > 175 or angle < 5):
                direction = "S"
            elif (angle < 175 and angle > 90):
                direction = "L"
            elif (angle > 5 and angle < 90):
                direction = "R"
            if (speed != prevspeed):
                serial_port.write(speed.encode())
            serial_port.write(direction.encode())
            prevspeed = speed
            #if serial_port.inWaiting() > 0:
            #    data = serial_port.read()
            #    print(data)
            #    serial_port.write(data)
            #    if data == "\r".encode():
                    # For Windows boxen on the other end
            #        serial_port.write("\n".encode())

            keyboard = cv.waitKey(30)
            if keyboard == 'q' or keyboard == 27:
                break
    except KeyboardInterrupt:
        print("keyboard interrupt")

    finally:
        GPIO.cleanup
        camera.release()
        cv.destroyAllWindows()
        del camera
        print('Stopped')
    
