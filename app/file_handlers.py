import pandas as pd
from collections import namedtuple

from app.solvers.solver import Output

Result = namedtuple('Result', ['status', 'msg'])


def save_solution(solution: Output, time: int) -> None:
    txt = f"{[(c.name, c.x, c.y, c.value) for c in solution.path]}\n{solution.total}\n{time - solution.time_left}"
    with open('app/tmp/solution.txt', 'w') as file:
        file.write(txt)


def validate_cities(df: pd.DataFrame) -> Result:
    if list(df.columns) != ['name', 'x', 'y', 'quantity']:
        return Result(False, 'Wrong columns names!')

    return Result(True, 'Success')


def validate_paths(df: pd.DataFrame) -> Result:
    if list(df.columns) != ['city_from', 'city_to', 'time']:
        return Result(False, 'Wrong columns names!')

    return Result(True, 'Success')


def validate_time(df: pd.DataFrame) -> Result:
    if list(df.columns) != ['time']:
        return Result(False, 'Wrong columns names!')

    if df.shape != (1, 1):
        return Result(False, 'Wrong format!')

    try:
        t = int(df.time.values[0])
    except ValueError:
        return Result(False, 'Time is not an integer!')

    return Result(True, 'Success')
