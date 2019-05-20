import sys, getopt
import os
import pandas as pd


class City:
    """ This class defines how city is represented. """

    def __init__(self, name = "", x = None, y = None, value = 0, neighbours = {}):
        """ Initializes attributes. """
        self.name = name
        self.x = x
        self.y = y
        self.value = value
        self.neighbours = neighbours
        self.visited = False

    def getCoords(self, df_cities):
        self.x = df_cities.loc[df_cities['name']]

    def getNeighbours(self, d ={}):
        self.neighbours = d.get(self.name, {})   # get the dictionary of pairs {neighbour:travel_time}

    def __str__(self):
        """ Defines how print(object_name) is displayed. """
        return "City: " + str(self.name) + "\n" + \
               "Coord: (" + str(self.x) + ', ' +  str(self.y) + ")\n" + \
               "Value: " + str(self.value) + "\n" + \
               "Ngbrs: " + str(self.neighbours) + "\n"


def convert_to_dict(df_cities, df_paths):
    """
    Converts data frames of cities and paths to a dictionary {city: {neighbour : time_to_neighbour}}.
    :param df_cities: pandas.read_csv("cities.csv")
    :param df_paths: pandas.read_csv("paths.csv")
    :return: dictionary {city: {neighbour : time_to_neighbour}}
    """

    dict_paths = {}
    for city in df_cities['name']:
        # get lists of neighbours of city
        neighbours_keys = list(df_paths.loc[df_paths['city_from'] == city]['city_to']) + \
                          list(df_paths.loc[df_paths['city_to'] == city]['city_from'])
        # get list of times needed to travel to each of them
        neighbours_values = list(df_paths.loc[df_paths['city_from'] == city]['time']) + \
                            list(df_paths.loc[df_paths['city_to'] == city]['time'])
        # then merge them
        dict_paths[city] = {key: value for key, value in zip(neighbours_keys, neighbours_values)}
    return dict_paths


# deletes duplicate from list of paths
def duplicate(items):
    unique = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique


def create_cities_dictionary(graph, cities_temp):
    cities_dict_temp ={}
    for k in graph.keys():
        vec = cities_temp.loc[cities['name'] == k].values[0]
        # vec[1] = x, vec[2] = y, vec[3] = quantity
        c = City(k, vec[1], vec[2], vec[3])
        c.getNeighbours(graph)
        cities_dict_temp[k] = c
    return cities_dict_temp


#resources is a list of possible paths with an eye to whole_time, cities list has info about "visited"  returns summary - paths with profits
def choose_the_best_path(resources, cities_list):
    summary ={}
    g = 0
    for j in resources:
        profit = 0
        for stepOne in j:
            if cities_list[stepOne].visited == False:
                profit = profit + cities_list[stepOne].value
                cities_list[stepOne].visited = True
        summary[profit] = j
        g = g + 1
        for stepTwo in j:
            cities_list[stepTwo].visited = False
    # print(summary)
    return summary


# returns the best profit from dictionary which consist of paths with profits
def return_the_best_value(dict_temp):
    naj = max(dict_temp.keys())
    return naj


# return the cost on the best (from profit side) path
def return_cost_of_the_best_path(graph, dict_temp_two, best):
    w = 1
    cost = 0
    do = len(dict_temp_two[best]) - 1
    for x in dict_temp_two[best][:do]:
        cost = cost + graph[x][dict_temp_two[best][w]]
        w = w + 1
    return cost

# create special form of answer for path creation
def create_answer_for_path_creation(dict_temp_three, best):
    answer_plot = []
    do = len(dict_temp_three[best]) -1
    for x in range(do):
        answer_plot.append((dict_temp_three[best][x], dict_temp_three[best][x + 1]))
    return answer_plot


def solve(cities: pd.DataFrame, paths: pd.DataFrame, time: pd.DataFrame):
    assert isinstance(cities, pd.DataFrame), 'Wrong data format!'
    assert isinstance(paths, pd.DataFrame), 'Wrong data format!'
    assert isinstance(time, pd.DataFrame), 'Wrong data format!'

    # finds all paths from chosen start point with eye on possible time
    def find_all_possible_paths(graph, start, time_left, path=[], price=0):
        nonlocal all_paths
        time_left = time_left - price
        path = path + [start]
        if start not in graph:
            return []
        for node in graph[start].keys():
            if time_left - graph[start][node] >= 0:
                find_all_possible_paths(graph, node, time_left, path, graph[start][node])
            elif path not in all_paths:
                all_paths.append(path)
            if time_left == 0:
                break
        return all_paths

    # general paths creating for all possible starting points
    def create_all_possible_paths(graph, time_at_the_beggining):
        list_of_paths = []
        for x in graph.keys():
            # all_paths = []
            list_of_paths = list_of_paths + find_all_possible_paths(graph, x, time_at_the_beggining)
            print(x)
        return list_of_paths

    working_time = time['time'].values[0]

    d = convert_to_dict(cities, paths)

    all_paths = []
    possible_paths = create_all_possible_paths(d, working_time)

    cities_dict = create_cities_dictionary(d, cities)

    cities_dict_with_values = choose_the_best_path(possible_paths, cities_dict)

    best_profit = return_the_best_value(cities_dict_with_values)

    cost_of_the_best_path = return_cost_of_the_best_path(d, cities_dict_with_values, best_profit)

    path_answer = create_answer_for_path_creation(cities_dict_with_values, best_profit)

    solution = [working_time - cost_of_the_best_path, best_profit, cities_dict_with_values[best_profit]]
    return solution, path_answer
