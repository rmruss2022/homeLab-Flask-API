import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button to gpio23
GPIO.setup(24, GPIO.OUT) #led to gpio24

GPIO.output(24, GPIO.HIGH)
time.sleep(0.2)
GPIO.output(24, GPIO.LOW)
GPIO.cleanup()
print("ran")
