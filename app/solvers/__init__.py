import pandas as pd
from typing import Union, Tuple

from .city import City
from .random_solver import solve, Output


def make_plot_data(cities: pd.DataFrame,
                   paths: pd.DataFrame,
                   time: pd.DataFrame,
                   simulations: int = 50,
                   time_limit: int = 20):
    solution, selected_edges = solve(cities, paths, time, simulations, time_limit)

    check = lambda fc, tc: ((fc, tc) in selected_edges) or ((tc, fc) in selected_edges)

    cities = [City(name, x, y, q) for name, x, y, q in cities.values]
    edges = ((from_c, to_c, {'time': t, 'solution': check(from_c, to_c)})
             for from_c, to_c, t in paths.values)

    return solution, cities, edges


def data_from_solution(cities: Union[pd.DataFrame, None],
                       paths: Union[pd.DataFrame, None],
                       solution: Output) -> Tuple[list, list]:
    if (cities is not None) and (paths is not None):
        selected_edges = [(cf.name, ct.name) for cf, ct in zip(solution.path[:-1], solution.path[1:])]

        check = lambda fc, tc: ((fc, tc) in selected_edges) or ((tc, fc) in selected_edges)

        cities = [City(name, x, y, q) for name, x, y, q in cities.values]
        edges = [(from_c, to_c, {'time': t, 'solution': check(from_c, to_c)})
                 for from_c, to_c, t in paths.values]

        return cities, edges

    edges = [(cf.name, ct.name, {'time': '?', 'solution': True}) for
             cf, ct in zip(solution.path[:-1], solution.path[1:])]

    return solution.path, edges
