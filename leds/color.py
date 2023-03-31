from __future__ import annotations

import numpy as np
import rpi_ws281x

from enum import Enum


class Representation(Enum):
    RGB = 0
    HSV = 1


class Color:
    def __init__(self, representation: Representation, values: tuple[int]):
        self.representation = representation
        self.values = values

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> Color:  # TODO: decide what should and shouldnt be a classmethod
        """
        Creates a color from RGB values.
        :param r: Red (0-255)
        :param g: Green (0-255)
        :param b: Blue (0-255)
        :return: Color
        """
        if not 0 <= r <= 255: raise ValueError("red must be a value between 0 and 255")
        if not 0 <= g <= 255: raise ValueError("green must be a value between 0 and 255")
        if not 0 <= b <= 255: raise ValueError("blue must be a value between 0 and 255")
        return Color(Representation.RGB, (r, g, b))

    @classmethod
    def from_hsv(cls, h: int, s: int, v: int) -> Color:
        """
        Creates a color from HSV values.
        :param h: Hue (0-360)
        :param s: Saturation (0-1)
        :param v: Value (0-1)
        :return: Color
        """
        if not 0 <= h <= 360: raise ValueError("hue must be a value between 0 and 360")
        if not 0 <= s <= 1: raise ValueError("saturation must be a value between 0 and 1")
        if not 0 <= v <= 1: raise ValueError("value must be a value between 0 and 1")
        return Color(Representation.HSV, (h, s, v))

    def get_RGB_code(self):
        """
        returns the RGB code of the color 
        """
        if self.representation == Representation.RGB:
            return rpi_ws281x.Color(*self.values)
        elif self.representation == Representation.HSV:
            return rpi_ws281x.Color(*self.to_rgb().values)

    def to_rgb(self) -> Color:
        """
        Converts the color to RGB representation.
        :return: Color
        """
        if self.representation == Representation.RGB:
            return self
        elif self.representation == Representation.HSV:
            return Color.from_rgb(*Color.hsv_to_rgb(self).values)
        else:
            raise ValueError("Unknown representation")

    def to_hsv(self) -> Color:
        """
        Converts the color to HSV representation.
        :return: Color
        """
        if self.representation == Representation.RGB:
            return Color.from_hsv(*Color.rgb_to_hsv(self).values)
        elif self.representation == Representation.HSV:
            return self
        else:
            raise ValueError("Unknown representation")

    @classmethod
    def lerp(cls, c1: Color, c2: Color, t: float) -> Color:
        """
        Interpolates between the two given colors.
        :param c1: Color 1
        :param c2: Color 2
        :param t: Interpolation factor (0-1)
        :return: Interpolated color
        """
        if c1.representation != c2.representation:
            raise ValueError("colors must be of same representation")

        return Color(c1.representation, (
            int(c1.values[0] + t * (c2.values[0] - c1.values[0])),
            int(c1.values[1] + t * (c2.values[1] - c1.values[1])),
            int(c1.values[2] + t * (c2.values[2] - c1.values[2]))
        ))
    
    @staticmethod
    def hsv_to_rgb(hsv: Color) -> Color:
        # calculate values of RGB
        h, s, v = hsv.values

        if s == 0:
            r, g, b = v, v, v
        else:
            h /= 60
            i = int(h)
            f = h - i

            p = v * (1 - s)
            q = v * (1 - s * f)
            t = v * (1 - s * (1 - f))

            if i == 0:
                r, g, b = v, t, p
            elif i == 1:
                r, g, b = q, v, p
            elif i == 2:
                r, g, b = p, v, t
            elif i == 3:
                r, g, b = p, q, v
            elif i == 4:
                r, g, b = t, p, v
            else:
                r, g, b = v, p, q

        # convert to 8-bit values
        r, g, b = int(255 * r), int(255 * g), int(255 * b)

        return Color(Representation.RGB, (r, g, b))

    @staticmethod
    def rgb_to_hsv(rgb: Color) -> Color:
        #  normalize RGB values to be between 0 and 1
        r, g, b = [(v / 255.0) for v in rgb.values]

        # get maximum and minimum values of R, G, and B
        max_val = np.max([r, g, b])
        min_val = np.min([r, g, b])

        # calculate value (V)
        v = max_val

        # calculate saturation (S)
        if v == 0:
            s = 0
        else:
            s = (max_val - min_val) / max_val

        # calculate hue (H)
        if s == 0:
            h = 0
        else:
            delta = max_val - min_val
            if max_val == r:
                h = 60 * (((g - b) / delta) % 6)
            elif max_val == g:
                h = 60 * (((b - r) / delta) + 2)
            else:
                h = 60 * (((r - g) / delta) + 4)
            h = round(h % 360, 2)

        return Color(Representation.HSV, (h, s, v))

    def __str__(self):
        return f"{self.representation.name}, {self.values}"
