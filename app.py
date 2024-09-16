import RPi.GPIO as GPIO
from time import sleep

WIFI_RESET_PIN = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def button_pressed(WIFI_RESET_PIN):
    print("Button pressed.")

GPIO.setup(WIFI_RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(WIFI_RESET_PIN, GPIO.RISING, callback=button_pressed, bouncetime=10) # add rising edge detection on a channel


try:
    while True:
        sleep(10)
finally:
    GPIO.cleanup()
