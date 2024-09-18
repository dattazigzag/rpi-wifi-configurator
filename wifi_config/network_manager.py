import subprocess
from time import sleep
from logger import logger

class NetworkManager:
    @staticmethod
    def setup_ap():
        try:
            subprocess.run(["nmcli", "con", "up", "hotspot"], check=True)
            sleep(2)
            logger.info("[net..._manager.py][Result] Access Point set up successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"[net..._manager.py][Result] Failed to set up Access Point: {e}")


    @staticmethod
    def connect_to_wifi(ssid, password):
        try:
            # Connect to the new network
            cmd = f"nmcli dev wifi connect '{ssid}' password '{password}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)

            logger.debug(f"[net..._manager.py][Result] Command: {cmd}")
            logger.debug(f"[net..._manager.py][Result] Return code: {result.returncode}")
            logger.debug(f"[net..._manager.py][Result] Stdout: {result.stdout}")
            logger.debug(f"[net..._manager.py][Result] Stderr: {result.stderr}")

            # Wait for connection to stabilize
            sleep(15)

            # If it could not connect to user provided SSID ...
            if not NetworkManager.is_connected_to_wifi():
                return False, f"Failed to connect to {ssid}"
            
            # If it could connect to user provided SSID ...
            try:
                subprocess.run(["nmcli", "con", "down", "hotspot"], check=True)
                sleep(2)
                logger.debug("[net..._manager.py][Result] Hotspot brought down successfully.")
                return True, f"Connected successfully to {ssid}"
            except subprocess.CalledProcessError as e:
                logger.error(f"[net..._manager.py][Result] Failed to bring down hotspot: {e}")
                return False, f"Could not bring AP hotspot down after connecting to WIFI in  mode"
            
        except subprocess.CalledProcessError as e:
            print(e)
            logger.error(f"[net..._manager.py][Result] Error connecting to WiFi: {e.stderr}")
            return False, "Error connecting to WiFi"


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