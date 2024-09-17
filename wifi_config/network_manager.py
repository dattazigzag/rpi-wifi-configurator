import subprocess
import time

class NetworkManager:
    @staticmethod
    def setup_ap():
        # Commands to set up AP mode
        commands = [
            "nmcli con add type wifi ifname wlan0 con-name hotspot autoconnect yes ssid KOMOREBI-PI-STICK",
            "nmcli con modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared",
            "nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk",
            "nmcli con modify hotspot wifi-sec.psk komorebi123",
            "nmcli con up hotspot"
        ]
        for cmd in commands:
            subprocess.run(cmd, shell=True, check=True)

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