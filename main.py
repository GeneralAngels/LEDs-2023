from leds.patterns.blink import Blink
from leds.patterns.breathing import Breathing

from leds.color import Color
from leds.pattern_scheduler import PatternScheduler
from leds.strip import LEDStrip

LED_COUNT = 129


def main():
    strip = LEDStrip(12, LED_COUNT)
    scheduler = PatternScheduler(strip)
    # scheduler.set_default_pattern(Blink(LED_COUNT, 10, 0.5, Color.from_rgb(255, 0, 0)))
    scheduler.set_default_pattern(Breathing(LED_COUNT, 10, Color.from_rgb(0, 0, 255), Color.from_rgb(0, 0, 0), 8, 2))
    scheduler.start()


if __name__ == "__main__":
    main()
