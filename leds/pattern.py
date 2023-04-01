from abc import ABC, abstractmethod
import time

from typing import Callable

from leds.strip import LEDStrip


class Pattern(ABC):
    def __init__(self, strip_length: int, duration: float) -> None:
        """
        :param strip_length: The length of the LED strip
        :param duration: The duration of the pattern in seconds
        """
        self.strip = None
        self.strip_length = strip_length
        self.duration = duration

    def insert_strip(self, strip: LEDStrip) -> None:
        """
        Inserts the LED strip into the pattern.
        This method is called by the PatternScheduler.
        """
        self.strip = strip

    @abstractmethod
    def init(self) -> None:
        """
        Logic that is executed once at the beginning of the pattern.
        """
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def update(self) -> None:
        """
        Logic that is executed every update cycle.
        """
        raise NotImplementedError("Subclass must implement abstract method")

    def is_finished(self) -> bool:
        """
        Logic that decides whether the pattern is finished or not.
        By default, the pattern is finished after the specified duration is over.
        """
        return time.time() - self.start_time >= self.duration


def PatternSupplier(func: Callable[[], object]) -> Callable[[], object]:
    return lambda: func()
