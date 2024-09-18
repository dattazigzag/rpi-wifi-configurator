import subprocess
from time import sleep
from logger import logger

class NetworkManager:
    @staticmethod
    def setup_ap():
        logger.info("[net..._manager.py][Result] Turning predefined AP down, even though it maybe down... [wait 5 sec ...]")
        subprocess.run(["nmcli", "con", "down", "hotspot"], check=False)
        sleep(5)
        logger.info("[net..._manager.py][Result] Turning predefined AP up ... [wait 5 sec ...]")
        try:
            subprocess.run(["nmcli", "con", "up", "hotspot"], check=True)
            sleep(5)
            logger.info("[net..._manager.py][Result] Access Point set up successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"[net..._manager.py][Result] Failed to set up Access Point: {e}")


    @staticmethod
    def connect_to_wifi(ssid, password):
        cmd = f"nmcli dev wifi connect '{ssid}' password '{password}'"
        subprocess.run(cmd, shell=True, check=False)
        # Wait for connection to stabilize
        sleep(20)
        # If it could not connect to user provided SSID ...
        if not NetworkManager.is_connected_to_wifi():
            return False, f"Failed to connect to {ssid}"

        # TBD: Do we even need it? As, after conneting to WIFI it automatically goes into STN mode 
        # logger.info("[net..._manager.py][Result] Turning predefined AP down [wait 5 sec ...]")
        # subprocess.run(["nmcli", "con", "down", "hotspot"], check=False)
        # sleep(5)

        # If it could connect to user provided SSID ...
        return True, f"Connected successfully to {ssid}"
        

    @staticmethod
    def is_connected_to_wifi():
        cmd = "nmcli -t -f TYPE,STATE dev | grep '^wifi:connected$'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0


    @staticmethod
    def get_current_ip():
        cmd = "hostname -I | awk '{print $1}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()