from __future__ import annotations

import numpy as np
import rpi_ws281x

from enum import Enum
from dataclasses import dataclass


class Representation(Enum):
    RGB = 0
    HSV = 1


class Color:
    def __init__(self, representation: Representation, value: tuple[int]):
        self.representation = representation
        self.values = value

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> Color:
        return Color(Representation.RGB, (r, g, b))

    @classmethod
    def from_hsv(cls, h: int, s: int, v: int) -> Color:
        return Color(Representation.HSV, (h, s, v))

    def get_value(self):
        if self.representation == Representation.RGB:
            return rpi_ws281x.Color(*self.values)
        elif self.representation == Representation.HSV:
            return rpi_ws281x.Color(*self.to_rgb().values)

    def to_rgb(self) -> Color:
        if self.representation == Representation.RGB:
            return self
        elif self.representation == Representation.HSV:
            return Color.hsv_to_rgb(self)
        else:
            raise ValueError("Unknown representation")

    def to_hsv(self) -> Color:
        if self.representation == Representation.RGB:
            return Color.rgb_to_hsv(self)
        elif self.representation == Representation.HSV:
            return self
        else:
            raise ValueError("Unknown representation")

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
        r, g, b = rgb.r / 255.0, rgb.g / 255.0, rgb.b / 255.0

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

    @classmethod
    def lerp(cls, c1: Color, c2: Color, t: float) -> Color:
        if c1.representation != c2.representation:
            raise ValueError("colors must be of same representation")

        return Color(c1.representation, (
            int(c1.values[0] + t * (c2.values[0] - c1.values[0])),
            int(c1.values[1] + t * (c2.values[1] - c1.values[1])),
            int(c1.values[2] + t * (c2.values[2] - c1.values[2]))
        ))

    def __str__(self):
        return f"{self.representation.name}, {self.values}"
