import pandas as pd
import random
from typing import Tuple, List
from collections import namedtuple
from time import time

from .city import City


Output = namedtuple('Output', ['time_left', 'total', 'path'])


def convert_to_dict(df_cities: pd.DataFrame, df_paths: pd.DataFrame, time_limit: int = 60) -> dict:
    """
    Converts data frames of cities and paths to a dictionary.

    Parameters
    ----------
    df_cities: validated data frame with cities
    df_paths: validated data frame with paths
    time_limit

    Returns
    -------
    Dictionary {city: {neighbour : time_to_neighbour}}
    """

    tic = time()
    dict_paths = {}
    for (i, city) in enumerate(df_cities['name']):
        # get lists of neighbours of the city
        neighbours_keys = list(df_paths[df_paths['city_from'] == city]['city_to']) + \
                          list(df_paths[df_paths['city_to'] == city]['city_from'])
        # get list of times needed to travel to each of them
        neighbours_values = list(df_paths[df_paths['city_from'] == city]['travel_time']) + \
                            list(df_paths[df_paths['city_to'] == city]['travel_time'])
        # then merge them
        dict_paths[city] = {key: value for key, value in zip(neighbours_keys, neighbours_values)}

        print(f"Preprocessing in progress: \t{round((i+1)/df_cities['name'].count()*100)}%", end="\r")  # /{df_cities['name'].count()}

        toc = time() - tic

        if time_limit - toc < 0:
            print(f"Whoops! It seems that preprocessing data "
                  f"is taking longer than given limit ({round(time_limit,2)}s). "
                  "No solution was found.")
            break
    print()
    print(f"Preprocessing time:\t\t{round(toc,2)}s")

    return dict_paths


def find_random_path(cities_dict: dict, starting_city: City, time_left: int) -> Output:
    """
    Generates a list containing: time, total and random path.

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

    path = []
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
        if cities_dict.get(next_city).visited:
            next_city = random.choice(list(curr_city.neighbours.keys()))
            # and maybe again
            if cities_dict.get(next_city).visited:
                next_city = random.choice(list(curr_city.neighbours.keys()))
                # three times lucky
                if cities_dict.get(next_city).visited:
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
    Returns list [time_left, sum, path] for the best of paths found in random walk.

    Parameters
    ----------
    cities_dict: dictionary {name : {neighbour1 : travel_time1, neighbour2 : travel_time2}}
    working_time: limits the duration of single path
    n: number of trials for each vertex in random walk
    time_limit: max number of seconds the algorithm can work

    Returns
    -------
    Output
    """

    tic = time()
    best_paths = []

    for (i, starting_city) in enumerate(cities_dict.keys()):
        # print(f"Looping: {round((i+1)/len(cities_dict.keys())*100)}%", end="\r")
        lst = []

        # for better performance, define
        add = lst.append
        for j in range(n):
            if time_limit < 0.1:
                break
            else:
                add(find_random_path(cities_dict, starting_city, working_time))

        # sort list [time_left, total, path] by total, descending
        lst.sort(key=lambda x: x.total, reverse=True)

        if not lst:
            return Output(path=[], total=0, time_left=working_time)

        best_paths.append(lst[0])

        toc = time() - tic

        # update time limit
        time_limit -= toc


        # if finding the best path took time_limit [in seconds] as far,
        # break the loop and select the best of paths found as far
        if time_limit < 0.1:
            break

    best_paths.sort(key=lambda x: x.total, reverse=True)

    return best_paths[0]


def convert_to_edges_list(paths: List[City]) -> List[tuple]:
    """
    Returns edges between cities.
    """
    path = [(cf.name, ct.name) for cf, ct in zip(paths[:-1], paths[1:])]
    return path


# solver
def solve(cities: pd.DataFrame,
          edges: pd.DataFrame,
          df_time: pd.DataFrame,
          n_simulation: int = 50,
          time_limit: int = 60) -> Tuple[Output, list]:
    """
    Solver using random walk.

    Parameters
    ----------
    cities: validated data frame with cities / nodes
    edges: validated data frame with edges / paths
    df_time: validated data frame with time
    n_simulation: number of simulations per nodes
    time_limit: maximum time of arunning the algorithm (in seconds)

    Returns
    -------
    Solution and list of selected edges.
    Tuple[Output, list]
    """
    tic = time()

    assert isinstance(cities, pd.DataFrame), 'Wrong data format!'
    assert isinstance(edges, pd.DataFrame), 'Wrong data format!'
    assert isinstance(df_time, pd.DataFrame), 'Wrong data format!'

    if cities['name'].count() == 0:
        solution = Output(time_limit, 0, [])
        return  solution, []

    # header for better readability in console
    print("= = = = = = = = = = = = = = = = = = = = =")

    # build a dictionary {city : {neighbour1 : travel_time1, neighbour2 : travel_time2}}
    d = convert_to_dict(cities, edges, time_limit)

    # build a dict {city_name : City object}
    cities_dict = {}

    tic_dict = time()

    for (i, k) in enumerate(d.keys()):
        print(f"Creating dictionary:\t\t{round((i+1)/len(d.keys())*100)}%", end="\r")

        # get: name, x, y, quantity
        vec = cities[cities['name'] == k].values[0]
        c = City(k, vec[1], vec[2], vec[3])
        c.set_neighbours(d)
        cities_dict[k] = c

    toc_dict = time() - tic_dict
    print()
    print(f"Creating dictionary time:\t{round(toc_dict,2)}s")


    # get working time from the data frame
    working_time = df_time['time'].values[0]

    # preprocessing time
    preproc_time = time() - tic

    print()

    # if preprocessing data took longer than given time
    if preproc_time > time_limit:
        print("Solving interrupted, time of preprocessing was too long.")
        solu = Output(working_time, 0, [])
        return solu, []

    # else
    time_left = time_limit - preproc_time

    # best solution found as far
    best_solu = Output(time_left, 0, [])
    # worst solution found as far
    worst_solu = Output(time_left, 10 ** 10, [])

    # for displaying in later statistics
    iteration_counter = 0

    # execution time of the algorithm
    toc_solu = 0

    # while there is still time left
    while time_left > 0.1:

        # execution time of the algorithm
        tic_solu = time()

        # compute the best path
        solution = find_best_of_random_paths(cities_dict, working_time, n_simulation, time_left)

        # print(f"Solution: {solution.total}")

        # measure how long executing solution took
        toc_solu = time() - tic_solu

        # update time left
        time_left -= toc_solu

        # update iterator
        iteration_counter += 1

        print(f"Time left:\t\t{round(time_left,2)}s", end="\r")

        # update best and worst solutions (for later comparison)
        if solution.total >= best_solu.total:
            best_solu = solution
        if solution.total <= worst_solu.total:
            worst_solu = solution

    print()
    print(f"> Best solution total:\t{best_solu.total}")
    print(f"> Worst solution total:\t{worst_solu.total}")
    print(f"> Looping profit:\t{best_solu.total - worst_solu.total}")
    print(f"> Iterations:\t\t{iteration_counter}")

    print("Solving finished.")

    return best_solu, convert_to_edges_list(best_solu.path)
