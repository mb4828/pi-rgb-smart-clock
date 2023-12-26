"""
Fetches data from various APIs
"""

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

from config import TOMORROWIO_API_KEY, TOMORROWIO_ZIP_CODE

EXTERNAL_CHECK_INTERVAL = 5 # new data every 5 minutes
last_external_check = datetime(1990,1,1)
cached_data = {}

""" Gets weather data from tomorrow.io """
def get_weather():
    try:
        request = requests.get(
            'https://api.tomorrow.io/v4/weather/realtime',
            params={
                "location": TOMORROWIO_ZIP_CODE,
                "units": "imperial",
                "apikey": TOMORROWIO_API_KEY
            }
        )
        request.raise_for_status()
        data = request.json()["data"]["values"]
        return {
            'temp': round(data.get('temperature', 0)), 
            'humidity': round(data.get('humidity', 0)), 
            'icon': data.get('weatherCode')
        }
    except requests.exceptions.RequestException as e:
        print(f"Request failed. Error: {e}")
        return {}
    

""" Gets stock data from Yahoo finance """
def get_stocks():
    stock_list = ['^GSPC','^DJI','^IXIC']
    results = []
    try:
        request = requests.get(f'https://finance.yahoo.com/')
        request.raise_for_status()
        data = request.text
        soup = BeautifulSoup(data, 'html.parser')
        for stock in stock_list:
            price = soup.find(attrs={'data-symbol': stock, 'data-field': 'regularMarketPrice'})
            change = soup.find(attrs={'data-symbol': stock, 'data-field': 'regularMarketChangePercent'})
            if price and change:
                results.append({'ticker': stock, 'price': float(price['value']), 'change': round(float(change['value']), 2)})
    except requests.exceptions.RequestException as e:
        print(f"Request failed. Error: {e}")
    return results

def get_time():
    return datetime.now().strftime('%-I:%M:%S %p')

def get_date():
    return datetime.now().strftime('%b %-d')

def get_data():
    # cache data so we're not hitting external apis every second
    global last_external_check
    global cached_data
    drop_cache = False
    if last_external_check + timedelta(minutes=EXTERNAL_CHECK_INTERVAL) < datetime.now():
        last_external_check = datetime.now()
        drop_cache = True
        print('CACHE EXPIRED - DROPPING')

    cached_data = {
        "local_time": get_time(),
        "local_date": get_date(),
        "weather": get_weather() if drop_cache else cached_data['weather'],
        "stocks": get_stocks() if drop_cache else cached_data['stocks']
    }
    return cached_data