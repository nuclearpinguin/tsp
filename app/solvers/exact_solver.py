import pandas as pd
from .city import City
from .random_solver import convert_to_dict, Output


def choose_the_best_path(resources, cities_list):
    """
    Resource is a list of possible paths with an eye on possible time
        cities list is used to hold an information if city has been visited or not
        function returns summary - path with profits 
    Parameters
    ----------
    resources - list [[path_1], [path_2], [path_3], ...]
    cities_list - list [city_A, city_B, city_C,..]

    Returns - dictionary {'value_1' : [path_i], 'value_2' : [path_y],...}
    -------

    """
    summary = {}
    g = 0
    for j in resources:
        profit = 0
        for stepOne in j:
            if cities_list[stepOne].visited is False:
                profit = profit + cities_list[stepOne].value
                cities_list[stepOne].visited = True
        summary[profit] = j
        g = g + 1
        for stepTwo in j:
            cities_list[stepTwo].visited = False
    return summary


def return_the_best_value(dict_temp):
    """
    Returns the best profit from dictionary which consist of paths with profits.
    Parameters
    ----------
    dict_temp - dictionary {'value_1' : [path_i], 'value_2' : [path_y],...}

    Returns - numer : value_y
    -------

    """
    naj = max(dict_temp.keys())
    return naj


def return_path_time(graph, dict_temp_two, best):
    """
    Returns the cost on the best (from profit side) path
    Parameters
    ----------
    graph
    dict_temp_two - dictionary {'value_1' : [path_i], 'value_2' : [path_y],...}
    best - number - value_y

    Returns - number 
    -------

    """
    w = 1
    cost = 0
    do = len(dict_temp_two[best]) - 1
    for x in dict_temp_two[best][:do]:
        cost = cost + graph[x][dict_temp_two[best][w]]
        w = w + 1
    return cost


def create_answer_for_path_creation(dict_temp_three, best):
    """
    Creates special form of answer for path creation
    Parameters
    ----------
    dict_temp_three - dictionary {'value_1' : [path_i], 'value_2' : [path_y],...}
    best - number - value_y

    Returns - list - [{city_1,city_2),(city_2,city_3),...]
    -------

    """
    answer_plot = []
    do = len(dict_temp_three[best]) - 1
    for x in range(do):
        answer_plot.append((dict_temp_three[best][x], dict_temp_three[best][x + 1]))
    return answer_plot


def exact_solve(cities: pd.DataFrame, paths: pd.DataFrame, time: pd.DataFrame, time_limit: int = 20):
    """

    Parameters
    ----------
    cities
    paths
    time

    Returns
    -------

    """
    print('Works exact')

    assert isinstance(cities, pd.DataFrame), 'Wrong data format!'
    assert isinstance(paths, pd.DataFrame), 'Wrong data format!'
    assert isinstance(time, pd.DataFrame), 'Wrong data format!'

    def find_all_possible_paths(graph, start, time_left, path=[], time_used=0):
        """

        Parameters
        ----------
        graph
        start - letter 
        time_left - number 
        path - list [city_1, city_2, city_3]
        time_used - number

        Returns - list - [city_1, city_2, city_3, city_4]
        -------

        """
        nonlocal all_paths
        time_left = time_left - time_used
        path = path + [start]
        if start not in graph:
            return []
        # all_paths = []
        for node in graph[start].keys():
            if time_left - graph[start][node] >= 0:
                find_all_possible_paths(graph, node, time_left, path, graph[start][node])
            elif path not in all_paths:
                all_paths.append(path)
            if time_left == 0:
                break
        return all_paths

    def create_all_possible_paths(graph, time_at_the_beggining):
        """

        Parameters
        ----------
        graph
        time_at_the_beggining - number

        Returns - list [[path_1], [path_2], [path_3], ...]
        -------

        """
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
    cities_dict = {}
    for k in d.keys():
        # get: name, x, y, quantity
        vec = cities[cities['name'] == k].values[0]
        c = City(k, vec[1], vec[2], vec[3])
        c.set_neighbours(d)
        cities_dict[k] = c

    cities_dict_with_values = choose_the_best_path(possible_paths, cities_dict)

    best_profit = return_the_best_value(cities_dict_with_values)

    path_time = return_path_time(d, cities_dict_with_values, best_profit)

    path_answer = create_answer_for_path_creation(cities_dict_with_values, best_profit)

    solution = [working_time - path_time, best_profit, cities_dict_with_values[best_profit]]

    print(solution)

    output = Output(time_left=working_time - path_time,
                    path=path_answer,
                    total=best_profit)
    print(output)
    return output, []
