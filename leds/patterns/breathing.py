from leds.pattern import Pattern
from leds.color import Color

from time import time


class Breathing(Pattern):
    def __init__(self, strip_length: int, duration: float, inhale_color: Color, exhale_color: Color, breath_time: float, interval: float) -> None:
        super().__init__(strip_length, duration)

        self.inhale_color = inhale_color
        self.exhale_color = exhale_color

        self.breath_time = breath_time
        self.interval = interval

        self.clock = time()

    def start(self):
        self.clock = time()

    def update(self) -> None:
        if time() - self.clock < self.breath_time / 2:
            t = (time() - self.clock) / (self.breath_time / 2)
            self.strip.set_all(Color.lerp(
                self.exhale_color,
                self.inhale_color,
                t
            ))
        elif time() - self.clock < self.breath_time:
            t = (time() - self.clock - self.breath_time / 2) / (self.breath_time / 2)
            self.strip.set_all(Color.lerp(
                self.inhale_color,
                self.exhale_color,
                t
            ))
        elif time() - self.clock < self.breath_time + self.interval:
            self.strip.set_all(self.exhale_color)
        else:
            self.clock = time()
