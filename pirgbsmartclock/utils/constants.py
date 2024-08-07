from colour import COLOR_NAME_TO_RGB as RGB
from pirgbsmartclock.utils.utils import load_font, load_icon
from rgbmatrix import graphics

VENDOR_DIR = './vendor/'

BLACK = graphics.Color(*RGB['black'])
WHITE = graphics.Color(*RGB['lightgray'])
RED = graphics.Color(*RGB['red'])
GREEN = graphics.Color(*RGB['lightseagreen'])
BLUE = graphics.Color(*RGB['blue'])

FONT_LG = load_font(VENDOR_DIR + 'fonts/8x13B.bdf')
FONT_MD = load_font(VENDOR_DIR + 'fonts/5x7.bdf')
FONT_SM = load_font(VENDOR_DIR + 'fonts/4x6.bdf')

ICON_HOME = load_icon(VENDOR_DIR + 'icons/home.png')
ICON_HUMIDITY = load_icon(VENDOR_DIR + 'icons/humidity.png', RGB['red'])
ICON_UMBRELLA = load_icon(VENDOR_DIR + 'icons/umbrella_small.png')
ICON_W1000 = load_icon(VENDOR_DIR + 'icons/1000.png', RGB['gold'])
ICON_W1000N = load_icon(VENDOR_DIR + 'icons/1000n.png', RGB['silver'])
ICON_W1001 = load_icon(VENDOR_DIR + 'icons/1001.png', RGB['gray'])
ICON_W1100 = load_icon(VENDOR_DIR + 'icons/1100.png', RGB['gold'], RGB['gray'])
ICON_W1100N = load_icon(VENDOR_DIR + 'icons/1100n.png', RGB['silver'], RGB['gray'])
ICON_W2000 = load_icon(VENDOR_DIR + 'icons/2000.png', RGB['gray'])
ICON_W4000 = load_icon(VENDOR_DIR + 'icons/4000.png')
ICON_W5000 = load_icon(VENDOR_DIR + 'icons/5000.png', RGB['silver'])
ICON_W6000 = load_icon(VENDOR_DIR + 'icons/6000.png', RGB['silver'])
ICON_W7000 = load_icon(VENDOR_DIR + 'icons/7000.png', RGB['red'], RGB['silver'])
ICON_W8000 = load_icon(VENDOR_DIR + 'icons/8000.png', RGB['orange'])
ICON_WOTHER = load_icon(VENDOR_DIR + 'icons/1000.png')
