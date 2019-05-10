import numpy as np
import pandas as pd
import random


class Path:
    """ This class defines how path is represented."""

    def __init__(self, sum=0, time=0, n=0):
        """ Initializes attributes. """
        self.path = []
        self.distinct_path = []
        self.sum = sum
        self.time = time
        self.number_of_visited_cities = n

    def add_city(self, city, value, travel_time=0):
        """ Modifies attributes when adding a city to a path. """
        if city not in self.path:
            self.distinct_path.append(city)
            self.sum += value
            self.number_of_visited_cities += 1
        self.path.append(city)
        self.time += travel_time

    def __repr__(self):
        """ Defines what is displayed when object_name is called. """
        return "Path()"

    def __str__(self):
        """ Defines how print(object_name) is displayed. """
        return "Path: " + str(self.path) + "\n" + \
               "Distinct path: " + str(self.distinct_path) + "\n" + \
               "Sum: " + str(self.sum) + "\n" + \
               "Time: " + str(self.time) + "\n" + \
               "Number of visited cities: " + str(self.number_of_visited_cities) + "\n"


class City:
    """ This class defines how city is represented. """

    def __init__(self, name="", x=None, y=None, value=0, neighbours={}):
        """ Initializes attributes. """
        self.name = name
        self.x = x
        self.y = y
        self.value = value
        self.neighbours = neighbours
        self.visited = False

    def getCoords(self, df_cities):
        self.x = df_cities.loc[df_cities['ID']]

    def getNeighbours(self, d=dict()):
        self.neighbours = d.get(self.name, {})   # get the dictionary of pairs {neighbour:travel_time}

    def __str__(self):
        """ Defines how print(object_name) is displayed. """
        return "City: " + str(self.name) + "\n" + \
               "Coord: (" + str(self.x) + ', ' +  str(self.y) + ")\n" + \
               "Value: " + str(self.value) + "\n" + \
               "Ngbrs: " + str(self.neighbours) + "\n"


def convert_to_dict(df_cities: pd.DataFrame, df_paths: pd.DataFrame):
    """
    Converts data frames of cities and paths to a dictionary {city: {neighbour : time_to_neighbour}}.
    :param df_cities: pandas.read_csv("cities.csv")
    :param df_paths: pandas.read_csv("paths.csv")
    :return: dictionary {city: {neighbour : time_to_neighbour}}
    """

    dict_paths = {}
    for city in df_cities['ID']:
        # get lists of neighbours of city
        neighbours_keys = list(df_paths.loc[df_paths['city_from'] == city]['city_to']) + \
                          list(df_paths.loc[df_paths['city_to'] == city]['city_from'])
        # get list of times needed to travel to each of them
        neighbours_values = list(df_paths.loc[df_paths['city_from'] == city]['time']) + \
                            list(df_paths.loc[df_paths['city_to'] == city]['time'])
        # then merge them
        dict_paths[city] = {key: value for key, value in zip(neighbours_keys, neighbours_values)}
    return dict_paths


def find_random_path(cities_list, starting_city, time_left):
    """ Generates a list containing: time, sum and random path. """

    path = []
    tmp_time = time_left
    sum = 0
    curr_city = cities_list[starting_city]

    while tmp_time > 0:
        time_left = tmp_time
        if curr_city not in path:
            # city value is added only once
            sum += curr_city.value

        # add city to a path
        path.append(curr_city)

        # select random neighbour
        next_city = random.choice(list(curr_city.neighbours.keys()))

        # subtract the travel time from available time
        tmp_time -= curr_city.neighbours[next_city]

        # set city we travelled to as a current city
        curr_city = cities_list[next_city]

    return [time_left, sum, path]


def find_best_of_random_paths(df_cities: pd.DataFrame, df_paths: pd.DataFrame, df_time: pd.DataFrame, n=50):
    """
    Returns list [time_left, sum, path] for the best of paths found in random walk.
    :param n: number of trials for each vertex in random walk
    """

    d = convert_to_dict(df_cities, df_paths)

    # define empty dictionary containing {city_name : city_object}
    cities_list = {}

    for k in d.keys():
        vec = df_cities.loc[df_cities['ID'] == k].values[0]
        c = City(k, vec[1], vec[2], vec[3])
        c.getNeighbours(d)
        cities_list[k] = c

    time = df_time['time'].values[0]

    best_paths = []
    for starting_city in list(d.keys()):
        lst = []
        for i in range(n):
            lst.append(find_random_path(cities_list, starting_city, time))

        # sort list [time_left, sum, path] by sum (second element), descending
        lst.sort(key=lambda x: x[1], reverse=True)
        best_paths.append(lst[0])

    best_paths.sort(key=lambda x: x[1], reverse=True)

    return best_paths[0]


# tsp solver
def tsp(cities: pd.DataFrame, coords: pd.DataFrame, info: int):
    assert isinstance(cities, pd.DataFrame), 'Wrong data format!'
    assert isinstance(coords, pd.DataFrame), 'Wrong data format!'
    # assert isinstance(info, pd.DataFrame), 'Wrong data format!'

    df_time = pd.DataFrame([{'time': 12}])

    time_left, total, pth = find_best_of_random_paths(df_cities=cities,
                                                      df_paths=coords,
                                                      df_time=df_time)

    print(f'Time left : {time_left}')
    print(f'Earned : {total}')
    print("Best found path:")

    for item in pth:
        print(item)


