PI RGB Smart Clock
==================

Python project for driving a Raspberry Pi powered RGB matrix display acting as a smart clock, displaying time, temperature, weather, and other data.

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
