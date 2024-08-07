from colour import COLOR_NAME_TO_RGB as RGB
from PIL import Image
from rgbmatrix import graphics
from suntime import Sun, SunTimeException


def load_font(path):
    font = graphics.Font()
    font.LoadFont(path)
    return font


def load_icon(path, color_white=None, color_blue=None):
    image = Image.open(path)
    image = image.convert('RGB')

    if color_white is None:
        color_white = RGB['blue']
    if color_blue is None:
        color_blue = RGB['blue']

    width, height = image.size
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            pixel_color = pixels[x, y]
            if pixel_color[0] > 250 and pixel_color[1] > 250 and pixel_color[2] > 250:
                pixels[x, y] = color_white
            if pixel_color[0] < 5 and pixel_color[1] < 5 and pixel_color[2] > 250:
                pixels[x, y] = color_blue
    return image
