from datetime import datetime
from .graphics_base import GraphicsBase
from rgbmatrix import graphics
import time


class GraphicsTest(GraphicsBase):
    CLOCK_POS = (4, 19)
    _prev_time = None


    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.font = graphics.Font()
        self.font.LoadFont('./pirgbsmartclock/vendor/fonts/7x13.bdf')

    def run(self, show_clock):
        canvas = self.matrix
        now = datetime.now()
        current_time = now.strftime("%l:%M:%S")
        print(current_time)

        blue = graphics.Color(0, 0, 255)
        black = graphics.Color(0, 0, 0)
        if self._prev_time is not None:
            graphics.DrawText(canvas, self.font, self.CLOCK_POS[0], self.CLOCK_POS[1], black, self._prev_time)
        if show_clock:
            graphics.DrawText(canvas, self.font, self.CLOCK_POS[0], self.CLOCK_POS[1], blue, current_time)
        self._prev_time = current_time


# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
