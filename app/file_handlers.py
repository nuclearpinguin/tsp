import pandas as pd
import numpy as np
import base64
from collections import namedtuple, Counter

from app.solvers import Output, City

Result = namedtuple('Result', ['status', 'msg'])


def save_solution(solution: Output, time: int, new: bool = True) -> None:
    if new:
        txt = f"{[(c.name, c.x, c.y, c.value) for c in solution.path]}\n{solution.total}\n{time - solution.time_left}"
    else:
        txt = f"{[(c.name, c.x, c.y, c.value) for c in solution.path]}\n{solution.total}\n{time}"
    with open('app/tmp/solution.txt', 'w') as file:
        file.write(txt)


def validate_cities(df: pd.DataFrame) -> Result:
    if list(df.columns) != ['name', 'x', 'y', 'quantity']:
        return Result(False, 'Wrong columns names!')

    if df.shape[0] != df.name.unique().size:
        return Result(False, f"Whoops! It seems that some cities are duplicated!")

    for name, x, y, q in df.values:
        try:
            int(str(q))
        except ValueError:
            return Result(False, f"Whoops! Commodity amount in city {name} is not integer! :<")

        if q < 0:
            return Result(False, f"Whoops! Commodity amount in city {name} is below zero! :<")

        try:
            int(str(x))
        except ValueError:
            return Result(False, f"Whoops! Coordinate x in city {name} is not integer! :<")

        try:
            int(str(y))
        except ValueError:
            return Result(False, f"Whoops! Coordinate y in city {name} is not integer! :<")

    return Result(True, 'Success')


def validate_paths(df: pd.DataFrame, cities: pd.DataFrame) -> Result:
    if list(df.columns) != ['city_from', 'city_to', 'travel_time']:
        return Result(False, 'Wrong columns names!')

    # Each city can have at most 4 neighbours
    cntr = Counter(np.concatenate([df.city_from.values, df.city_to.values]))
    check = sum(x for x in cntr.values() if x > 4)
    if check > 0:
        return Result(False, f"Whoops! At least one city has more than 4 neighbours! :o")

    # General check for paths and cities
    unique_cities = cities.name.unique().tolist()
    unique_cities.sort()

    unique_paths = df.city_from.unique().tolist() + df.city_to.unique().tolist()
    unique_paths = list(set(unique_paths))

    unique_paths.sort()

    ucl = len(unique_cities)
    upl = len(unique_paths)
    if ucl > upl:
        return Result(False, f'It seems that there are {ucl- upl} \
        cities that are lonely islands. Take care of them!')

    if ucl < upl:
        return Result(False, f'It seems that there are {upl-ucl} cities that \
        are unplottable. Check if each city in paths is provided with coordinates')

    if unique_cities != unique_paths:
        return Result(False, 'Something elements differs')

    for city_from, city_to, dist in df.values:
        try:
            int(str(dist))
        except ValueError:
            return Result(False, f"Whoops! Distance between {city_from}-{city_to} is not integer! :<")

        if dist < 0:
            return Result(False, f"Distance between {city_from}-{city_to} is less than 0. \
             We do not support time travellers yet :<")

        # Validate relation between cities and paths
        cf = cities[cities.name == city_from]
        if cf.shape[0] != 1:
            return Result(False, f"Whoops! No coordinates for city {city_from} :<")

        ct = cities[cities.name == city_to]
        if ct.shape[0] != 1:
            return Result(False, f"Whoops! No coordinates for city {city_to} :<")

        # Unpack info about city_from cf, city_to ct
        _, fx, fy, fq = cf.values[0]
        _, tx, ty, tq = ct.values[0]

        if abs(fx - tx) + abs(fy-ty) != 1:
            return Result(False, f"Cities {city_from}-{city_to} are off \
            the grid with coords ({fx},{fy}) and ({tx},{ty}).")

    return Result(True, 'Success')


def validate_time(df: pd.DataFrame) -> Result:
    if list(df.columns) != ['time']:
        return Result(False, 'Wrong columns names!')

    if df.shape != (1, 1):
        return Result(False, 'Wrong format!')

    try:
        int(str(df.time.values[0]))
    except ValueError:
        return Result(False, 'Time is not an integer!')

    return Result(True, 'Success')


def parse_solution(contents: str) -> str:
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return decoded.decode('utf-8')


def solution_to_output(content: str) -> Output:
    cities, total, time = parse_solution(content).split('\n')
    return Output(time, total, [City(name, x, y, q) for name, x, y, q in eval(cities)])


def validate_solution(content: str) -> Result:
    try:
        parsed = parse_solution(content)
        cities, total, time = parsed.split('\n')
    except ValueError:
        return Result(False, f'Parse error. Input has wrong format!')

    try:
        cities = eval(cities)
    except SyntaxError:
        return Result(False, f'Parse error. Cities list has wrong format')

    if not isinstance(cities, list):
        return Result(False, f'Parse error. Cities list has wrong format')

    for i, c in enumerate(cities):
        if not isinstance(c, tuple):
            return Result(False, f'Parse error. City {i} is not a tuple.')

        if len(c) != 4:
            return Result(False, f'Parse error. City {i} is not a 4-tuple.')

        name, x, y, q = c
        try:
            int(str(x))
        except ValueError:
            return Result(False, f'Coordinate x of city {name} is not an integer.')

        try:
            int(str(y))
        except ValueError:
            return Result(False, f'Coordinate y of city {name} is not an integer.')

        try:
            int(str(q))
        except ValueError:
            return Result(False, f'Quantity in city {name} is not an integer.')

        if q < 0:
            return Result(False, f'Quantity in city {name} has negative value')

    return Result(True, 'Success')
