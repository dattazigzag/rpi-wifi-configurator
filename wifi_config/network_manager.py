import subprocess
import time

class NetworkManager:
    @staticmethod
    def setup_ap():
        try:
            subprocess.run(["sudo", "nmcli", "con", "up", "hotspot"], check=True)
            print("Access Point set up successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to set up Access Point: {e}")
            # TBD: Add some error handling or retry logic here

    @staticmethod
    def get_wifi_networks():
        cmd = "nmcli -f SSID,FREQ dev wifi list | grep -v '5[0-9]\{3\}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        networks = [line.split()[0] for line in result.stdout.split('\n') if line.strip()]
        return networks

    @staticmethod
    def connect_to_wifi(ssid, password):
        commands = [
            f"nmcli dev wifi connect '{ssid}' password '{password}'",
            "nmcli con down hotspot",
            "nmcli con delete hotspot"
        ]
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                return False, result.stderr
        time.sleep(5)  # Wait for connection to stabilize
        return True, "Connected successfully"

    @staticmethod
    def get_current_ip():
        cmd = "hostname -I | awk '{print $1}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()