import pygame

from typing import List

from leds.color import Color, Representation


class LEDStripSim():
    def __init__(self, length: int) -> None:
        self.length = length

        self.window_width = 100
        self.window_height = 100

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

        pygame.display.set_caption("LED Strip Simulator")

        self.led_size = 10

        self.leds: List[LEDSim] = [LEDSim(self.screen, 0, 0, self.led_size) for _ in range(self.length)]

        self.reformat_leds()

    def mainloop(self) -> None:
        while True:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.VIDEORESIZE:
                    self.on_resize(event)

            self.update()

            pygame.display.update()

    def on_resize(self, event) -> None:
        self.window_width, self.window_height = event.dict['size']
        self.reformat_leds()

    def reformat_leds(self) -> None:
        leds_per_row = int(self.window_width / self.led_size) if self.led_size > 0 else 1
        leds_per_column = int(self.length / leds_per_row) if leds_per_row > 0 else self.length
        extra_leds = self.length - leds_per_row * leds_per_column

        for j in range(leds_per_column):
            for i in range(leds_per_row):
                self.leds[i + j * leds_per_row].x = i * self.led_size + self.led_size//2
                self.leds[i + j * leds_per_row].y = j * self.led_size + self.led_size//2

        for i in range(extra_leds):
            self.leds[i + leds_per_row * leds_per_column].x = i * self.led_size + self.led_size//2
            self.leds[i + leds_per_row * leds_per_column].y = leds_per_column * self.led_size + self.led_size//2

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

class LEDSim:
    def __init__(self, screen: pygame.display, x: int, y: int, size: float,
                 color: Color = Color.from_rgb(0, 0, 0)) -> None:
        self.screen = screen

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
        pygame.draw.rect(self.screen, self.color.to_rgb().values, (self.x - self.size//2, self.y - self.size//2, self.size - 1, self.size - 1))
