import time
from datetime import datetime
from colour import COLOR_NAME_TO_RGB as RGB
from rgbmatrix import graphics
from PIL import Image
from .graphics_base import GraphicsBase
from .api import ForecastApi, WeatherApi, TemperApi


class Clock(GraphicsBase):
    VENDOR_DIR = './pirgbsmartclock/vendor/'
    BLACK = graphics.Color(*RGB['black'])
    RED = graphics.Color(*RGB['red'])
    GREEN = graphics.Color(*RGB['lightseagreen'])
    BLUE = graphics.Color(*RGB['blue'])

    CLOCK_POS = (27, 13)
    DAY_POS = (3, 8)
    MONTH_POS = (3, 16)
    DATE_POS = (16, 16)
    INDOOR_ICON_POS = (2, 22)
    INDOOR_POS = (11, 29)
    OUTDOOR_ICON_POS = (34, 22)
    OUTDOOR_POS = (44, 29)
    HIGH_POS = (44, 21)
    LOW_POS = (54, 21)
    
    _show_sec = True

    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__(*args, **kwargs)
        self.process()

        self.font_lg = self.load_font(self.VENDOR_DIR + 'fonts/7x14B.bdf')
        self.font_md = self.load_font(self.VENDOR_DIR + 'fonts/6x10.bdf')
        self.font_sm = self.load_font(self.VENDOR_DIR + 'fonts/4x6.bdf')

        self.home = self.load_icon(self.VENDOR_DIR + 'icons/home.png')
        self.w1000 = self.load_icon(self.VENDOR_DIR + 'icons/1000.png')
        self.w1001 = self.load_icon(self.VENDOR_DIR + 'icons/1001.png')
        self.w1100 = self.load_icon(self.VENDOR_DIR + 'icons/1100.png')
        self.w2000 = self.load_icon(self.VENDOR_DIR + 'icons/2000.png')
        self.w4000 = self.load_icon(self.VENDOR_DIR + 'icons/4000.png')
        self.w5000 = self.load_icon(self.VENDOR_DIR + 'icons/5000.png')
        self.w6000 = self.load_icon(self.VENDOR_DIR + 'icons/6000.png')
        self.w7000 = self.load_icon(self.VENDOR_DIR + 'icons/7000.png')
        self.w8000 = self.load_icon(self.VENDOR_DIR + 'icons/8000.png')

    def load_font(self, path):
        font = graphics.Font()
        font.LoadFont(path)
        return font

    def load_icon(self, path, recolor=None):
        image = Image.open(path)
        image = image.convert('RGB')
        if recolor is None:
            recolor = RGB['blue']

        width, height = image.size
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                pixel_color = pixels[x,y]
                if pixel_color[0] > 250 and pixel_color[1] > 250  and pixel_color[2] > 250:
                    pixels[x, y] = recolor
        return image

    def get_weather_icon(self, code):
        code = str(code)
        if code == '1000':
            return self.w1000
        elif code == '1001':
            return self.w1001
        elif code == '1100':
            return self.w1100
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
        return self.w1000

    def run(self, show_clock):
        now = datetime.now()
        current_time = now.strftime("%l:%M") if self._show_sec else now.strftime("%l %M")
        current_month = now.strftime('%b')
        current_date = now.strftime('%-d')
        current_day = now.strftime('%a')
        indoor_temp = f"{round(TemperApi.fetch().get('temp') * 1.8 + 32)}°"
        outdoor_temp = f"{WeatherApi.fetch().get('temp',0)}°"
        outdoor_code = WeatherApi.fetch().get('icon')
        high_temp = str(ForecastApi.fetch()[0].get('high_temp', 0))
        low_temp = str(ForecastApi.fetch()[0].get('low_temp', 0))

        canvas = self.matrix
        canvas.Clear()

        if show_clock:
            # draw clock
            graphics.DrawText(canvas, self.font_lg, self.CLOCK_POS[0], self.CLOCK_POS[1], self.BLUE, current_time)
            self._show_sec = not self._show_sec
            
            # draw date
            graphics.DrawText(canvas, self.font_sm, self.DATE_POS[0], self.DATE_POS[1], self.GREEN, current_date)

            # draw month
            graphics.DrawText(canvas, self.font_sm, self.MONTH_POS[0], self.MONTH_POS[1], self.GREEN, current_month)

            # draw day
            graphics.DrawText(canvas, self.font_sm, self.DAY_POS[0], self.DAY_POS[1], self.GREEN, current_day)
            
            # draw indoor temp
            graphics.DrawText(canvas, self.font_md, self.INDOOR_POS[0], self.INDOOR_POS[1], self.GREEN, indoor_temp)

            # draw outdoor temp
            graphics.DrawText(canvas, self.font_md, self.OUTDOOR_POS[0], self.OUTDOOR_POS[1], self.GREEN, outdoor_temp)

            # draw high and low temp
            graphics.DrawText(canvas, self.font_sm, self.HIGH_POS[0], self.HIGH_POS[1], self.RED, high_temp)
            graphics.DrawText(canvas, self.font_sm, self.LOW_POS[0], self.LOW_POS[1], self.BLUE, low_temp)

            # draw icons
            canvas.SetImage(self.home, self.INDOOR_ICON_POS[0], self.INDOOR_ICON_POS[1])
            canvas.SetImage(self.get_weather_icon(outdoor_code), self.OUTDOOR_ICON_POS[0], self.OUTDOOR_ICON_POS[1])

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
