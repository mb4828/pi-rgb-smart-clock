from datetime import datetime
from colour import COLOR_NAME_TO_RGB as RGB
from .graphics_base import GraphicsBase
from .api import WeatherApi, TemperApi
from rgbmatrix import graphics
import time


class GraphicsTest(GraphicsBase):
    BLACK = graphics.Color(*RGB['black'])
    COLOR1 = graphics.Color(*RGB['blue'])
    COLOR2 = graphics.Color(*RGB['lightseagreen'])

    CLOCK_POS = (3, 13)
    _prev_time = None
    _show_sec = True

    DATE_POS = (42, 16)
    _prev_date = None

    DAY_POS = (42, 8)
    _prev_day = None

    OUTDOOR_POS = (3, 27)
    _prev_outdoor = None

    INDOOR_POS = (35, 27)
    _prev_indoor = None

    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.font1 = graphics.Font()
        self.font1.LoadFont('./pirgbsmartclock/vendor/fonts/7x14B.bdf')
        self.font2 = graphics.Font()
        self.font2.LoadFont('./pirgbsmartclock/vendor/fonts/4x6.bdf')
        self.font3 = graphics.Font()
        self.font3.LoadFont('./pirgbsmartclock/vendor/fonts/6x10.bdf')

    def run(self, show_clock):
        canvas = self.matrix
        now = datetime.now()
        current_time = now.strftime("%l:%M") if self._show_sec else now.strftime("%l %M")
        current_date = now.strftime('%-m/%-d')
        current_day = now.strftime('%a')
        outdoor_temp = f"O-{round(WeatherApi().fetch().get('temp',0))}°"
        indoor_temp = f"I-{round(TemperApi().fetch()['temp'] * 1.8 + 32)}°"

        # draw clock
        if self._prev_time is not None:
            graphics.DrawText(canvas, self.font1, self.CLOCK_POS[0], self.CLOCK_POS[1], self.BLACK, self._prev_time)
        if show_clock:
            graphics.DrawText(canvas, self.font1, self.CLOCK_POS[0], self.CLOCK_POS[1], self.COLOR1, current_time)
        self._prev_time = current_time
        self._show_sec = not self._show_sec

        # draw date
        if self._prev_date is not None:
            graphics.DrawText(canvas, self.font2, self.DATE_POS[0], self.DATE_POS[1], self.BLACK, self._prev_date)
        if show_clock:
            graphics.DrawText(canvas, self.font2, self.DATE_POS[0], self.DATE_POS[1], self.COLOR2, current_date)
        self._prev_date = current_date

        # draw day
        if self._prev_day is not None:
            graphics.DrawText(canvas, self.font2, self.DAY_POS[0], self.DAY_POS[1], self.BLACK, self._prev_day)
        if show_clock:
            graphics.DrawText(canvas, self.font2, self.DAY_POS[0], self.DAY_POS[1], self.COLOR2, current_day)
        self._prev_day = current_day

        # draw outdoor conditions
        if self._prev_outdoor is not None:
            graphics.DrawText(canvas, self.font3, self.OUTDOOR_POS[0], self.OUTDOOR_POS[1], self.BLACK, self._prev_outdoor)
        if show_clock:
            graphics.DrawText(canvas, self.font3, self.OUTDOOR_POS[0], self.OUTDOOR_POS[1], self.COLOR2, outdoor_temp)
        self._prev_outdoor = outdoor_temp

        # draw indoor conditions
        if self._prev_indoor is not None:
            graphics.DrawText(canvas, self.font3, self.INDOOR_POS[0], self.INDOOR_POS[1], self.BLACK, self._prev_indoor)
        if show_clock:
            graphics.DrawText(canvas, self.font3, self.INDOOR_POS[0], self.INDOOR_POS[1], self.COLOR2, indoor_temp)
        self._prev_indoor = indoor_temp

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
