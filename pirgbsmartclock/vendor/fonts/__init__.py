import os
from rgbmatrix import graphics

# Fonts
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
extrasmall = graphics.Font()
small = graphics.Font()
regular = graphics.Font()
large = graphics.Font()
large_bold = graphics.Font()
extrasmall.LoadFont(f"{DIR_PATH}/4x6.bdf")
small.LoadFont(f"{DIR_PATH}/5x8.bdf")
regular.LoadFont(f"{DIR_PATH}/6x12.bdf")
large.LoadFont(f"{DIR_PATH}/8x13.bdf")
large_bold.LoadFont(f"{DIR_PATH}/8x13B.bdf")
