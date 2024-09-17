from button import Button
import time


print("KOMOREBI LOG")


# ---------------------------- #
# * Create a Button instance * #
# ---------------------------- #
# Default GPIO pin is 23 
# Default debounce time is 10 ms (0.01)
# Default long press threshold time period is 5 sec
button = Button(pin=23, debounce_time=0.02, long_press_time=4)


def main():
    while True:
        # 
        # Your main program code here
        # 
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program stopped")