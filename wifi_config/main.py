from network_manager import NetworkManager
from web_server import run_server
import threading

def main():
    print("Press 'A' and hit Enter to start the Wi-Fi configuration process.")
    while True:
        user_input = input().strip().lower()
        if user_input == 'a' or user_input == 'A':
            break
        else:
            print("Invalid input. Please press 'A' or 'a' and hit Enter.")

    print("Setting up Access Point...")
    NetworkManager.setup_ap()
    print("Access Point set up. SSID: KOMOREBI-PI-STICK, Password: komorebi123")
    print("Starting web server...")
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    print("Web server started. Connect to the Wi-Fi and navigate to http://10.10.1.1")

    # Wait for the server to stop (this will happen after successful Wi-Fi connection)
    server_thread.join()

    print("Wi-Fi configuration process completed.")


if __name__ == "__main__":
    main()