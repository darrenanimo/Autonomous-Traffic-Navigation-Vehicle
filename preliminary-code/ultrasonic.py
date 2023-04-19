import time
import RPi.GPIO as GPIO

trigger = 31
echo = 33

goLED = 36
stopLED = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(echo, GPIO.IN)

GPIO.setup(stopLED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(goLED, GPIO.OUT, initial=GPIO.LOW)
while True:
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger, GPIO.LOW)
    
    duration = None
    whilestart= time.time()
    while not GPIO.input(echo):
        if (time.time() - whilestart >= 0.5):
            break
        continue
    start = time.monotonic()
    
    while GPIO.input(echo):
        continue
    duration = time.monotonic() - start
    
    #cm = (duration/2) / 29.1 * 1000000
    
    cm = duration * 0.017 * 1000000
    
    print("distance:", cm)
    
    # if object is far, full speed
    if(cm > 30):
        GPIO.output(goLED, GPIO.HIGH)
        GPIO.output(stopLED, GPIO.LOW)
    # if near, slowdown
    #elif(cm <= 30):
        # slowdown
    # else if very close, stop
    else:
        GPIO.output(goLED, GPIO.LOW)
        GPIO.output(stopLED, GPIO.HIGH)
    
    time.sleep(0.5)
    
