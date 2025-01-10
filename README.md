# README

## Hardware notes

1. Connect Button to  `GPIO 23 `
2. Connect LED to  `GPIO x `

> If you want to customize these pins, for whatever reason, after changing them, makes the changes in the script. You can do so by editing [app.py](app.py). Find the line `WIFI_RESET_PIN = 23` and change it there. 

## How to customize WIFI Settings

1. Create a new branch before making adjustments to your new pi project

```bash
# Create & Switch to your branch
git checkout -b [A_SUITABLE_NAME_PROJECT]
```

2. In [app.py](app.py) change the SSID name

```bash
AP_SSID="[A_PREFERRED_SSID_NAME]"
```

3. Create a new hotspot/access_point scope using `nmcli`. So that the script [network_manager.py](wifi_config/network_manager.py) can control it and create an AP when needed for you to provide as SSID and WPA2/PSK for the pi to connect to.

```bash
```