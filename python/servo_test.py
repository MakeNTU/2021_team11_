import RPi.GPIO as GPIO
import time

def SetAngle(angle):
    duty = angle/18+2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(12,GPIO.OUT)

pwm = GPIO.PWM(12, 50)

pwm.start(0)
while True:
    angle = input("input angle:")
    SetAngle(int(angle))

pwm.stop()
GPIO.cleanup()
