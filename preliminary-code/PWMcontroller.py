# UART Control

import time
from pyb import UART
from pyb import LED
from pyb import Pin, Timer

def jumpstart(ch1):
    ch1.pulse_width_percent(21)
    now = time.time()
    while(time.time() < now - 7):
        #ch2.pulse_width_percent(17)
        pass

uart = UART(1, 115200)
uart.init(115200, bits = 8, parity=None, stop=1, flow=0)

tim = Timer(2, freq=100)
tim2 = Timer(4, freq=1500)

# P5 = Servo
ch1 = tim.channel(4, Timer.PWM, pin=Pin("P5"))
# P7 = DC Motor
ch2 = tim2.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=10)

pin2 = Pin('P2', Pin.OUT_PP) #inA
pin3 = Pin('P3', Pin.OUT_PP) #inB

pin4 = Pin('P4', Pin.OUT_PP) #ENA
pin6 = Pin('P6', Pin.OUT_PP) #ENB


pin2.value(0) #inA
pin3.value(1) #inB

pin4.value(1) #inA
pin6.value(1) #inB


in1 = 'x'
prev_in = 'x'

print("Test Program Started")
red_led = LED(1)
red_led.on()
time.sleep_ms(5000)
red_led.off()
ch1.pulse_width(370000)
ch2.pulse_width_percent(22)
time.sleep(0.2)

while(True):
    if (uart.any() > 0):
        prev_in = in1
        ch = uart.readchar()
        in1 = chr(ch)
        print(in1)


    # turn straight
    if ( in1 == 'S'):
        #print("straight")

        pin2.value(0) #inA
        pin3.value(1) #inB
        ch1.pulse_width(370000)
        if(prev_in == 'B'):
            jumpstart(ch1)
        ch2.pulse_width_percent(18)
    # turn right
    elif ( in1 == 'R' ):

        pin2.value(0) #inA
        pin3.value(1) #inB
        ch1.pulse_width(300000)
        if(prev_in == 'B'):
            jumpstart(ch1)
        ch2.pulse_width_percent(19)
    # turn left
    elif ( in1 == 'L' ):

        #print("left")
        pin2.value(0) #inA
        pin3.value(1) #inB
        ch1.pulse_width(440000)
        if(prev_in == 'B'):
            jumpstart(ch1)
        ch2.pulse_width_percent(19)
    # slight right
    elif ( in1 == ']' ):

        pin2.value(0) #inA
        pin3.value(1) #inB
        ch1.pulse_width(330000) #285000
        if(prev_in == 'B'):
            jumpstart(ch1)
        ch2.pulse_width_percent(18)
    # slight left
    elif ( in1 == '[' ):

        pin2.value(0) #inA
        pin3.value(1) #inB
        ch1.pulse_width(415000) #415000
        if(prev_in == 'B'):
            jumpstart(ch1)
        ch2.pulse_width_percent(18)

    # Motor Off
    elif ( in1 == '0'):
        ch2.pulse_width_percent(0)
    elif ( in1 == 'B'):
        #print("off")
        ch2.pulse_width_percent(0)
        #ch1.pulse_width(370000)
        pin2.value(1) #inA
        pin3.value(0) #inB
        ch2.pulse_width_percent(23)
        now = time.time()
        while(time.time() < now - 20):
            #ch2.pulse_width_percent(17)
            pass
    # medium
    elif ( in1 == 'y' ):
        #print("medium")
        ch2.pulse_width_percent(18)
    # slow
    else:
        pin2.value(0) #inA
        pin3.value(1) #inB
        ch1.pulse_width(370000)
        ch2.pulse_width_percent(19)




