from datetime import datetime
from pirgbsmartclock.utils.constants import BLUE, FONT_LG, FONT_MD, FONT_SM, GREEN, RED, WHITE
from pirgbsmartclock.utils.weather_utils import ICON_HOME, ICON_HUMIDITY, ICON_UMBRELLA, get_weather_icon
from rgbmatrix import graphics
from .utils.graphics_base import GraphicsBase
from .api import ForecastApi, StockApi, WeatherApi, TemperApi, HolidayApi


class Clock(GraphicsBase):
    CLOCK_POS = (24, 11)
    DAY_POS = (1, 6)
    MONTH_POS = (1, 14)
    DATE_POS = (14, 14)
    INDOOR_ICON_POS = (0, 25)
    INDOOR_POS = (9, 31)
    OUTDOOR_ICON_POS = (22, 25)
    OUTDOOR_POS = (32, 31)
    HIGH_POS = (45, 31)
    LOW_POS = (55, 31)
    ALERT_POS = (15, 1)
    TICKER_Y_POS = 22
    ticker_x_pos = 0

    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__(*args, **kwargs)
        self.process()

    def draw_ticker(self, canvas, stocks, holiday):
        # build the list of ticker elements
        ticker_els = []
        if holiday:
            ticker_els.append((f'| {holiday} |', WHITE))
        for stock in stocks:
            ticker_els.append((stock['name'], WHITE))
            ticker_els.append((f'{stock["points"]} {stock["percent"]}', GREEN if stock['direction'] == 'up' else RED))

        # draw each element in the ticker twice to allow continuous scrolling and compute the ticker width
        draw_pos = self.ticker_x_pos
        ticker_width = 0
        for i in range(2):
            for el in ticker_els:
                (text, color) = el
                graphics.DrawText(canvas, FONT_SM, draw_pos, self.TICKER_Y_POS, color, text)
                text_width = (len(text)+1)*4  # (text length + space) * character width (4)
                if i == 0:
                    ticker_width += text_width
                draw_pos += text_width

        # slide the ticker by decrementing the x position
        self.ticker_x_pos = self.ticker_x_pos - 1
        if self.ticker_x_pos + ticker_width <= 0:
            self.ticker_x_pos = 0  # reset position once the first ticker has scrolled off the screen

    def run(self, show_clock):
        canvas = self.matrix
        if not show_clock:
            canvas.Clear()
            return

        now = datetime.now()
        temp = TemperApi.fetch()
        weather = WeatherApi.fetch()
        forecast = ForecastApi.fetch()[0] if len(ForecastApi.fetch()) > 0 else {}
        stocks = []  # StockApi.fetch()
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
        ui_is_high_humidity = weather.get('dewpoint', 0) > 60

        canvas.Clear()

        # draw clock
        graphics.DrawText(canvas, FONT_LG, self.CLOCK_POS[0], self.CLOCK_POS[1], BLUE, ui_time)

        # draw day of the week, month, and day
        graphics.DrawText(canvas, FONT_SM, self.DAY_POS[0], self.DAY_POS[1], WHITE, ui_day)
        graphics.DrawText(canvas, FONT_SM, self.MONTH_POS[0], self.MONTH_POS[1], WHITE, ui_month)
        graphics.DrawText(canvas, FONT_SM, self.DATE_POS[0], self.DATE_POS[1], WHITE, ui_date)

        # draw indoor temp
        canvas.SetImage(ICON_HOME, self.INDOOR_ICON_POS[0], self.INDOOR_ICON_POS[1])
        graphics.DrawText(canvas, FONT_MD, self.INDOOR_POS[0], self.INDOOR_POS[1], WHITE, ui_indoor_temp)

        # draw outdoor temp
        canvas.SetImage(get_weather_icon(ui_outdoor_code), self.OUTDOOR_ICON_POS[0], self.OUTDOOR_ICON_POS[1])
        graphics.DrawText(canvas, FONT_MD, self.OUTDOOR_POS[0], self.OUTDOOR_POS[1], WHITE, ui_outdoor_temp)

        # draw high and low temp
        graphics.DrawText(canvas, FONT_SM, self.HIGH_POS[0], self.HIGH_POS[1], RED, ui_high_temp)
        graphics.DrawText(canvas, FONT_SM, self.LOW_POS[0], self.LOW_POS[1], BLUE, ui_low_temp)

        # draw alert icons
        if ui_is_rain_likely:
            canvas.SetImage(ICON_UMBRELLA, self.ALERT_POS[0], self.ALERT_POS[1])
        elif ui_is_high_humidity:
            canvas.SetImage(ICON_HUMIDITY, self.ALERT_POS[0], self.ALERT_POS[1])

        # draw ticker
        self.draw_ticker(canvas, stocks, holiday)
