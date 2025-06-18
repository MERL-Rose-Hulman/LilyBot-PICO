#motor A is the left motor
from machine import Pin, PWM
import time

ledPin = 18
triggerPin = 17
echoPin = 16
#led pin
led = Pin(ledPin, Pin.OUT) 
#pin for sonar
trigger = Pin(triggerPin, Pin.OUT) 
echo = Pin(echoPin, Pin.IN)
#motor A
AIN1 = Pin(26, Pin.OUT)
AIN2 = Pin(27, Pin.OUT)
PWMA = PWM(Pin(28))
PWMA.freq(100)
#motor B
BIN1 = Pin(22, Pin.OUT)
BIN2 = Pin(21, Pin.OUT)
PWMB = PWM(Pin(20))
PWMB.freq(100)
#setting motor speed
motorspeed = 25000

#funx that returns distance away from nearest obstacle
def dist():
    #making sure trigger is off
    trigger.value(0)
    time.sleep_us(2)
    #activate trigger
    trigger.value(1)
    time.sleep_us(10)
    #turn trigger back off
    trigger.value(0)
    #I realized that the sonar sometimes gets stucked so "timeout" is a temporary solution
    #timeout = 20000  # 20
    #start = time.ticks_us()
    while echo.value() == 0:
        print("timer hasn't started")
        pass
    startTime = time.ticks_us()
    while echo.value() == 1:
        pass
    endTime = time.ticks_us()
    timeElapsed = time.ticks_diff(endTime, startTime)
    distance = 0.0343 * timeElapsed / 2
    return distance

def forward():
    #motor A
    AIN1.value(0)
    AIN2.value(1) #2 is forward.ie: AIN2 & BIN2
    PWMA.duty_u16(motorspeed)
    #motor B
    BIN1.value(0)
    BIN2.value(1)
    PWMB.duty_u16(motorspeed)

def stop():
    PWMA.duty_u16(0)
    PWMB.duty_u16(0)
    
def pivot_right():
    #move motor A forward
    AIN1.value(0)
    AIN2.value(1)
    PWMA.duty_u16(motorspeed)
    #move motor B backward
    BIN1.value(1)
    BIN2.value(0)
    PWMB.duty_u16(motorspeed)

clearance = 20 #threshold distance in cm

try:
    while True:
        
        print("Starting....")
        distance_cm = dist()
        print("Distance = ", round(distance_cm, 2), "cm")
        if distance_cm <= clearance:
            led.value(1)
            print("Obstacle detected,turning right")
            stop()
            time.sleep(0.1)
            pivot_right()
            time.sleep(0.95)
            stop()
        else:
            led.value(0)
            print("No obstacle detected, moving forward")
            forward()

        time.sleep(0.5)  #just a brief pause

except KeyboardInterrupt:
    print("Stopping program...")

#making sure the PWM signals are set back to 0 at the end
#to avoid undetermined states
finally:
    print("Cleaning up...")
    stop()
    PWMA.duty_u16(0)
    PWMB.duty_u16(0)
    AIN1.value(0)
    AIN2.value(0)
    BIN1.value(0)
    BIN2.value(0)
    echo.value(0)
    
    
