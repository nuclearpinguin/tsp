from random import randint
import pandas as pd


def make_sample(size: int) -> list:
    x, y = randint(0, 100), randint(0, 100)
    start_point = (x, y, 'none')
    cities = [start_point]
    n = 1
    step = max(1, size//10)
    while n < size:
        i = -1
        cities = list(set(cities))
        n = len(cities)
        add_city = cities.append
        for _ in range(step):
            try:
                n = add_points(add_city, cities[i], n, size)
                i = randint(max(1, i + 1), len(cities))
            except IndexError:
                break
    return list(set(cities))


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


def generate_csv(size: int, max_q: int = 100, filename: str = 'sample') -> tuple:
    points = make_sample(size)

    df_cities = pd.DataFrame(points, columns=['x', 'y', 'position'])
    df_cities = df_cities.drop('position', axis=1)
    df_cities['name'] = [f'city_{i}' for i in range(df_cities.shape[0])]
    df_cities['quantity'] = [randint(0, max_q) for _ in range(df_cities.shape[0])]

    df_edges = pd.DataFrame(find_edges(df_cities), columns=['city_from', 'city_to', 'time'])
    df_cities.to_csv(f'{filename}_cities.csv', index=False)
    df_edges.to_csv(f'{filename}_paths.csv', index=False)

    return df_cities, df_edges


def validate_input(cities: pd.DataFrame, paths: pd.DataFrame) -> tuple:
    unique_cities = cities.name.unique().tolist()
    unique_cities.sort()

    unique_paths = paths.city_from.unique().tolist() + paths.city_to.unique().tolist()
    unique_paths = list(set(unique_paths))
    unique_paths.sort()

    if len(unique_cities) != len(unique_paths):
        return False, f'{len(unique_cities)} != {len(unique_paths)}'

    if unique_cities != unique_paths:
        return False, 'Some elements differs'

    return True, 'Success'
