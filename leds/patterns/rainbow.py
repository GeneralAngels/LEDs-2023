from leds import Color, Pattern

import time


class Rainbow(Pattern):
    def __init__(self, strip_length: int, duration: float, lapses: float) -> None:
        super().__init__(strip_length, duration)

        self.lapses = lapses

        self.start_time = time.time()

    def init(self):
        self.start_time = time.time()

    def update(self) -> None:
        for i in range(self.strip_length):
            self.strip.set_color(i, Color.from_hsv(
                (360 * (time.time() - self.start_time) / (self.duration / self.lapses) + 360 * i / self.strip_length) % 360, 1, 1))
