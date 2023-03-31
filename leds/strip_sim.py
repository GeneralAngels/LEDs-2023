import tkinter as tk
from threading import Thread

from typing import List

from leds.color import Color, Representation


class LEDSim:
    def __init__(self, master: tk.Tk, x: int, y: int, size: float,
                 color: Color = Color.from_rgb(0, 0, 0)) -> None:
        self.master = master

        self.canvas = tk.Canvas(master, width=100, height=100)
        self.canvas.pack()

        self.x = x
        self.y = y

        self.size = size

        self.color = color

    def set_color(self, color: Color) -> None:
        self.color = color

    def get_color(self, representation: Representation) -> Color:
        match representation:
            case Representation.RGB:
                return self.color.to_rgb()
            case Representation.HSV:
                return self.color.to_hsv()
            case _:
                raise ValueError("Unknown representation")

    def draw(self) -> None:
        self.canvas.create_rectangle(self.x, self.y,
                                     self.x + self.size, self.y + self.size,
                                     fill=f"#{self.color.values[0]:02x}\
                                             {self.color.values[1]:02x}\
                                             {self.color.values [2]:02x}")


class LEDStripSim(Thread):
    def __init__(self, length: int) -> None:
        super().__init__()

        self.length = length

        self.master = tk.Tk()

        self.leds: List[LEDSim] = [None for _ in range(self.length)]

        self.led_size = 10

        self.window_width = 100
        self.window_height = 100

        self.master.bind("<Configure>", self.on_resize)

    def begin(self) -> None:
        self.start()

    def run(self) -> None:
        self.master.mainloop()

    def on_resize(self, event) -> None:
        self.canvas.config(width=event.width, height=event.height)
        self.window_width = event.width
        self.window_height = event.height
        self.reformat_leds()

    def reformat_leds(self) -> None:
        leds_per_row = int(self.window_width / self.led_size)
        leds_per_column = int(self.window_height / self.led_size)
        extra_leds = self.length - leds_per_row * leds_per_column

        for j in range(leds_per_column):
            for i in range(leds_per_row):
                self.leds[i + j * leds_per_row].x = i * self.led_size
                self.leds[i + j * leds_per_row].y = j * self.led_size

        for i in range(extra_leds):
            self.leds[i + leds_per_row * leds_per_column].x = i * self.led_size
            self.leds[i + leds_per_row * leds_per_column].y = leds_per_column * self.led_size

    def set_color(self, i: int, color: Color) -> None:
        self.leds[i].set_color(color)

    def set_all(self, color: Color) -> None:
        for i in range(self.length):
            self.leds[i].set_color(color)

    def get_color(self, i: int, representation: Representation) -> Color:
        return self.leds[i].get_color(representation)

    def update(self) -> None:
        for led in self.leds:
            led.draw()

    def suppress(self) -> None:
        self.set_all(Color.from_rgb(0, 0, 0))
