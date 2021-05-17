import RPi.GPIO as GPIO
import time

def set_angle(angle, channel, pwm):
    duty = angle/18+2
    GPIO.output(channel, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(channel, False)
    pwm.ChangeDutyCycle(0)

