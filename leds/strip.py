from rpi_ws281x import PixelStrip

from leds.color import Color, Representation


class LEDStrip:
    def __init__(self, pin: int, length: int) -> None:
        self.pin = pin
        self.length = length

        self.strip = PixelStrip(self.length, self.pin)

        self.strip.begin()

    def set_color(self, i: int, color: Color) -> None:
        self.strip.setPixelColor(i, color.get_value())

    def set_all(self, color: Color) -> None:
        for i in range(self.length):
            self.strip.setPixelColor(i, color.get_value())

    def get_color(self, i: int, representation: Representation) -> Color:
        rgb_val = self.strip.getPixelColor(i)
        rgb = (rgb_val >> 16) & 0xFF, (rgb_val >> 8) & 0xFF, rgb_val & 0xFF
        if representation == Representation.RGB:
            return Color.from_rgb(*rgb)
        elif representation == Representation.HSV:
            return Color.from_hsv(*self.rgb_to_hsv(rgb))
        else:
            raise ValueError("Unknown representation")

    def show(self):
        self.strip.show()

    def suppress(self):
        self.set_all(Color.from_rgb(0, 0, 0))
