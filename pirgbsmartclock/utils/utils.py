from colour import COLOR_NAME_TO_RGB as RGB
from config import LATITUDE, LONGITUDE, TIMEZONE
from datetime import datetime
import pytz
from PIL import Image
from pirgbsmartclock.utils.constants import ICON_W1000, ICON_W1000N, ICON_W1001, ICON_W1100, ICON_W1100N, ICON_W2000, ICON_W4000, ICON_W5000, ICON_W6000, ICON_W7000, ICON_W8000, ICON_WOTHER
from rgbmatrix import graphics
from suntime import Sun, SunTimeException


def load_font(path):
    font = graphics.Font()
    font.LoadFont(path)
    return font


def load_icon(path, color_white=None, color_blue=None):
    image = Image.open(path)
    image = image.convert('RGB')

    if color_white is None:
        color_white = RGB['blue']
    if color_blue is None:
        color_blue = RGB['blue']

    width, height = image.size
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            pixel_color = pixels[x, y]
            if pixel_color[0] > 250 and pixel_color[1] > 250 and pixel_color[2] > 250:
                pixels[x, y] = color_white
            if pixel_color[0] < 5 and pixel_color[1] < 5 and pixel_color[2] > 250:
                pixels[x, y] = color_blue
    return image


def get_weather_icon(self, code):
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

    if code == '1000':
        return ICON_W1000 if not is_night else ICON_W1000N
    elif code == '1001':
        return ICON_W1001
    elif code.startswith('11'):
        return ICON_W1100 if not is_night else ICON_W1100N
    elif code.startswith('2'):
        return ICON_W2000
    elif code.startswith('4'):
        return ICON_W4000
    elif code.startswith('5'):
        return ICON_W5000
    elif code.startswith('6'):
        return ICON_W6000
    elif code.startswith('7'):
        return ICON_W7000
    elif code.startswith('8'):
        return ICON_W8000
    return ICON_WOTHER
