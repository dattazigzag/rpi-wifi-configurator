from button import Button
from runner import run_command
import time
from wifi_config.network_manager import NetworkManager
from wifi_config.web_server import run_server, server_running, stop_server
import threading

# * Note: From webserver.py
server_thread = None
server_running = False


# ------------------------------------------- #
# * Call backl functions for button presses * #
# ------------------------------------------- #

def on_short_press():
    print("[app.py][Event] Short Press")
    print("[app.py][Action] Do nothing ...")


def on_long_press():
    global server_thread, server_running
    print("\n[app.py][Event] Long Press")
    if not server_running:
        print("[app.py][Action] Setting up Access Point ...")
        NetworkManager.setup_ap()
        server_thread = threading.Thread(target=run_server)
        server_thread.start()
        print("[app.py][Result] Web server started. Connect to the Wi-Fi and navigate to http://10.10.1.1")
    else:
        print("[app.py][Result] Server is already running.")


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
    global server_thread, server_running
    while True:
        time.sleep(1)
        if not server_running and server_thread and not server_thread.is_alive():
            print("Wi-Fi configuration process completed.")
            server_thread = None

# ------------------------------------------ #

print("-----------------------")
print("KOMOREBI SYS VIEW | LOG")
print("-----------------------")
print("Artist: Saurabh Datta")
print("Loc: Berlin, Germany")
print("Date: Sept|2024")
print("-----------------------")

# TBD 
# If wifi connected print IP address
# if not type this message below
# print("\n[app.py][Next step] Long press the wifi button to ")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[app.py][Result] Program stopped")