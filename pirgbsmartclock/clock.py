from datetime import datetime
from pirgbsmartclock.api import get_all
from vendor.rgbmatrix import graphics
from vendor import fonts
from colour import Color

CLOCK_FONT = fonts.regular
CLOCK_COLOR = graphics.Color(Color('green').get_rgb())
CLOCK_POSITION = (1, 8)

_canvas = None
_last_time = None


def draw_clock():
    data = get_all()
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    if _last_time != current_time:
        graphics.DrawText(_canvas, CLOCK_FONT, CLOCK_POSITION[0], CLOCK_POSITION[1], CLOCK_COLOR, current_time)
