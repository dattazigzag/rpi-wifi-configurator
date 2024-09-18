import subprocess
from time import sleep
from logger import logger

in_ap_mode = False
in_stn_mode = False

class NetworkManager:
    @staticmethod
    def setup_ap():
        global in_ap_mode, in_stn_mode
        try:
            subprocess.run(["sudo", "nmcli", "radio", "wifi", "on"], check=True)
            sleep(2)
            subprocess.run(["sudo", "nmcli", "con", "down", "hotspot"], check=True)
            sleep(2)
            subprocess.run(["sudo", "nmcli", "con", "up", "hotspot"], check=True)
            sleep(2)
            logger.info("[net..._manager.py][Result] Access Point set up successfully.")
            in_ap_mode = True
            in_stn_mode = False
        except subprocess.CalledProcessError as e:
            logger.error(f"[net..._manager.py][Result] Failed to set up Access Point: {e}")
            in_ap_mode = False

    @staticmethod
    def connect_to_wifi(ssid, password):
        global in_ap_mode, in_stn_mode

        # Connect to the new network
        cmd = f"sudo nmcli dev wifi connect '{ssid}' password '{password}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)

        logger.debug(f"[net..._manager.py][Result] Command: {cmd}")
        logger.debug(f"[net..._manager.py][Result] Return code: {result.returncode}")
        logger.debug(f"[net..._manager.py][Result] Stdout: {result.stdout}")
        logger.debug(f"[net..._manager.py][Result] Stderr: {result.stderr}")

        # Wait for connection to stabilize
        sleep(5)

        if result.returncode != 0:
            in_stn_mode = True
            return False, f"[net..._manager.py][Result] Connected successfully to {ssid}"

        # if return code is 0, check if it is actually connected
        if NetworkManager.is_connected_to_wifi():
            # If connected, then bring down the hotspot
            logger.debug(f"[net..._manager.py][Result] Connected successfully to {ssid}! Bringing AP hotspot down ...")
           
            cmd = subprocess.run(["sudo", "nmcli", "con", "down", "hotspot"], check=True)
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)

            logger.debug(f"[net..._manager.py][Result] Command: {cmd}")
            logger.debug(f"[net..._manager.py][Result] Return code: {result.returncode}")
            logger.debug(f"[net..._manager.py][Result] Stdout: {result.stdout}")
            logger.debug(f"[net..._manager.py][Result] Stderr: {result.stderr}")

            # wait a tiny bit
            sleep (2)

            if result.returncode != 0:
                return False, f"[net..._manager.py][Result] Could not bring AP hotspot down after connecting to WIFI in  mode"
            
            in_ap_mode = False
            in_stn_mode = True
            return True, "[net..._manager.py][Result] Connected successfully"
        else:
            in_stn_mode = False
            return False, "[net..._manager.py][Result] Failed to confirm WiFi connection"


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