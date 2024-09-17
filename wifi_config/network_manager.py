import subprocess
import time
from logger import logger

class NetworkManager:
    @staticmethod
    def setup_ap():
        try:
            subprocess.run(["sudo", "nmcli", "con", "up", "hotspot"], check=True)
            logger.info("Access Point set up successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to set up Access Point: {e}")

    @staticmethod
    def connect_to_wifi(ssid, password):
        commands = [
            f"sudo nmcli dev wifi connect '{ssid}' password '{password}'",
            "sudo nmcli con down hotspot",
            "sudo nmcli con delete hotspot"
        ]
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            logger.debug(f"Command: {cmd}")
            logger.debug(f"Return code: {result.returncode}")
            logger.debug(f"Stdout: {result.stdout}")
            logger.debug(f"Stderr: {result.stderr}")
            if result.returncode != 0:
                return False, f"Error: {result.stderr}"

        for _ in range(10):  # Try for about 10 seconds
            if NetworkManager.is_connected_to_wifi():
                return True, "Connected successfully"
            time.sleep(1)

        return False, "Failed to confirm WiFi connection"

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