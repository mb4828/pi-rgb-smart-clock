from colour import COLOR_NAME_TO_RGB as RGB
from config import LATITUDE, LONGITUDE, TIMEZONE
from datetime import datetime
from pirgbsmartclock.utils.constants import VENDOR_DIR
from pirgbsmartclock.utils.utils import load_icon
import pytz
from suntime import Sun, SunTimeException

ICON_HOME = load_icon(VENDOR_DIR + 'icons/home.png')
ICON_HUMIDITY = load_icon(VENDOR_DIR + 'icons/humidity.png', RGB['red'])
ICON_UMBRELLA = load_icon(VENDOR_DIR + 'icons/umbrella_small.png')
ICON_W1000 = load_icon(VENDOR_DIR + 'icons/1000.png', RGB['gold'])
ICON_W1000N = load_icon(VENDOR_DIR + 'icons/1000n.png', RGB['silver'])
ICON_W1001 = load_icon(VENDOR_DIR + 'icons/1001.png', RGB['gray'])
ICON_W1100 = load_icon(VENDOR_DIR + 'icons/1100.png', RGB['gold'], RGB['gray'])
ICON_W1100N = load_icon(VENDOR_DIR + 'icons/1100n.png', RGB['silver'], RGB['gray'])
ICON_W2000 = load_icon(VENDOR_DIR + 'icons/2000.png', RGB['gray'])
ICON_W4000 = load_icon(VENDOR_DIR + 'icons/4000.png', RGB['gray'])
ICON_W5000 = load_icon(VENDOR_DIR + 'icons/5000.png', RGB['gray'], RGB['silver'])
ICON_W6000 = load_icon(VENDOR_DIR + 'icons/6000.png', RGB['gray'], RGB['silver'])
ICON_W7000 = load_icon(VENDOR_DIR + 'icons/7000.png', RGB['red'], RGB['silver'])
ICON_W8000 = load_icon(VENDOR_DIR + 'icons/8000.png', RGB['orange'])
ICON_WOTHER = load_icon(VENDOR_DIR + 'icons/1000.png')


def get_weather_icon(code):
    sun = Sun(LATITUDE, LONGITUDE)
    code = str(code)
    is_night = False
    try:
        now = datetime.now(pytz.timezone(TIMEZONE)).time()
        sunrise = sun.get_sunrise_time().astimezone(pytz.timezone(TIMEZONE)).time()
        sunset = sun.get_sunset_time().astimezone(pytz.timezone(TIMEZONE)).time()
        is_night = now > sunset or now < sunrise
    except SunTimeExcpetion:
        pass

    if code == '1000':  # Clear
        return ICON_W1000 if not is_night else ICON_W1000N
    elif code == '1001':  # Cloudy
        return ICON_W1001
    elif code.startswith('11'):  # Partly Cloudy
        return ICON_W1100 if not is_night else ICON_W1100N
    elif code.startswith('2'):  # Fog
        return ICON_W2000
    elif code.startswith('4'):  # Rain
        return ICON_W4000
    elif code.startswith('5'):  # Snow
        return ICON_W5000
    elif code.startswith('6'):  # Freezing Rain
        return ICON_W6000
    elif code.startswith('7'):  # Hail
        return ICON_W7000
    elif code.startswith('8'):  # Thunderstorm
        return ICON_W8000
    return ICON_WOTHER
