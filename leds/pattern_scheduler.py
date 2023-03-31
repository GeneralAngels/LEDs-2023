from threading import Thread

import time

from leds.strip import LEDStrip
from leds.pattern import Pattern


class PatternScheduler(Thread):
    def __init__(self, strip: LEDStrip, update_time: float = 0.03) -> None:
        super().__init__()

        self.strip = strip
        self.update_time = update_time

        self.current_pattern: Pattern = None
        self.default_pattern: Pattern = None
        self.pattern_runs = 0  # TODO: implement multiple pattern runs
        self.current_run = 0

    def run(self) -> None:
        while True:
            start = time.time()
            if self.current_pattern is not None:
                if not self.current_pattern.is_finished():
                    self.current_pattern.update()
                elif self.default_pattern is not None:
                    self.current_pattern = self.default_pattern
                    self.current_pattern.init()
                else:
                    self.strip.suppress()

            self.strip.update()
            # time.sleep(max(0, self.update_time - (time.time() - start)))

    def set_pattern(self, pattern: Pattern) -> None:
        pattern.insert_strip(self.strip)

        self.current_pattern = pattern
        self.current_pattern.init()

    def set_default_pattern(self, pattern: Pattern) -> None:
        pattern.insert_strip(self.strip)

        if self.current_pattern is None:
            self.current_pattern = pattern
        self.default_pattern = pattern
        self.default_pattern.init()
