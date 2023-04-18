# UART Control

import time
from pyb import UART
from pyb import LED
from pyb import Pin, Timer

uart = UART(1, 115200)
uart.init(115200, bits = 8, parity=None, stop=1, flow=0)

tim = Timer(2, freq=100)
tim2 = Timer(4, freq=1500)

ch1 = tim.channel(4, Timer.PWM, pin=Pin("P5"), pulse_width_percent=10)
ch2 = tim2.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=20)

in1 = '0'
in2 = '0'

ff = 0

print("Lab 9 Part 2 Program Started")
red_led = LED(1)
red_led.on()
time.sleep_ms(5000)
red_led.off()

while(True):
    if (uart.any() > 0):
        ch = uart.readchar()
        if (ff == 0):
            in1 = chr(ch)
            ff = 1
        else:
            in2 = chr(ch)
            ff = 0

    if ( in1 == '0' and in2 == '0' ):
        print("in1 = 0, in2 = 0")
        ch1.pulse_width(360000)
        ch2.pulse_width_percent(20)
    elif ( in1 == '0' and in2 == '1' ):
        print("in1 = 0, in2 = 1")
        ch1.pulse_width(265000)
        ch2.pulse_width_percent(50)
    elif ( in1 == '1' and in2 == '0' ):
        print("in1 = 1, in2 = 0")
        ch1.pulse_width(455000)
        ch2.pulse_width_percent(50)
    elif ( in1 == '1' and in2 == '1' ):
        print("in1 = 1, in2 = 1")
        ch1.pulse_width(360000)
        ch2.pulse_width_percent(80)



