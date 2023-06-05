# UART Control

import time
from pyb import UART
from pyb import LED
from pyb import Pin, Timer

import sensor, image, os, tf, math, uos, gc

# sensor setup
sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=3000)          # Let the camera adjust.

net = None
labels = None
min_confidence = 0.5

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
    (255,   0,   0),
    (  0, 255,   0),
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

clock = time.clock()

#PWM setup

uart = UART(1, 115200)
uart.init(115200, bits = 8, parity=None, stop=1, flow=0)

tim = Timer(2, freq=100)
tim2 = Timer(4, freq=1500)

# P5 = Servo
#ch1 = tim.channel(4, Timer.PWM, pin=Pin("P5"))
# P7 = DC Motor
ch2 = tim2.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=0)

pin3 = Pin('P2', Pin.OUT_PP) #inA
pin2 = Pin('P3', Pin.OUT_PP) #inB

pin4 = Pin('P4', Pin.OUT_PP) #ENA
pin6 = Pin('P6', Pin.OUT_PP) #ENB

pin8 = Pin('P8', Pin.OUT_PP)
pin9 = Pin('P9', Pin.IN) #speed from Jetson
pin5 = Pin('P5', Pin.IN) #stop

pin3.value(1) #inAs
pin2.value(0) #inB

pin4.value(1) #enA
pin6.value(1) #enB

pin8.value(0)
            #low battery values
slower = 14 #15
faster = 16 #16
fromstop =20

#working : 14 16

in1 = 'x'
prev_in = 'x'

print("Test Program Started")
red_led = LED(1)
green_led = LED(2)
blue_led  = LED(3)
red_led.on()
green_led.on()
blue_led.on()
time.sleep_ms(3000)
red_led.off()
green_led.off()
blue_led.off()
#ch1.pulse_width(370000)
ch2.pulse_width_percent(20)
time.sleep(0.2)
#ch2.pulse_width_percent(15)

sees_red_light = False
sees_green_light = False
sees_stop_sign = False
has_seen_stop_sign = False

pin8.value(1)

while(True):
    clock.tick()

    img = sensor.snapshot()

    for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
        if (i == 0): continue # background class
        if (len(detection_list) == 0): continue # no detections for this class?

        print("********** %s **********" % labels[i])
        if (labels[i] == "red_light"):
            sees_red_light = True
            sees_green_light = False
            sees_stop_sign = False
            has_seen_stop_sign = False
        elif (labels[i] == "stop_sign"):
            sees_stop_sign = True
            sees_red_light = False
            sees_green_light = False
        elif (labels[i] == "green_light"):
            sees_green_light = True
            sees_red_light = False
            sees_stop_sign = False
            has_seen_stop_sign = False
        else:
            sees_red_light = False
            sees_stop_sign = False
            sees_green_light = False
            has_seen_stop_sign = False

    #if (uart.any() > 0):
    #    prev_in = in1
    #    ch = uart.read(6)
    #    #print(ch)
    #    in1 = ch.decode()
    #    length = len(in1)
        #print(length)
    #    print(in1)
    red_led.off()
    green_led.off()
    blue_led.off()

    if (in1 == 0 or sees_red_light == True):
        ch2.pulse_width_percent(0)
        red_led.on()
        green_led.on()
        blue_led.off()
    elif (pin5.value() == 1):
        ch2.pulse_width_percent(0)

    if(sees_stop_sign == True and has_seen_stop_sign == False):
        ch2.pulse_width_percent(0)
        blue_led.on()
        green_led.off()
        red_led.off()
        #now = time.time()
        #while(time.time() < now + 5):
            ##if (uart.any() > 0):
            ##    uart.read(6)
        print("waiting for stop")
        #    pass
        time.sleep(4)
        sees_stop_sign = False
        has_seen_stop_sign = True
        now = time.time()
        blue_led.off()
        ch2.pulse_width_percent(fromstop)
        time.sleep(2)
        ch2.pulse_width_percent(slower)

        #while(time.time() < now + 3):
        #    if (time.time() < now + 2):
        #        ch2.pulse_width_percent(faster)
        #    else:
        #        ch2.pulse_width_percent(slower)
        #    pass
   # elif(sees_green_light == True):
   #     green_led.on()
   #     red_led.off()
   #     blue_led.off()
#        ch2.pulse_width_percent(green)
#        now = time.time()
#        while(time.time() < now + 2):
#            pass
#        sees_green_light = False
    elif (pin9.value() == 0):
        ch2.pulse_width_percent(slower)
        #print("faster")
        blue_led.on()
        red_led.off()
        green_led.off()
        has_seen_stop_sign = False
    elif (pin9.value() == 1):
        ch2.pulse_width_percent(faster)
        #print("slower")
        blue_led.off()
        red_led.off()
        green_led.off()
        has_seen_stop_sign = False

    else:
        has_seen_stop_sign = False
        #now = time.time()
        #while(time.time() < now + 9):
        #    ch2.pulse_width_percent(16)
        #    print("slow")
        #now = time.time()
        #while(time.time() < now + 2):
        #    ch2.pulse_width_percent(18)
        #    print("fast")


    #


#    elif (in1 == 999999):
#        ch2.pulse_width_percent(18)
#    elif (in1 == 777777):
#        ch2.pulse_width_percent(0)
#        #ch1.pulse_width(370000)
#        pin2.value(1) #inA
#        pin3.value(0) #inB
#        ch2.pulse_width_percent(18)
#        now = time.time()
#        while(time.time() < now - 20):
#            ##ch2.pulse_width_percent(17)
#            pass


    #elif( int(in1) < 200 and int(in1) > 30):
        #angle = int(in1)
        #if (int(in1) > 110):
            #ch2.pulse_width_percent(16)
        #elif (int(in1) < 70):
            #ch2.pulse_width_percent(16)
        #elif (int(in1) > 100):
            #ch2.pulse_width_percent(16)
        #elif (int(in1) < 80):
            #ch2.pulse_width_percent(16)
        #else:
            #ch2.pulse_width_percent(16)

        #if (int(in1) > 120):
            #angle = 120
        #elif (int(in1) < 60):
            #angle = 60
        #turn = 370000 + 2700 * (90 - angle)
        ##print("turn=",turn)
        #ch1.pulse_width(turn)
        #angle5 = angle4
        #angle4 = angle3
        #angle3 = angle2
        #angle2 = angle1
        #angle1 = angle



    #if ((angle5+angle4+angle3+angle2+angle1) / 5 == angle1):
        ##ch2.pulse_width_percent(18)
        ##print("stuck")
        #now = time.time()
        #while(time.time() < now - 10):
            #pass





