from datetime import datetime
from colour import COLOR_NAME_TO_RGB as RGB
from pirgbsmartclock.utils.constants import BLUE, FONT_LG, FONT_MD, FONT_SM, ICON_HOME, ICON_HUMIDITY, ICON_UMBRELLA, RED, WHITE
from pirgbsmartclock.utils.utils import get_weather_icon
from rgbmatrix import graphics
from config import LATITUDE, LONGITUDE
from .utils.graphics_base import GraphicsBase
from .api import ForecastApi, WeatherApi, TemperApi, HolidayApi


class Clock(GraphicsBase):
    CLOCK_POS = (24, 11)
    DAY_POS = (1, 6)
    MONTH_POS = (1, 13)
    DATE_POS = (14, 13)
    INDOOR_ICON_POS = (0, 16)
    INDOOR_POS = (9, 22)
    OUTDOOR_ICON_POS = (22, 16)
    OUTDOOR_POS = (32, 22)
    HIGH_POS = (45, 22)
    LOW_POS = (55, 22)
    RAIN_LIKELY_POS = (15, 1)
    scroll_pos = 64

    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__(*args, **kwargs)
        self.process()

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
        ui_indoor_temp = f"{round(temp.get('temp') * 1.8 + 32)}"
        ui_outdoor_temp = f"{weather.get('temp', 0)}"
        ui_outdoor_code = weather.get('icon')
        ui_high_temp = str(forecast.get('high_temp', 0))
        ui_low_temp = str(forecast.get('low_temp', 0))
        ui_is_rain_likely = forecast.get('rain_likely', False)
        ui_is_high_humidity = weather.get('humidity', 0) > 60

        canvas.Clear()

        # draw text scroll
        if len(holiday) > 0:
            graphics.DrawText(canvas, FONT_SM, self.scroll_pos, 30, BLUE, holiday)
            if self.scroll_pos + len(holiday)*4 <= 0:
                self.scroll_pos = 64  # reset scroll
            else:
                self.scroll_pos = self.scroll_pos-1

        # draw clock
        graphics.DrawText(canvas, FONT_LG, self.CLOCK_POS[0], self.CLOCK_POS[1], BLUE, ui_time)

        # draw date
        graphics.DrawText(canvas, FONT_SM, self.DATE_POS[0], self.DATE_POS[1], WHITE, ui_date)

        # draw month
        graphics.DrawText(canvas, FONT_SM, self.MONTH_POS[0], self.MONTH_POS[1], WHITE, ui_month)

        # draw day
        graphics.DrawText(canvas, FONT_SM, self.DAY_POS[0], self.DAY_POS[1], WHITE, ui_day)

        # draw indoor temp
        graphics.DrawText(canvas, FONT_MD, self.INDOOR_POS[0], self.INDOOR_POS[1], WHITE, ui_indoor_temp)

        # draw outdoor temp
        graphics.DrawText(canvas, FONT_MD, self.OUTDOOR_POS[0], self.OUTDOOR_POS[1], WHITE, ui_outdoor_temp)

        # draw high and low temp
        graphics.DrawText(canvas, FONT_SM, self.HIGH_POS[0], self.HIGH_POS[1], RED, ui_high_temp)
        graphics.DrawText(canvas, FONT_SM, self.LOW_POS[0], self.LOW_POS[1], BLUE, ui_low_temp)

        # draw icons
        canvas.SetImage(ICON_HOME, self.INDOOR_ICON_POS[0], self.INDOOR_ICON_POS[1])
        canvas.SetImage(get_weather_icon(ui_outdoor_code), self.OUTDOOR_ICON_POS[0], self.OUTDOOR_ICON_POS[1])
        if ui_is_rain_likely:
            canvas.SetImage(ICON_UMBRELLA, self.RAIN_LIKELY_POS[0], self.RAIN_LIKELY_POS[1])
        elif ui_is_high_humidity:
            canvas.SetImage(ICON_HUMIDITY, self.RAIN_LIKELY_POS[0], self.RAIN_LIKELY_POS[1])
