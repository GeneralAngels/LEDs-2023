from leds import Color, Pattern



class RemoteRainbow(Pattern):
    """
    This class is meant to be an example of how to use the PatternSupplier method 
    """
    def __init__(self, strip_length: int, duration: float, current_color: callable) -> None:
        super().__init__(strip_length, duration)

        self.current_color = current_color

    def init(self):
        pass

    def update(self) -> None:
        print(str(self.current_color()))
        self.strip.set_all(self.current_color())
