from button import Button
from runner import run_command
import time
from wifi_config.network_manager import NetworkManager
from wifi_config.web_server import run_server, server_running, stop_server
from dns_server import DNSServer
import threading
from logger import logger


# * Note: From webserver and DNSServer 
server_thread = None
server_running = False
dns_thread = None
dns_server = None



# ------------------------------------------- #
# * Call backl functions for button presses * #
# ------------------------------------------- #

def on_short_press():
    logger.info("[app.py][Event] Short Press")
    logger.info("[app.py][Action] Do nothing ...")


def on_long_press():
    global server_thread, server_running, dns_thread, dns_server
    logger.info("\n[app.py][Event] Long Press")
    if not server_running:
        logger.info("[app.py][Action] Setting up Access Point ...")
        NetworkManager.setup_ap()

        ip = "10.10.1.1"  # Static IP for the Access Point
        
        server_thread = threading.Thread(target=run_server)
        dns_server = DNSServer(ip)
        dns_thread = threading.Thread(target=dns_server.run)

        server_thread.start()
        dns_thread.start()

        logger.info("[app.py][Result] Web server and DNS Server started. Connect to the Wi-Fi and navigate to http://10.10.1.1")
    else:
        logger.info("[app.py][Result] Server is already running.")


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
    global server_thread, server_running, dns_thread, dns_server
    while True:
        time.sleep(1)
        if not server_running and server_thread and not server_thread.is_alive():
            logger.info("[app.py][Result] Wi-Fi configuration process completed.")
            server_thread = None
            if dns_server:
                dns_server.stop()
                dns_thread.join()
                dns_thread = None
                dns_server = None

# ------------------------------------------ #

logger.info("-----------------------")
logger.info("KOMOREBI SYS VIEW | LOG")
logger.info("-----------------------")
logger.info("Artist: Saurabh Datta")
logger.info("Loc: Berlin, Germany")
logger.info("Date: Sept|2024")
logger.info("-----------------------")

# TBD 
# If wifi connected print IP address
# if not type this message below
# logger.info("\n[app.py][Next step] Long press the wifi button to ")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("[app.py][Result] Program stopped")