from button import Button
from led import LED
from wifi_config.network_manager import NetworkManager
from wifi_config.web_server import run_server, stop_server, server_running, switch_to_ap_mode, switch_to_normal_mode, reset_wifi_state
import threading
import time
from logger import logger


# ------------------------------------------- #
# ************* Global Variables ************ #
# ------------------------------------------- #

AP_SELF_IP = "10.10.1.1"
AP_SSID="SERIAL_MONITOR_PI4"
WIFI_RESET_PIN = 23
LED_PIN = 24

# * Note: From webserver and DNSServer 
server_thread = None
server_running = False


# ------------------------------------------- #
# * Call backl functions for button presses * #
# ------------------------------------------- #

def on_short_press():
    logger.info("[app.py][Event] Short Press detected... Do nothing!")


def on_long_press():
    global server_thread, server_running
    logger.info("")
    logger.info("[app.py][Event] Long Press detected!")

    logger.info("[app.py][Action] Setting up Access Point ...")
    
    # Set LED to fast blink for AP mode
    status_led.set_state(LED.FAST_BLINK)
    
    
    # Set LED to fast blink for AP mode
    status_led.set_state(LED.FAST_BLINK)
    
    NetworkManager.setup_ap()
    reset_wifi_state() 
    switch_to_ap_mode()

    logger.info(f"[app.py][Result] AP mode activated. Connect to the Wi-Fi and navigate to http://{AP_SELF_IP}:8080")


# ------------------------------------------ #
# ******** Create a Button instance ******** #
# ------------------------------------------ #

button = Button(pin=WIFI_RESET_PIN, debounce_time=0.02, long_press_time=4)
# Note: Default Values in the class 
# GPIO pin is 23 
# Debounce time is 10 ms (0.01)
# Long press threshold time period is 5 sec

button.on_short_press = on_short_press
button.on_long_press = on_long_press

# ------------------------------------------ #
# -------- Process status signal LED ------- #
# ------------------------------------------ #
# status_led = LED(pin=LED_PIN)
status_led = LED(pin=LED_PIN, max_brightness=0.3)  # 30% brightness
from wifi_config.web_server import init_app
init_app(status_led)

# ------------------------------------------ # 

def main():
    global server_thread, server_running
    
    # Start the web server
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    server_running = True
    
    # Initialize last known state
    last_known_ip = NetworkManager.get_current_ip()
    last_known_mode = "normal" if last_known_ip != AP_SELF_IP else "ap"
    
    while True:
        time.sleep(1)
        current_ip = NetworkManager.get_current_ip()
        
        if NetworkManager.is_in_ap_mode():
            if last_known_mode != "ap":
                logger.info("[app.py][Action] Switched to AP mode.")
                switch_to_ap_mode()
                last_known_mode = "ap"
        elif current_ip != AP_SELF_IP and NetworkManager.is_connected_to_wifi():
            if last_known_mode != "normal":
                logger.info("[app.py][Action] Connected to Wi-Fi. Switching to normal mode...")
                switch_to_normal_mode()
                last_known_mode = "normal"
        
        last_known_ip = current_ip
                
# ------------------------------------------ #


logger.info("-----------------------")
logger.info("SERIAL MON SYS VIEW | LOG")
logger.info("-----------------------")
logger.info("Artist: Saurabh Datta")
logger.info("Loc: Berlin, Germany")
logger.info("Date: Jan, 2025")
logger.info("-----------------------")


# If wifi connected print IP address. if not type a message below
logger.info(f"[app.py][Status] Current IP: {NetworkManager.get_current_ip()}")
if NetworkManager.get_current_ip() == AP_SELF_IP:
    logger.info(f"[app.py][Status] Connect to wifi access point: {AP_SSID} and go to: http://serialmonitor.local:8080 or http://serialmonitor.lan :8080 to provide 2.5GHz Wifi credentials")
else:
    logger.info("[app.py][Status] To configure wifi, Long Press the Wifi Reset Button for more than 5 sec")
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if server_running:
            stop_server()
        logger.info("[app.py][Result] Program stopped")

