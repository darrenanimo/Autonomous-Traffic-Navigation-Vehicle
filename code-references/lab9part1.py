# PWM Control Example
#
# This example shows how to do PWM with your OpenMV Cam.

import time
from pyb import Pin, Timer

tim = Timer(4, freq=1500) # Frequency in Hz
tim2 = Timer(2, freq=100)
# Generate a 1KHz square wave on TIM4 with 50%, 75% and 50% duty cycles on channels 1, 2 and 3 respectively.
ch1 = tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=10)
ch2 = tim2.channel(4, Timer.PWM, pin=Pin("P5"), pulse_width_percent=10)

print(tim.counter())
print(tim2.counter())
i = 10
j = 275000
rising1 = 1
rising2 = 1

while (True):
    print("ch1", ch1.pulse_width(), "ch2:",ch2.pulse_width())
    if (rising1 == 1):
        i = i + 1
        j = int(265000 + (i/90)*200000)
        ch1.pulse_width_percent(i)
        ch2.pulse_width(j)
        if (i == 90):
            rising1 = 0
    else:
        i = i - 1
        j = int(275000 + (i/90)*200000)
        ch1.pulse_width_percent(i)
        ch2.pulse_width(j)
        if (i == 10):
            rising1 = 1

    #ch 2 logic
    #if (rising2 == 1):
        #j = j + 1
        #ch2.pulse_width(0.11*(i/100)*2000)
        #if (j == 0.11*i*2000): #778
            #rising2 = 0
    #else:
        #j = j - 1
        #ch2.pulse_width(j)
        #if (j == 3200):#0.19*tim2.counter()): #451
            #rising2 = 1



    time.sleep_ms(100)
