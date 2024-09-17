
from time import sleep
import board
import digitalio

'''
* TBD
1. write and rotate log files
2. Make the logger as a module
3. write the button unit as a module
4. write the led unit as a module
5. Check write functions
'''
 

print("KOMOREBI LOG")


button = digitalio.DigitalInOut(board.D23)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

while True:
    print(button.value)
    sleep(1)
