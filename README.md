# README

With the Push of a button, it disconnectes from any previously connected WiFi Access Point (or if the wifi is not configured, then it doesn't matter) and creates a new Access Point. 

You can then connect to that Access Point (Check out how to customize that below), navigate to [http://10.10.1.1](http://10.10.1.1) and provide a SSID and PWD for a visible 2.5GHz network you what your rpi to connect to. 

It will then disable the self initited AP and connect to the provided SSID. If all goes well and the credentials were, correct, it will connect successfully. 
> [TBD] Blink meaning for status 

## Hardware notes

1. Connect Button to  `GPIO 23 `
2. Connect LED to  `GPIO x `

> If you want to customize these pins, for whatever reason, after changing them, makes the changes in the script. You can do so by editing [app.py](app.py). Find the line `WIFI_RESET_PIN = 23` and change it there. 

> [TBD] Wiring Diagram

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
sudo nmcli con add \
    type wifi \
    ifname wlan0 \
    con-name hotspot \
    autoconnect no \
    ssid [SAME_SSID_USED_ABOVE] \
    mode ap \
    ipv4.method shared \
    ipv4.addresses 10.10.1.1/24 \
    wifi-sec.key-mgmt wpa-psk \
    wifi-sec.psk "[YOUR_WPA2/PSK_PWD]"
```

> The value of `wifi-sec.psk` __must be same__ as the value of `AP_SSID` modified in [app.py](app.py)

4. Edit the html to customize according to your needs. Specifically edit these two files:
    
    1. [index.html](wifi_config/templates/index.html)

    ```html
    <title>[YOUR_PROJECT_NAME] Wi-Fi Configuration</title>
    ```

    ```html
    <h1>[YOUR_PROJECT_NAME] Wi-Fi Configuration</h1>
    ```

    2. [general.html](wifi_config/templates/general.html)

    ```html
    <title>[YOUR_PROJECT_NAME]</title>
    ```

    ```html
    <h1>[YOUR_PROJECT_NAME]</h1>
    ```

5. Create virtual environment

```bash
```

6. Install dependencies

```bash
```

7. Test Script

```bash
```

8. Commit & Push Changes

```bash
```
