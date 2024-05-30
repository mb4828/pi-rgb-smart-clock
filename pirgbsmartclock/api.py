"""
Fetches data from various APIs
"""

import asyncio
from datetime import datetime, timedelta
import logging
from bs4 import BeautifulSoup
from pirgbsmartclock.vendor.temper import USBRead, USBList
import requests
import holidays
import csv

from config import TOMORROWIO_API_KEY, TOMORROWIO_LOCATION


class Api:
    FETCH_INTEVAL = 10  # new data every 10 minutes
    _next_fetch = datetime(1990, 1, 1)
    _cached_data = {}

    @classmethod
    async def async_get_data(cls):
        if cls._is_cache_expired():
            await cls._fetch()
            cls._reset_next_fetch()
        return cls._cached_data

    @classmethod
    def get_data(cls):
        if cls._is_cache_expired():
            asyncio.run(cls._fetch())
            cls._reset_next_fetch()
        return cls._cached_data

    @classmethod
    async def _fetch(cls):
        # override this method
        cls._cached_data({})

    @classmethod
    def _is_cache_expired(cls):
        return cls._next_fetch <= datetime.now()

    @classmethod
    def _reset_next_fetch(cls):
        cls._next_fetch = datetime.now() + timedelta(minutes=cls.FETCH_INTEVAL)


class WeatherApi(Api):
    @classmethod
    async def _fetch(cls):
        try:
            request = requests.get(
                'https://api.tomorrow.io/v4/weather/realtime',
                params={
                    "location": TOMORROWIO_LOCATION,
                    "units": "imperial",
                    "apikey": TOMORROWIO_API_KEY
                }
            )
            request.raise_for_status()
            data = request.json()["data"]["values"]
            cls._cached_data = {
                'temp': round(data.get('temperature', 0)),
                'humidity': round(data.get('humidity', 0)),
                'icon': data.get('weatherCode')
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed. Error: {e}")
            cls._cached_data = {}
        cls._reset_next_fetch()


class ForecastApi(Api):
    @classmethod
    async def _fetch(cls):
        results = []
        try:
            request = requests.get(
                'https://api.tomorrow.io/v4/weather/forecast',
                params={
                    "timesteps": '1d',
                    "location": TOMORROWIO_LOCATION,
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
                    'rain_likely': d['values'].get('precipitationProbabilityMax', 0) > 25,
                    'icon': d['values'].get('weatherCodeMax', 0),
                })
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed. Error: {e}")
        cls._cached_data = results
        cls._reset_next_fetch()


class StockApi(Api):
    FETCH_INTEVAL = 0.25  # every 15 seconds

    @classmethod
    async def _fetch(cls):
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
        cls._cached_data = results
        cls._reset_next_fetch()


class TemperApi(Api):
    FETCH_INTEVAL = 2  # every 2 minutes

    @classmethod
    async def _fetch(cls):
        try:
            device_list = USBList().get_usb_devices()
            device = device_list.get(next(k for k, v in device_list.items() if v.get('product') == 'TEMPer2'))

            usbread = USBRead(device.get('devices')[-1]).read()
            cls._cached_data = {'temp': usbread['external temperature']}

        except Exception as e:
            logging.error(f'Failed to fetch Temper data. Error: {e}')
            cls._cached_data = {'temp': -1}
        cls._reset_next_fetch()


class HolidayApi(Api):
    HOLIDAYS = holidays.US() + holidays.NYSE()

    try:
        custom_holidays = {}
        with open('custom_holidays.csv') as f:
            year = datetime.now().strftime('%Y-')
            reader = csv.reader(f)
            for row in reader:
                custom_holidays[year + row[0]] = row[1]
        HOLIDAYS.append(custom_holidays)
    except Exception as e:
        logging.error(f'Failed to load custom_holidays.csv\n{e}', exc_info=True)

    @classmethod
    async def _fetch(cls):
        today = datetime.now().strftime('%Y-%m-%d')
        if today in HolidayApi.HOLIDAYS:
            hol = HolidayApi.HOLIDAYS.get(today)
            if 'C:' in hol:
                cls._cached_data = hol[2:]
            elif 'Christmas' in hol:
                cls._cached_data = f'Merry {hol}'
            cls._cached_data = f'Happy {hol}'
        else:
            cls._cached_data = ''
        cls._reset_next_fetch()


def get_time():
    return datetime.now().strftime('%-I:%M:%S %p')


def get_date():
    return datetime.now().strftime('%b %-d')
