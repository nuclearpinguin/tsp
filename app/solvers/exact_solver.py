from .city import City


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


def find_all_paths(graph, start, time, path=[]):
    path = path + [start]
    if time == 0:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        time = time - 1
        print(path)
        print(graph[start])
        print(node)
        print(time)
        newpaths = find_all_paths(graph, node, time, path)
        for newpath in newpaths:
            paths.append(newpath)
        if time == 0:
            break
    return paths


def find_all_possible_paths(graph, start, time, path=[], price=0):
    global all_paths
    global newpaths
    time = time - price
    path = path + [start]
    if start not in graph:
        return []
    for node in graph[start].keys():
        if time - graph[start][node] >=0:
            newpaths = find_all_possible_paths(graph, node, time , path, graph[start][node])
        else:
            all_paths.append(path)
        if time == 0:
            break
    return all_paths


def duplicate(items):
    unique = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique


def create_all_possible_paths(graph,time):
    lista = []
    for x in graph.keys():
        all_paths=[]
        newpaths=[]
        lista = lista + duplicate(find_all_possible_paths(graph,x,time))
        print(x)
    return lista


def create_cities_dictionary(graph):
    for k in graph.keys():
        vec = cities.loc[cities['name'] == k].values[0]
        # vec[1] = x, vec[2] = y, vec[3] = quantity
        c = City(k, vec[1], vec[2], vec[3])
        c.set_neighbours(d)
        cities_dict[k] = c
    return cities_dict


def choose_the_best_path(lista, cities_list):
    podsumowanie={}
    g = 0
    i = 1
    for j in lista:
        zysk = 0
        for krok in j:
            if cities_list[krok].visited == False:
                zysk = zysk + cities_list[krok].value
                cities_list[krok].visited = True
        podsumowanie[zysk] = j
        g = g + 1
        for krok in j:
            cities_list[krok].visited = False
        # print(i)
        i = i + 1
    return podsumowanie


def return_the_best_value(dict):
    naj = max(dict.keys())
    return naj


def return_cost_of_the_best_path(dict, best):
    w = 1
    koszt = 0
    do = len(dict[best]) - 1
    for x in dict[best][:do]:
        koszt = koszt + dict[x][dict[best][w]]
        w = w + 1
    return koszt


def create_answer_for_path_creation(dict, best):
    answer_plot = []
    do = len(dict[best]) -1
    for x in range(do):
        answer_plot.append((dict[best][x], dict[best][x + 1]))
    return answer_plot
