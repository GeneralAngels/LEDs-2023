from leds import Color, Pattern



class Compass(Pattern):
    """
    This class is meant to be an example of how to use the PatternSupplier method 
    """
    def __init__(self, strip_length: int, duration: float, pos: callable) -> None:
        super().__init__(strip_length, duration)

        self.pos = pos

    def start(self):
        pass

    def update(self) -> None:
        print(self.pos())
