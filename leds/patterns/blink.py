from leds.pattern import Pattern
from leds.color import Color

from time import time


class Blink(Pattern):
    def __init__(self, strip_length: int, duration: float, interval: float,
                 color: Color) -> None:
        super().__init__(strip_length, duration)
        self.interval = interval

        self.color = color

        self.clock = time()

    def start(self):
        self.clock = time()

    def update(self) -> None:
        if time() - self.clock < self.interval:
            self.strip.set_all(self.color)
        elif time() - self.clock < self.interval * 2:
            self.strip.set_all(Color.from_rgb(0, 0, 0))
        else:
            self.clock = time()
