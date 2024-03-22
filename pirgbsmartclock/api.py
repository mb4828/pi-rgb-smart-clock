"""
Fetches data from various APIs
"""

from datetime import datetime, timedelta
import logging
from bs4 import BeautifulSoup
from pirgbsmartclock.vendor.temper import USBRead, USBList
import requests

from config import TOMORROWIO_API_KEY, TOMORROWIO_ZIP_CODE


class Api:
    FETCH_INTEVAL = 10  # new data every 10 minutes
    next_fetch = datetime(1990, 1, 1)
    cached_data = {}

    @staticmethod
    def _fetch():
        pass  # override this method

    @classmethod
    def fetch(cls):
        if cls.is_cache_expired():
            cls.cached_data = cls._fetch()
            cls.next_fetch = datetime.now() + timedelta(minutes=cls.FETCH_INTEVAL)
        return cls.cached_data

    @classmethod
    def is_cache_expired(cls):
        return cls.next_fetch <= datetime.now()


class WeatherApi(Api):
    def _fetch():
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
            logging.error(f"Request failed. Error: {e}")
            return {}


class ForecastApi(Api):
    def _fetch():
        results = []
        try:
            request = requests.get(
                'https://api.tomorrow.io/v4/weather/forecast',
                params={
                    "timesteps": '1d',
                    "location": TOMORROWIO_ZIP_CODE,
                    "units": "imperial",
                    "apikey": TOMORROWIO_API_KEY
                }
            )
            request.raise_for_status()
            data = request.json()["timelines"]["daily"]
            for d in data:
                results.append({
                    'day_name': datetime.strptime(d.get('time'), '%Y-%m-%dT%H:%M:%SZ').strftime('%a'),
                    'low_temp': round(d['values'].get('temperatureMin', 0)),
                    'high_temp': round(d['values'].get('temperatureMax', 0)),
                    'humidity': round(d['values'].get('humidityAvg', 0)),
                    'icon': d['values'].get('weatherCodeMax', 0),
                })
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed. Error: {e}")
        return results


class StockApi(Api):
    FETCH_INTEVAL = 0.25  # every 15 seconds

    def _fetch():
        index_list = {
            '^GSPC': 'S&P',
            '^DJI': 'Dow',
            '^IXIC': 'Nasdaq',
            '^FTSE': 'FTSE 100',
            '^N225': 'Nikkei 225',
            '^VIX': 'Vix',
        }
        results = []
        try:
            request = requests.get(f'https://finance.yahoo.com/world-indices/')
            request.raise_for_status()
            soup = BeautifulSoup(request.text, 'html.parser')
            for idx in index_list:
                price = soup.find(attrs={'data-symbol': idx, 'data-field': 'regularMarketPrice'})
                pts = soup.find(attrs={'data-symbol': idx, 'data-field': 'regularMarketChange'})
                pct = soup.find(attrs={'data-symbol': idx, 'data-field': 'regularMarketChangePercent'})
                if price and pts and pct:
                    results.append({
                        'name': index_list[idx],
                        'price': '{0:.2f}'.format(float(price['value'])),
                        'points': '{0:+.2f}'.format(float(pts['value'])),
                        'percent': '{0:+.2f}%'.format(float(pct['value'])),
                        'direction': 'up' if float(pts['value']) > 0 else 'down'
                    })
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed. Error: {e}")
        return results


class TemperApi(Api):
    FETCH_INTEVAL = 0.1  # every 10 seconds

    def _fetch():
        try:
            device_list = USBList().get_usb_devices()
            device = device_list.get(next(k for k, v in device_list.items() if v.get('product') == 'TEMPer2'))

            usbread = USBRead(device.get('devices')[-1]).read()
            return {'temp': usbread['external temperature']}

        except Exception as e:
            logging.error(f'Failed to fetch Temper data. Error: {e}')
            return {'temp': -1}


def get_time():
    return datetime.now().strftime('%-I:%M:%S %p')


def get_date():
    return datetime.now().strftime('%b %-d')


def get_all():
    return {
        "local_time": get_time(),
        "local_date": get_date(),
        "weather": WeatherApi.fetch(),
        "forecast": ForecastApi.fetch(),
        # "stocks": StockApi.fetch(),
        "temper": TemperApi.fetch()
    }
