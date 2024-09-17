from button import Button
from runner import run_command
import time
from wifi_config.network_manager import NetworkManager
from wifi_config.web_server import run_server 
import threading

print("KOMOREBI LOG")


# ------------------------------------------- #
# * Call backl functions for button presses * #
# ------------------------------------------- #

def on_short_press():
    print("[*] Short Press")

def on_long_press():
    print("\n[***] Long Press")
    print("Setting up Access Point ...")
    NetworkManager.setup_ap()
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    print("Web server started. Connect to the Wi-Fi and navigate to http://10.10.1.1")
    # Wait for the server to stop (this will happen after successful Wi-Fi connection)
    server_thread.join()
    # block
    print("Wi-Fi configuration process completed.")

# ------------------------------------------ #
# ******** Create a Button instance ******** #
# ------------------------------------------ #

# Default GPIO pin is 23 
# Default debounce time is 10 ms (0.01)
# Default long press threshold time period is 5 sec

button = Button(pin=23, debounce_time=0.02, long_press_time=4)
button.on_short_press = on_short_press
button.on_long_press = on_long_press

# ------------------------------------------ # 

def main():
    while True:
        # Your main program code here
        time.sleep(10)

# ------------------------------------------ #


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program stopped")