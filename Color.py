class Color:
    """docstring for Color."""
    def __init__(self):
        self.__color = ""

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, suit):
        if suit == "H" or suit == "D":
            self.__color = "red"
        else:
            self.__color = "black"
