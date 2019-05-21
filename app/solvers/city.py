import pandas as pd


class City:
    """ This class defines how city is represented. """

    def __init__(self, name: str, x: int, y: int, value: int = 0) -> None:
        """ Initializes attributes. """
        self.name = str(name)
        self.x = x
        self.y = y
        self.value = value
        self.neighbours = {}
        self.visited = False

    def set_neighbours(self, d) -> None:
        self.neighbours = d.get(self.name, {})   # get the dictionary of pairs {neighbour:travel_time}

    def __str__(self) -> str:
        """ Defines how print(object_name) is displayed. """
        return f"City: {self.name}\n" + \
               f"Coord: ({self.x}, {self.y})\n" + \
               f"Value: {self.value}\n" + \
               f"Ngbrs: {self.neighbours}\n"
