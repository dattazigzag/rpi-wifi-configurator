import RPi.GPIO as GPIO

print(GPIO.getmode())
GPIO.setmode(GPIO.BOARD)
print(GPIO.getmode())