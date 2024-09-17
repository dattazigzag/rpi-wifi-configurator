import os
import sys
from network_manager import NetworkManager
from web_server import run_server
import threading


# Ensure we're using the virtual environment
# venv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'venv', 'bin', 'activate_this.py')
# exec(open(venv_path).read(), {'__file__': venv_path})


def main():
    print("Press 'A' and hit Enter to start the Wi-Fi configuration process.")
    while True:
        user_input = input().strip().lower()
        if user_input == 'a':
            break
        else:
            print("Invalid input. Please press 'A' and hit Enter.")

    print("Setting up Access Point...")
    NetworkManager.setup_ap()
    print("Access Point set up. SSID: KOMOREBI-PI-STICK, Password: komorebi123")
    print("Starting web server...")
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    print("Web server started. Connect to the Wi-Fi and navigate to http://10.10.1.1")


if __name__ == "__main__":
    main()