
from time import sleep
import board
import digitalio

print("press the button!")


button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

while True:
    print(button.value)
    sleep(2)