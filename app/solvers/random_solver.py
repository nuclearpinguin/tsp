import pandas as pd
import random
from collections import namedtuple
from .city import City
from time import time


Output = namedtuple('Output', ['time_left', 'total', 'path'])


def convert_to_dict(df_cities: pd.DataFrame, df_paths: pd.DataFrame) -> dict:
    """
    Converts data frames of cities and paths to a dictionary.

    Parameters
    ----------
    df_cities - pandas.read_csv("cities.csv")
    df_paths - pandas.read_csv("paths.csv")

    Returns
    -------
    A dictionary containing {city: {neighbour : time_to_neighbour}}.
    """

    dict_paths = {}
    for city in df_cities['name']:
        # get lists of neighbours of the city
        neighbours_keys = list(df_paths[df_paths['city_from'] == city]['city_to']) + \
                          list(df_paths[df_paths['city_to'] == city]['city_from'])
        # get list of times needed to travel to each of them
        neighbours_values = list(df_paths[df_paths['city_from'] == city]['travel_time']) + \
                            list(df_paths[df_paths['city_to'] == city]['travel_time'])
        # then merge them
        dict_paths[city] = {key: value for key, value in zip(neighbours_keys, neighbours_values)}

    return dict_paths


def find_random_path(cities_dict: dict, starting_city: City, time_left: int) -> Output:
    """
    Sets random path, trying not to walk through a city multiple times.

    Parameters
    ----------
    cities_dict - dictionary {name : {neighbour1 : travel_time1, neighbour2 : travel_time2}},
                  obtained from convert_to_dict function
    starting_city - City object, from which the path starts
    time_left - number of hours until salesman can travel no more

    Returns
    -------
    A tuple (Output) containing: time, total and path.
    """

    path=[]
    tmp_time = time_left
    total = 0
    curr_city = cities_dict[starting_city]

    # reset visited property
    for city in cities_dict.values():
        city.visited = False

    while tmp_time >= 0:
        time_left = tmp_time

        if curr_city not in path:
            # city's quantity is added only once
            total += curr_city.value

        # add city to a path
        path.append(curr_city)
        curr_city.visited = True

        # select random neighbour
        nghbrs = list(curr_city.neighbours.keys())
        if not nghbrs:
            break

        next_city = random.choice(list(curr_city.neighbours.keys()))

        # if the city was visited - draw again
        if cities_dict[next_city].visited:
            next_city = random.choice(list(curr_city.neighbours.keys()))
            # and maybe again
            if cities_dict[next_city].visited:
                next_city = random.choice(list(curr_city.neighbours.keys()))
                # three times lucky
                if cities_dict[next_city].visited:
                    next_city = random.choice(list(curr_city.neighbours.keys()))

        # subtract the travel time from available time
        tmp_time -= curr_city.neighbours[next_city]

        # if for the drawn neighbour path was too expensive,
        # check other neighbours
        if tmp_time < 0:
            for ngbr in curr_city.neighbours.keys():
                # restore last time that was > 0
                tmp = tmp_time + curr_city.neighbours[next_city]

                # calculate time left after travel to ngbr
                tmp -= curr_city.neighbours[ngbr]
                # if "affordable" neighbour was found
                if tmp > 0:
                    # print(f"Better neighbour from {curr_city.name} found: {ngbr} instead of {next_city}")
                    tmp_time = tmp
                    next_city = ngbr
                    break

        # set city we travelled to as a current city
        curr_city = cities_dict[next_city]

    return Output(time_left, total, path)


def find_best_of_random_paths(cities_dict: dict,
                              working_time: int,
                              n: int,
                              time_limit: int) -> Output:
    """
    Runs find_random_path starting from each city, and returns the best
    (in view of profit) of found paths.

    Parameters
    ----------
    cities_dict - dictionary {name : {neighbour1 : travel_time1, neighbour2 : travel_time2}}
    working_time - limits the duration of single path
    n - number of trials for each vertex in random walk
    time_limit - max number of seconds the algorithm can work

    Returns
    -------
    A tuple (Output) containing: time_left, total and path of the best of random paths.
    """

    start_time = time()

    best_paths = []
    for starting_city in cities_dict.keys():
        lst = []

        # for better performance define
        add = lst.append
        for i in range(n):
            add(find_random_path(cities_dict, starting_city, working_time))

        # sort list [time_left, total, path] by total, descending
        lst.sort(key=lambda x: x[1], reverse=True)
        best_paths.append(lst[0])

        # if finding the best path took 50s as far,
        # break the loop and select the best of paths found as far
        if time() - start_time > time_limit:
            print("Time limit exceeded.")
            break

    best_paths.sort(key=lambda x: x[1], reverse=True)

    return best_paths[0]


def convert_to_edges_list(paths: list) -> list:
    """
    Converts list of City objects to list which can be passed to output file.

    Parameters
    ----------
    paths - list of City objects

    Returns
    -------
    A list of pairs (city_from, city_to).
    """
    path = [(cf.name, ct.name)
            for cf, ct in zip(paths[:-1], paths[1:])]
    return path


# solver
def solve(cities: pd.DataFrame,
          edges: pd.DataFrame,
          info: pd.DataFrame,
          n_simulation: int = 50,
          time_limit: int = 20):
    """

    Parameters
    ----------
    cities - data frame containing: name, x, y, quantity
    edges - data frame containing: city_from, city_to, travel_time
    info - silly data frame containing: time
    n_simulation - number of random walks simulations from each city
    time_limit - number of seconds until calculation is interrupted,
                 and the best solution found as far is returned

    Returns
    -------
    A tuple: Output and list containing pairs (city_from, city_to).
    """
    assert isinstance(cities, pd.DataFrame), 'Wrong data format!'
    assert isinstance(edges, pd.DataFrame), 'Wrong data format!'
    assert isinstance(info, pd.DataFrame), 'Wrong data format!'

    # build a dictionary {city : {neighbour1 : travel_time1, neighbour2 : travel_time2}}
    d = convert_to_dict(cities, edges)

    # build a dict {city_name : City object}
    cities_dict = {}

    for k in d.keys():
        # get: name, x, y, quantity
        vec = cities[cities['name'] == k].values[0]
        c = City(k, vec[1], vec[2], vec[3])
        c.set_neighbours(d)
        cities_dict[k] = c

    # get working time from the data frame
    working_time = info['time'].values[0]

    # compute the best path
    solution = find_best_of_random_paths(cities_dict, working_time, n_simulation, time_limit)

    return solution, convert_to_edges_list(solution.path)
