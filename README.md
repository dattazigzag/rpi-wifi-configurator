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
# ------------------------------------------- #
# ************* Global Variables ************ #
# ------------------------------------------- #

AP_SELF_IP = "10.10.1.1"
AP_SSID="[A_PREFERRED_SSID_NAME]"
```
