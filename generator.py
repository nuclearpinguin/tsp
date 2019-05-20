from random import randint
import pandas as pd
from time import sleep


def unique(xs: list):
    seen = set()  # < keep track of what we have seen as we go
    unique_list = [x for x in xs if not ((x[1], x[0]) in seen or (x[0], x[1]) in seen or seen.add((x[0], x[1])))]
    return unique_list


def make_sample(size: int) -> list:
    x, y = randint(0, 100), randint(0, 100)
    start_point = (x, y, 'none')
    cities = [start_point]
    n = 1
    step = max(1, size//10)
    while n < size:
        i = -1
        cities = unique(cities)
        n = len(cities)
        add_city = cities.append
        j = 0
        while n < size and j < step:
            try:
                n = add_points(add_city, cities[i], n, size)
                i = randint(max(1, i + 1), len(cities))
            except IndexError:
                break
            j += 1
        sleep(0.0005)
    return unique(cities)


def add_points(add_city: callable,
               point: tuple,
               n: int,
               size: int) -> int:
    x, y, previous_position = point
    u, d, r = [randint(0, 1) for _ in range(3)]
    if u and n <= size and previous_position != 'down':
        add_city((x, y + 1, 'up'))
        n += 1
    if d and n <= size and previous_position != 'up':
        add_city((x, y - 1, 'down'))
        n += 1
    if r and n <= size:
        add_city((x + 1, y, 'left'))
        n += 1
    return n


def find_edges(cities: pd.DataFrame):
    cities = cities.copy()
    edges = []
    for x, y, name, _ in cities.values:
        q = f"(x=={x + 1} & y=={y}) | (x=={x - 1} & y=={y}) | (x=={x} & y=={y + 1}) | (x=={x} & y=={y - 1})"
        neighbours = cities.query(q)
        for n_name in neighbours.name:
            edges.append((name, n_name, randint(1, 24)))

    return edges


def generate_csv(size: int,
                 max_q: int = 100,
                 filename: str = 'sample',
                 save: bool = False) -> tuple:
    points = make_sample(size)

    df_cities = pd.DataFrame(points, columns=['x', 'y', 'position'])
    df_cities = df_cities.drop('position', axis=1)
    df_cities['name'] = [f'city_{i}' for i in range(df_cities.shape[0])]
    df_cities['quantity'] = [randint(0, max_q) for _ in range(df_cities.shape[0])]

    df_edges = pd.DataFrame(find_edges(df_cities), columns=['city_from', 'city_to', 'time'])
    df_cities = df_cities[['name', 'x', 'y', 'quantity']]
    if save:
        df_cities.to_csv(f'{filename}_cities.csv', index=False)
        df_edges.to_csv(f'{filename}_paths.csv', index=False)

    return df_cities, df_edges


def validate_input(cities: pd.DataFrame, paths: pd.DataFrame) -> tuple:
    # TODO: validate columns names
    unique_cities = cities.name.unique().tolist()
    unique_cities.sort()

    unique_paths = paths.city_from.unique().tolist() + paths.city_to.unique().tolist()
    unique_paths = list(set(unique_paths))
    unique_paths.sort()

    ucl = len(unique_cities)
    upl = len(unique_paths)
    if ucl > upl:
        return False, f'It seems that there are {ucl- upl} cities that are lonely islands. Take care of them!'

    if ucl < upl:
        return False, f'It seems that there are {upl-ucl} cities that are unplottable. ' \
            f'Check if each city in paths is provided with coordinates'

    # TODO: how to test it? does it make sense?
    # if unique_cities != unique_paths:
    #     return False, 'Something elements differs'

    for city_from, city_to, dist in paths.values:
        if dist < 0:
            return False, f"Distance between {city_from}-{city_to} is less than 0." \
                f" We do not support time travellers yet :<"

        if not isinstance(dist, int):
            return False,
        cf = cities[cities.name == city_from]
        if cf.shape[0] != 1:
            return False, f"Whoops! No coordinates for city {city_from} :<"

        ct = cities[cities.name == city_to]
        if ct.shape[0] != 1:
            return False, f"Whoops! No coordinates for city {city_to} :<"

        # Unpack info about city_from cf, city_to ct
        _, fx, fy, fq = cf.values[0]
        _, tx, ty, tq = ct.values[0]

        if not isinstance(fx, int):
            return False, f"Coordinate x of city {city_from} is not integer."

        if not isinstance(tx, int):
            return False, f"Coordinate x of city {city_to} is not integer."

        if not isinstance(fy, int):
            return False, f"Coordinate y of city {city_from} is not integer."

        if not isinstance(ty, int):
            return False, f"Coordinate y of city {city_to} is not integer."

        if not isinstance(fq, int):
            return False, f"Quantity in city {city_from} is not integer."

        if not isinstance(tq, int):
            return False, f"Quantity in city {city_to} is not integer."

        if fq < 0:
            return False, f"Whoops! Commodity amount in city {city_from} is below zero!:<"

        if tq < 0:
            return False, f"Whoops! Commodity amount in city {city_to} is below zero!:<"

        if abs(fx - tx) + abs(fy-ty) != 1:
            return False, f"Cities {city_from}-{city_to} are off the grid with coords ({fx},{fy}) and ({tx},{ty})."

    return True, 'Success'
