import pandas as pd
from .city import City
from .random_solver import Output, convert_to_dict


def find_all_possible_paths(graph, start, time, path=[], price=0):
    global all_paths
    global newpaths
    time = time - price
    path = path + [start]
    if start not in graph:
        return []

    for node in graph[start].keys():
        if time - graph[start][node] >= 0:
            newpaths = find_all_possible_paths(graph, node, time, path, graph[start][node])
        else:
            all_paths.append(path)
        if time == 0:
            break
    return all_paths


def create_all_possible_paths(graph, time):
    xs = []
    for x in graph.keys():
        all_paths = find_all_possible_paths(graph, x, time)
        xs = xs + list(set(all_paths))
    return xs


def create_cities_dictionary(cities_dict, graph, cities):
    for k in graph.keys():
        vec = cities.loc[cities['name'] == k].values[0]
        # vec[1] = x, vec[2] = y, vec[3] = quantity
        c = City(k, vec[1], vec[2], vec[3])
        c.set_neighbours(graph)
        cities_dict[k] = c
    return cities_dict


def choose_the_best_path(lista, cities_list):
    podsumowanie = {}

    for j in lista:
        total = 0
        for step in j:
            if not cities_list[step].visited:
                total = total + cities_list[step].value
                cities_list[step].visited = True
        podsumowanie[total] = j

        for step in j:
            cities_list[step].visited = False

    return podsumowanie


def return_the_best_value(dict):
    return max(dict.keys())


def return_time_of_the_best_path(dict, best):
    w = 1
    time = 0
    do = len(dict[best]) - 1
    for x in dict[best][:do]:
        time = time + dict[x][dict[best][w]]
        w += 1
    return time


def create_answer_for_path_creation(dict, best):
    answer_plot = []
    do = len(dict[best]) -1
    for x in range(do):
        answer_plot.append((dict[best][x], dict[best][x + 1]))
    return answer_plot


def solve(cities: pd.DataFrame, paths: pd.DataFrame, time: pd.DataFrame):
    assert isinstance(cities, pd.DataFrame), 'Wrong data format!'
    assert isinstance(paths, pd.DataFrame), 'Wrong data format!'
    assert isinstance(time, pd.DataFrame), 'Wrong data format!'

    # build a dictionary {city : {neighbour1 : travel_time1, neighbour2 : travel_time2}}
    d = convert_to_dict(cities, paths)

    lista = create_all_possible_paths(d, time)

    # build a dict {city_name : City object}
    cities_dict = create_cities_dictionary(d)

    cities_dict_with_values = choose_the_best_path(lista, cities_dict)

    best = return_the_best_value(cities_dict_with_values)

    worked_time = return_time_of_the_best_path(cities_dict_with_values, best)

    edges = create_answer_for_path_creation(cities_dict_with_values, best)

    output = Output(time_left=time.values[0] - worked_time,
                    total=best,
                    path=cities_dict_with_values[best]
                    )
    return output, edges
