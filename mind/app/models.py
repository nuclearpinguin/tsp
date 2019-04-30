class City:
    def __init__(self, name: str, x: float, y: float, neighbours: list):
        self.name = name
        self.x = x
        self.y = y
        self.neighbours = neighbours

    def add_neighbour(self, city):
        self.neighbours.append(city)

