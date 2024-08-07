import time
import pytz
from datetime import datetime
from colour import COLOR_NAME_TO_RGB as RGB
from rgbmatrix import graphics
from PIL import Image
from suntime import Sun, SunTimeException
from config import LATITUDE, LONGITUDE, TIMEZONE
from .graphics_base import GraphicsBase
from .api import ForecastApi, WeatherApi, TemperApi, HolidayApi

sun = Sun(LATITUDE, LONGITUDE)


class Clock(GraphicsBase):
    VENDOR_DIR = './pirgbsmartclock/vendor/'
    BLACK = graphics.Color(*RGB['black'])
    WHITE = graphics.Color(*RGB['lightgray'])
    RED = graphics.Color(*RGB['red'])
    GREEN = graphics.Color(*RGB['lightseagreen'])
    BLUE = graphics.Color(*RGB['blue'])

    CLOCK_POS = (24, 11)
    DAY_POS = (1, 6)
    MONTH_POS = (1, 14)
    DATE_POS = (14, 14)
    INDOOR_ICON_POS = (0, 17)
    INDOOR_POS = (9, 24)
    OUTDOOR_ICON_POS = (32, 17)
    OUTDOOR_POS = (42, 24)
    HIGH_POS = (42, 31)
    LOW_POS = (52, 31)
    RAIN_LIKELY_POS = (32, 26)

    scroll_pos = 32

    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__(*args, **kwargs)
        self.process()

        self.font_lg = self.load_font(self.VENDOR_DIR + 'fonts/8x13B.bdf')
        self.font_md = self.load_font(self.VENDOR_DIR + 'fonts/6x10.bdf')
        self.font_sm = self.load_font(self.VENDOR_DIR + 'fonts/4x6.bdf')

        self.home = self.load_icon(self.VENDOR_DIR + 'icons/home.png')
        self.humidity = self.load_icon(self.VENDOR_DIR + 'icons/humidity.png', RGB['red'])
        self.umbrella = self.load_icon(self.VENDOR_DIR + 'icons/umbrella_small.png')
        self.w1000 = self.load_icon(self.VENDOR_DIR + 'icons/1000.png', RGB['gold'])
        self.w1000n = self.load_icon(self.VENDOR_DIR + 'icons/1000n.png', RGB['silver'])
        self.w1001 = self.load_icon(self.VENDOR_DIR + 'icons/1001.png', RGB['gray'])
        self.w1100 = self.load_icon(self.VENDOR_DIR + 'icons/1100.png', RGB['gold'], RGB['gray'])
        self.w1100n = self.load_icon(self.VENDOR_DIR + 'icons/1100n.png', RGB['silver'], RGB['gray'])
        self.w2000 = self.load_icon(self.VENDOR_DIR + 'icons/2000.png', RGB['gray'])
        self.w4000 = self.load_icon(self.VENDOR_DIR + 'icons/4000.png')
        self.w5000 = self.load_icon(self.VENDOR_DIR + 'icons/5000.png', RGB['silver'])
        self.w6000 = self.load_icon(self.VENDOR_DIR + 'icons/6000.png', RGB['silver'])
        self.w7000 = self.load_icon(self.VENDOR_DIR + 'icons/7000.png', RGB['red'], RGB['silver'])
        self.w8000 = self.load_icon(self.VENDOR_DIR + 'icons/8000.png', RGB['orange'])
        self.wother = self.load_icon(self.VENDOR_DIR + 'icons/0.png')

    def load_font(self, path):
        font = graphics.Font()
        font.LoadFont(path)
        return font

    def load_icon(self, path, color_white=None, color_blue=None):
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
            return self.w1000 if not is_night else self.w1000n
        elif code == '1001':
            return self.w1001
        elif code.startswith('11'):
            return self.w1100 if not is_night else self.w1100n
        elif code.startswith('2'):
            return self.w2000
        elif code.startswith('4'):
            return self.w4000
        elif code.startswith('5'):
            return self.w5000
        elif code.startswith('6'):
            return self.w6000
        elif code.startswith('7'):
            return self.w7000
        elif code.startswith('8'):
            return self.w8000
        return self.wother

    def run(self, show_clock):
        canvas = self.matrix
        if not show_clock:
            canvas.Clear()
            return

        now = datetime.now()
        temp = TemperApi.fetch()
        weather = WeatherApi.fetch()
        forecast = ForecastApi.fetch()[0] if len(ForecastApi.fetch()) > 0 else {}
        holiday = HolidayApi.fetch()

        ui_time = now.strftime("%l:%M") if now.microsecond > 500000 else now.strftime("%l %M")
        ui_month = now.strftime('%b')
        ui_date = now.strftime('%-d')
        ui_day = now.strftime('%a')
        ui_indoor_temp = f"{round(temp.get('temp') * 1.8 + 32)}°"
        ui_outdoor_temp = f"{weather.get('temp', 0)}°"
        ui_outdoor_code = weather.get('icon')
        ui_high_temp = str(forecast.get('high_temp', 0))
        ui_low_temp = str(forecast.get('low_temp', 0))
        ui_is_rain_likely = forecast.get('rain_likely', False)
        ui_is_high_humidity = weather.get('humidity', 0) > 60

        canvas.Clear()

        # draw text scroll
        if len(holiday) > 0:
            graphics.DrawText(canvas, self.font_sm, self.scroll_pos, 31, self.BLUE, holiday)
            if abs(self.scroll_pos) > len(holiday)*4:
                self.scroll_pos = 32  # reset scroll
            else:
                self.scroll_pos = self.scroll_pos-1
        graphics.DrawText(canvas, self.font_sm, 32, 31, self.BLACK, '████████')

        # draw clock
        graphics.DrawText(canvas, self.font_lg, self.CLOCK_POS[0], self.CLOCK_POS[1], self.BLUE, ui_time)

        # draw date
        graphics.DrawText(canvas, self.font_sm, self.DATE_POS[0], self.DATE_POS[1], self.WHITE, ui_date)

        # draw month
        graphics.DrawText(canvas, self.font_sm, self.MONTH_POS[0], self.MONTH_POS[1], self.WHITE, ui_month)

        # draw day
        graphics.DrawText(canvas, self.font_sm, self.DAY_POS[0], self.DAY_POS[1], self.WHITE, ui_day)

        # draw indoor temp
        graphics.DrawText(canvas, self.font_md, self.INDOOR_POS[0], self.INDOOR_POS[1], self.WHITE, ui_indoor_temp)

        # draw outdoor temp
        graphics.DrawText(canvas, self.font_md, self.OUTDOOR_POS[0], self.OUTDOOR_POS[1], self.WHITE, ui_outdoor_temp)

        # draw high and low temp
        graphics.DrawText(canvas, self.font_sm, self.HIGH_POS[0], self.HIGH_POS[1], self.RED, ui_high_temp)
        graphics.DrawText(canvas, self.font_sm, self.LOW_POS[0], self.LOW_POS[1], self.BLUE, ui_low_temp)

        # draw icons
        canvas.SetImage(self.home, self.INDOOR_ICON_POS[0], self.INDOOR_ICON_POS[1])
        canvas.SetImage(self.get_weather_icon(ui_outdoor_code), self.OUTDOOR_ICON_POS[0], self.OUTDOOR_ICON_POS[1])
        if ui_is_rain_likely:
            canvas.SetImage(self.umbrella, self.RAIN_LIKELY_POS[0], self.RAIN_LIKELY_POS[1])
        elif ui_is_high_humidity:
            canvas.SetImage(self.humidity, self.RAIN_LIKELY_POS[0], self.RAIN_LIKELY_POS[1])
