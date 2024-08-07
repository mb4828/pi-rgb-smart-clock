from colour import COLOR_NAME_TO_RGB as RGB
from pirgbsmartclock.utils.utils import load_font, load_icon
from rgbmatrix import graphics

VENDOR_DIR = './vendor/'

BLACK = graphics.Color(*RGB['black'])
WHITE = graphics.Color(*RGB['lightgray'])
RED = graphics.Color(*RGB['red'])
GREEN = graphics.Color(*RGB['green'])
BLUE = graphics.Color(*RGB['blue'])

FONT_LG = load_font(VENDOR_DIR + 'fonts/8x13B.bdf')
FONT_MD = load_font(VENDOR_DIR + 'fonts/5x7.bdf')
FONT_SM = load_font(VENDOR_DIR + 'fonts/4x6.bdf')
