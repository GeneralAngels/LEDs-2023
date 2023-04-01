from leds.patterns import *

from leds import Color, PatternScheduler, LEDStrip, PatternSupplier

import time

from strip_sim import LEDStripSim

from threading import Thread

import colorsys

LED_COUNT = 130


def inc_color(color: Color):
    while True:
        color.values = ((color.values[0] + 1 % 360), 1, 1)
        time.sleep(0.1)


def main():
    # strip = LEDStrip(12, LED_COUNT)
    strip = LEDStripSim(LED_COUNT)
    scheduler = PatternScheduler(strip)
    # scheduler.set_default_pattern(Blink(LED_COUNT, 10, 0.5, Color.from_rgb(255, 0, 0)))
    scheduler.set_default_pattern(Breathing(LED_COUNT, 10, Color.from_rgb(0, 0, 255), Color.from_rgb(0, 0, 0), 8, 2))
    # scheduler.set_pattern(Blink(LED_COUNT, 10, 0.5, Color.from_hsv(180, 1, 100)))
    # scheduler.set_default_pattern(RemoteRainbow(LED_COUNT, 10, PatternSupplier(lambda: current_color)))
    # scheduler.set_default_pattern(Rainbow(LED_COUNT, 10, 2))
    scheduler.start()

    # rainbow_thread = Thread(target=inc_color, args=(current_color,))

    # rainbow_thread.start()

    strip.mainloop()


if __name__ == "__main__":
    main()
