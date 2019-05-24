import pandas as pd


class City:
    """
    This class defines how city is represented.
    """

    def __init__(self, name: str, x: int, y: int, value: int = 0) -> None:
        """
        Initializes attributes.

        Parameters
        ----------
        name - name of the city
        x - x coordinate
        y - y coordinate
        value - amount of goods for salesman to sale
        """

        self.name = str(name)
        self.x = x
        self.y = y
        self.value = value
        self.neighbours = {}
        self.visited = False

    def set_neighbours(self, d) -> None:
        """

        Parameters
        ----------
        d - external dictionary, obtained by convert_to_dict function from random_solver
        """
        self.neighbours = d.get(self.name, {})   # get the dictionary of pairs {neighbour:travel_time}

    def __str__(self) -> str:
        """
        Defines how print(object_name) is displayed.
        """
        return f"City: {self.name}\n" + \
               f"Coord: ({self.x}, {self.y})\n" + \
               f"Value: {self.value}\n" + \
               f"Ngbrs: {self.neighbours}\n"
