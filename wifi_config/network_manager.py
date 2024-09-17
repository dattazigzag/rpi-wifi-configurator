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

    @staticmethod
    def get_wifi_networks():
        try:
            # Temporarily disable AP
            subprocess.run(["sudo", "nmcli", "con", "down", "hotspot"], check=True)
            time.sleep(2)  # Give some time for the interface to switch modes
            
            cmd = "sudo nmcli -f SSID,FREQ dev wifi list | grep -v '5[0-9]\{3\}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            networks = [line.split()[0] for line in result.stdout.split('\n') if line.strip()]
            
            # Re-enable AP
            subprocess.run(["sudo", "nmcli", "con", "up", "hotspot"], check=True)
            return networks
        except subprocess.CalledProcessError as e:
            print(f"Error getting Wi-Fi networks: {e}")
            return []

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
        time.sleep(5)  # Wait for connection to stabilize
        return True, "Connected successfully"

    @staticmethod
    def get_current_ip():
        cmd = "hostname -I | awk '{print $1}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

    @staticmethod
    def exit_ap_mode():
        try:
            subprocess.run(["sudo", "nmcli", "con", "down", "hotspot"], check=True)
            subprocess.run(["sudo", "nmcli", "con", "delete", "hotspot"], check=True)
            # Try to connect to the last known connection
            subprocess.run(["sudo", "nmcli", "con", "up", "$(nmcli -g NAME con show --active)"], shell=True, check=True)
            return True, "Exited AP mode and reconnected to previous network"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to exit AP mode: {e}"