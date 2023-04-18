import time 
import smbus 
import RPi.GPIO as GPIO

bus = smbus.SMBus(1) 
address=0x40 
  
off_time = 246 
dir = 1 

input1 = 31
input2 = 33
ledpin = 35

mode1 = bus.read_byte_data(address, 0) 
print("Mode1 Reg = ", hex(mode1)) 
mode1 = mode1 | 0x10 
bus.write_byte_data(address, 0, mode1)  
bus.write_byte_data(address, 0xFE, 60) 
mode1 = mode1 & ~0x10 
bus.write_byte_data(address, 0, mode1) 
time.sleep(1) 
mode1 = bus.read_byte_data(address, 0) 
print("Mode1 Reg = ", hex(mode1)) 
bus.write_byte_data(address, 1, 4) 
ps = bus.read_byte_data(address, 0xFE) 
print("prescale = ", ps) 
time.sleep(.5) 

off_time = 1000
ch0 = 614

bus.write_byte_data(address, 7, 0) 
bus.write_byte_data(address, 6, 0) 

bus.write_byte_data(address, 11, 0)
bus.write_byte_data(address, 10, 0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(input1,GPIO.IN)
GPIO.setup(input2,GPIO.IN)
GPIO.setup(ledpin, GPIO.OUT, initial=GPIO.HIGH)

while True: 
    time.sleep(0.02) 
    if ((GPIO.input(31) == GPIO.LOW) and (GPIO.input(33) == GPIO.LOW)):
        GPIO.output(ledpin, GPIO.LOW)
        
        bus.write_byte_data(address, 9, 650>>8)
        bus.write_byte_data(address, 8, 650 & 0xFF)
        
        bus.write_byte_data(address, 13, 0>>8)
        bus.write_byte_data(address, 12, 0 & 0xFF)


    elif ((GPIO.input(31) == GPIO.LOW) and (GPIO.input(33) == GPIO.HIGH)):
        GPIO.output(ledpin, GPIO.LOW)
        
        bus.write_byte_data(address, 9, 451>>8)
        bus.write_byte_data(address, 8, 451 & 0xFF)
        
        bus.write_byte_data(address, 13, 2048>>8)
        bus.write_byte_data(address, 12, 2048 & 0xFF)

    elif((GPIO.input(31) == GPIO.HIGH) and (GPIO.input(33) == GPIO.LOW)):
        GPIO.output(ledpin, GPIO.LOW)

        bus.write_byte_data(address, 9, 778>>8)
        bus.write_byte_data(address, 8, 778 & 0xFF)
        
        bus.write_byte_data(address, 13, 2048>>8)
        bus.write_byte_data(address, 12, 2048 & 0xFF)

    elif((GPIO.input(31) == GPIO.HIGH) and (GPIO.input(33) == GPIO.HIGH)):
        GPIO.output(ledpin, GPIO.HIGH)
        
        bus.write_byte_data(address, 9, 614>>8)
        bus.write_byte_data(address, 8, 614 & 0xFF)
        
        bus.write_byte_data(address, 13, 3276>>8)
        bus.write_byte_data(address, 12, 3276 & 0xFF)

