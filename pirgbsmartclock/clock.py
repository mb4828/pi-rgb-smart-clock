import time
from datetime import datetime
from colour import COLOR_NAME_TO_RGB as RGB
from rgbmatrix import graphics
from PIL import Image
from .graphics_base import GraphicsBase
from .api import WeatherApi, TemperApi


class Clock(GraphicsBase):
    VENDOR_DIR = './pirgbsmartclock/vendor/'
    BLACK = graphics.Color(*RGB['black'])
    COLOR1 = graphics.Color(*RGB['blue'])
    COLOR2 = graphics.Color(*RGB['lightseagreen'])

    CLOCK_POS = (27, 13)
    MONTH_POS = (3, 16)
    DATE_POS = (16, 16)
    DAY_POS = (3, 8)
    INDOOR_POS = (11, 29)
    OUTDOOR_POS = (44, 29)
    
    _show_sec = True

    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__(*args, **kwargs)
        self.process()

        self.font1 = graphics.Font()
        self.font1.LoadFont(self.VENDOR_DIR + 'fonts/7x14B.bdf')
        self.font2 = graphics.Font()
        self.font2.LoadFont(self.VENDOR_DIR + 'fonts/4x6.bdf')
        self.font3 = graphics.Font()
        self.font3.LoadFont(self.VENDOR_DIR + 'fonts/6x10.bdf')

        self.home = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/home.png'))
        self.w1000 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/1000.png'))
        self.w1001 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/1001.png'))
        self.w1100 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/1100.png'))
        self.w2000 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/2000.png'))
        self.w4000 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/4000.png'))
        self.w5000 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/5000.png'))
        self.w6000 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/6000.png'))
        self.w7000 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/7000.png'))
        self.w8000 = self.recolor_icon(Image.open(self.VENDOR_DIR + 'icons/8000.png'))

    def recolor_icon(self, image, recolor=None):
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
        outdoor_temp = f"{round(WeatherApi.fetch().get('temp',0))}°"
        outdoor_code = WeatherApi.fetch().get('icon')
        indoor_temp = f"{round(TemperApi.fetch().get('temp') * 1.8 + 32)}°"

        canvas = self.matrix
        canvas.Clear()

        if show_clock:
            # draw clock
            graphics.DrawText(canvas, self.font1, self.CLOCK_POS[0], self.CLOCK_POS[1], self.COLOR1, current_time)
            self._show_sec = not self._show_sec

            # draw month
            graphics.DrawText(canvas, self.font2, self.MONTH_POS[0], self.MONTH_POS[1], self.COLOR2, current_month)

            # draw date
            graphics.DrawText(canvas, self.font2, self.DATE_POS[0], self.DATE_POS[1], self.COLOR2, current_date)

            # draw day
            graphics.DrawText(canvas, self.font2, self.DAY_POS[0], self.DAY_POS[1], self.COLOR2, current_day)

            # draw outdoor conditions
            graphics.DrawText(canvas, self.font3, self.OUTDOOR_POS[0], self.OUTDOOR_POS[1], self.COLOR2, outdoor_temp)

            # draw indoor conditions
            graphics.DrawText(canvas, self.font3, self.INDOOR_POS[0], self.INDOOR_POS[1], self.COLOR2, indoor_temp)

            # draw icons
            canvas.SetImage(self.home, 2, 22)
            canvas.SetImage(self.get_weather_icon(outdoor_code), 34, 22)

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
