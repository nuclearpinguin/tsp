import pandas as pd
import numpy as np
import base64
from collections import namedtuple, Counter

from app.solvers import Output, City

Result = namedtuple('Result', ['status', 'msg'])


def save_solution(solution: Output, time: int, new: bool = True) -> None:
    """
    Saves solution to .txt file.

    Parameters
    ----------
    solution: Output with solution data
    time: value provided in time.csv
    new: True if solution is a new solution
    """
    if new:
        txt = '['
        for c in solution.path:
            txt += f'({c.name},{c.x},{c.y},{c.value}),'
        txt = txt[:-1]
        txt += ']'
        txt += f"\n{solution.total}\n{time - solution.time_left}"
    else:
        txt = '['
        for c in solution.path:
            txt += f'({c.name},{c.x},{c.y},{c.value}),'
        txt = txt[:-1]
        txt += ']'
        txt += f"\n{solution.total}\n{time}"
    with open('app/tmp/solution.txt', 'w') as file:
        file.write(txt)


def validate_cities(df: pd.DataFrame) -> Result:
    """
    Validates cities input.

    Parameters
    ----------
    df: data frame with cities

    Returns
    -------
    True if file is valid, else False.
    """
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
    """
    Validates paths input.

    Parameters
    ----------
    df: data frame with paths
    cities: data frame with cities

    Returns
    -------
    True if file is valid, else False.
    """
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
    if ucl > upl and ucl > 1:
        return Result(False, f'It seems that there are {ucl- upl} \
        cities that are lonely islands. Take care of them!')

    if ucl < upl:
        return Result(False, f'It seems that there are {upl-ucl} cities that \
        are unplottable. Check if each city in paths is provided with coordinates')

    if unique_cities != unique_paths and ucl > 1:
        return Result(False, 'Some elements differs')

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
    """
    Validates time input.

    Parameters
    ----------
    df: data frame with time

    Returns
    -------
    True if file is valid, else False.
    """
    if list(df.columns) != ['time']:
        return Result(False, 'Wrong columns names!')

    if df.shape != (1, 1):
        return Result(False, 'Wrong format!')

    try:
        int(str(df.time.values[0]))
    except ValueError:
        return Result(False, 'Time is not an integer!')

    return Result(True, 'Success')


def parse_city(txt: str) -> City:
    """
    Parses string to a City object.
    """
    name, x, y, q = txt.split(',')
    return City(name, int(x), int(y), int(q))


def parse_cities(txt: str) -> list:
    """
    Parses line with cities to list of Cities.
    """
    txt = txt[2:-2]
    # In case of Windows shit \r\n
    if txt[-1] == ')':
        txt = txt[:-1]
    txt = txt.split('),(')
    return list(map(parse_city, txt))


def parse_solution(contents: str) -> str:
    """
    Simple decoder.
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return decoded.decode('utf-8')


def solution_to_output(content: str) -> Output:
    """
    Parses solution in text to Output.
    """
    cities, total, time = parse_solution(content).split('\n')
    return Output(time, total, parse_cities(cities))


def validate_solution(content: str) -> Result:
    """
    Validates solution input.

    Parameters
    ----------
    content: raw input (bytes?)

    Returns
    -------
    True if file is valid, else False.
    """
    try:
        parsed = parse_solution(content)
        cities, total, time = parsed.split('\n')
    except ValueError:
        return Result(False, 'Parse error. Three lines required.')

    try:
       int(str(total))
    except ValueError:
        return Result(False, 'Total is not int')

    try:
       int(str(time))
    except ValueError:
        return Result(False, 'Total is not int')

    try:
        parsed_cities = parse_cities(cities)
    except ValueError:
        return Result(False, 'Parse error. Cities list has wrong format')

    for c in parsed_cities:
        if c.value < 0:
            return Result(False, f'Quantity in city {c.name} is negative.')

    return Result(True, 'Success')
