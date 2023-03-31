from rpi_ws281x import PixelStrip

from leds.color import Color, Representation


class LEDStrip:
    def __init__(self, pin: int, length: int) -> None:
        """
        :param pin: The GPIO pin the strip is connected to.
        supported pins include 10, 12, 18, 21, 40

        :param length: The number of LEDs in the strip.
        """
        self.pin = pin
        self.length = length

        self.strip = PixelStrip(self.length, self.pin)

        self.strip.begin()

    def set_color(self, i: int, color: Color) -> None:
        """
        Sets the color of a single LED.

        :param i: The index of the LED.
        :param color: The color to set.
        """
        self.strip.setPixelColor(i, color.get_RGB_code())

    def set_all(self, color: Color) -> None:
        """
        Sets the color of all LEDs.

        :param color: The color to set.
        """
        for i in range(self.length):
            self.strip.setPixelColor(i, color.get_RGB_code())

    def get_color(self, i: int, representation: Representation) -> Color:
        """
        Gets the color of a single LED.

        :param i: The index of the LED.
        :param representation: The color representation to return.
        :return: The color of the LED.
        """
        rgb_val = self.strip.getPixelColor(i)
        rgb = (rgb_val >> 16) & 0xFF, (rgb_val >> 8) & 0xFF, rgb_val & 0xFF
        if representation == Representation.RGB:
            return Color.from_rgb(*rgb)
        elif representation == Representation.HSV:
            return Color.from_hsv(*self.rgb_to_hsv(rgb))
        else:
            raise ValueError("Unknown representation")

    def update(self):
        """
        Updates the LED strip with the new colors.
        """
        self.strip.show()

    def suppress(self):
        """
        Turns off all LEDs.
        """
        self.set_all(Color.from_rgb(0, 0, 0))
