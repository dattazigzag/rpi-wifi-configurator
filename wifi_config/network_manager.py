import subprocess
from time import sleep

class NetworkManager:
    @staticmethod
    def setup_ap():
        try:
            subprocess.run(["sudo", "nmcli", "con", "up", "hotspot"], check=True)
            print("Access Point set up successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to set up Access Point: {e}")


    @staticmethod
    def connect_to_wifi(ssid, password):
        commands = [
            f"sudo nmcli dev wifi connect '{ssid}' password '{password}'",
            "sudo nmcli con down hotspot",
            "sudo nmcli con delete hotspot"
        ]
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                return False, result.stderr
        sleep(5)  # Wait for connection to stabilize
        return True, "Connected successfully"

    @staticmethod
    def get_current_ip():
        cmd = "hostname -I | awk '{print $1}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()