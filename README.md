# README

With the long press of a button, the rpi disconnects from any previously connected WiFi Access Points (or if the WiFi is not configured, then it doesn't matter) and creates a new Access Point. 

You can then connect to that Access Point (Check out how to customize that below), navigate to [http://10.10.1.1](http://10.10.1.1) and provide a SSID and PWD for a visible 2.5GHz network that you what your rpi to connect to. 

It will then disable the self initited AP and connect to the provided SSID. If all goes well and the credentials were, correct, it will connect successfully. 

> [TBD] Blink meaning for status 

---

## Hardware notes

0. Clone the repo

```bash
git clone https://github.com/dattasaurabh82/rpi-wifi-configurator.git
```

1. Connect Button to  `GPIO 23 `
2. Connect LED to  `GPIO x `

> If you want to use a different pin for the button to reconfigure Wifi (for whatever reason) make sure to after changing them, makes the changes in the script. You can do so by editing [app.py](app.py). Find the line `WIFI_RESET_PIN = 23` and change it there. 

> [TBD] Wiring Diagram

## How to customize WIFI Settings

1. Create a new branch before making adjustments to your new pi project

```bash
# Create & switch to your branch
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

5. Create a virtual environment

```bash
python -m venv venv
source activate venv/bin/activate
```

> You must leep the new venv's name as `venv` 

6. Install dependencies

```bash
python -m pip install -r requirements.txt
```

7. Test Script

> Better run it when a monitor and keyboard is attached to the pi, as if you are SSHed into the rpi, then when it creates an AP, you will lose connection to your tunnel, until you connect to it's AP again as it disconnectes from any associated station.

```bash
pyhton app.py
```

Now you can _Long Press_ (> 4 sec) and you will see the prompts ...

Alright, now that it's working, let's organize ...

8. Commit & Push Changes

```bash
git commit -m "made my custom changes"

```
