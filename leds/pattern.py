from abc import ABC, abstractmethod
import time

from leds.strip import LEDStrip


class Pattern(ABC):
    def __init__(self, strip_length: int, duration: float) -> None:
        self.strip = None
        self.strip_length = strip_length
        self.duration = duration

        self.start_time = time.time()

    def insert_strip(self, strip: LEDStrip) -> None:
        self.strip = strip

    def init(self):
        self.start_time = time.time()
        self.start()

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError("Subclass must implement abstract method")

    def is_finished(self) -> bool:
        return time.time() - self.start_time >= self.duration
