PI RGB Smart Clock
==================

Python project for driving a Raspberry Pi powered RGB matrix display, displaying clock and other data.

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
