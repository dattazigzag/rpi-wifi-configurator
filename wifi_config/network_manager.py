import subprocess
import time

class NetworkManager:
    @staticmethod
    def setup_ap():
        try:
            subprocess.run(["sudo", "nmcli", "con", "up", "hotspot"], check=True)
            print("[net_manager.py][Result] Access Point set up successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[net_manager.py][Result] Failed to set up Access Point: {e}")

    @staticmethod
    def connect_to_wifi(ssid, password):
        commands = [
            f"sudo nmcli dev wifi connect '{ssid}' password '{password}'",
            "sudo nmcli con down hotspot",
            "sudo nmcli con delete hotspot"
        ]
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(f"[net_manager.py][Debug] Command: {cmd}")
            print(f"[net_manager.py][Debug] Return code: {result.returncode}")
            print(f"[net_manager.py][Debug] Stdout: {result.stdout}")
            print(f"[net_manager.py][Debug] Stderr: {result.stderr}")
            if result.returncode != 0:
                return False, f"[net_manager.py][Error] {result.stderr}"

        # Check if we're actually connected
        for _ in range(20):  # Try for about 20 seconds
            if NetworkManager.is_connected_to_wifi():
                return True, "[net_manager.py][Result] Connected successfully"
            time.sleep(1)

        return False, "[net_manager.py][Error] Failed to confirm WiFi connection"

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