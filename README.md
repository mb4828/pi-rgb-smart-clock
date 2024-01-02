PI RGB Smart Clock
==================

Python project for driving a Raspberry Pi powered RGB matrix display acting as a smart clock, displaying time, temperature, weather, stock market, and other data.

Hardware used:
- [Raspberry Pi 4 Model B (2GB)](https://www.adafruit.com/product/4292)
- [RGB Matrix Bonnet](https://www.adafruit.com/product/3211) - [Programming Guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/overview)
- [64x32 RGB Matrix Display](https://www.adafruit.com/product/2279)
- [TEMPer2 USB Temperature Sensor](https://www.amazon.com/gp/product/B0B7SM95SX/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)

Inspired by: 
- https://github.com/c0wsaysmoo/plane-tracker-rgb-pi
- https://github.com/ColinWaddell/its-a-plane-python

Copyright &copy; 2024 Matt Brauner

## Getting started

### Installing the code

1. Install [Python 3.11](https://www.python.org/downloads/) if not installed already. This project must be run with Python 3.11 or higher
2. Setup virtual environment
    ```
    python3 -m venv venv
    pip3 install -r requirements.txt
    ```
3. Create [config.py](./config.py) file with the following content
    ```
    # https://www.tomorrow.io
    TOMORROWIO_API_KEY = 'yourTomorrowIOApiKey' 
    TOMORROWIO_ZIP_CODE = 'yourZipCode US'
    ```
4. Run [main.py](./main.py)

### Running on startup

If you want to run the clock automatically on start up, use the following steps:

1. Open the `rc.local` file
    ```
    sudo nano /etc/rc.local
    ```
2. Add the following line before the `exit 0` line
    ```
    python3 /path/to/main.py &
    ```
3. Save the file and exit
4. Make `rc.local` executable
    ```
    sudo chmod +x /etc/rc.local
    ```
5. Reboot the RPi to ensure main.py runs on startup
    ```
    sudo reboot
    ps -elf | grep pi-rgb-smart-clock
    ```
6. If you want to kill the process
    ```
    sudo kill <pid>
    ```

### Pairing with Apple Homekit

If you want to use Apple Homekit to turn the clock on and off, use the following steps to install Homebridge and add the clock to Homekit:

1. [Install Homebridge](https://github.com/homebridge/homebridge/wiki/Install-Homebridge-on-Raspbian) on the RPi
2. Open the Homebridge UI at `http://<ip address of your RPi>:8581`
3. On the _Plugins_ page, install the [homebridge-http-webhooks](https://github.com/benzman81/homebridge-http-webhooks``) plugin
4. On the _Config_ page, copy/paste the contents of [http-webhooks-config.json](./http-webhooks-config.json) into the config, save, and restart Homebridge
5. On the _Status_ page, use the QR code to add Homebridge to Homekit