import pandas as pd
from typing import Union, Tuple

from .city import City
from .random_solver import solve, Output
from .exact_solver import exact_solve


def make_plot_data(cities: pd.DataFrame,
                   paths: pd.DataFrame,
                   time: pd.DataFrame,
                   simulations: int = 50,
                   time_limit: int = 20,
                   exact: bool = False):
    """
    Given an input, creates new solution and returns
    data in format required by app.helpers.make_graph.

    Parameters
    ----------
    cities: validated data frame with cities
    paths: validated data frame with paths
    time: validated data frame with time
    simulations: number of simulations (only for random_solver)
    time_limit: time limit for solving (in seconds)
    exact: if True then exact_solver is being used

    Returns
    -------
    Tuple[Output, list, list]
    """

    cities['name'] = cities.name.apply(lambda x: str(x))
    paths['city_from'] = paths.city_from.apply(lambda x: str(x))
    paths['city_to'] = paths.city_to.apply(lambda x: str(x))

    if exact:
        solution, selected_edges = exact_solve(cities, paths, time, time_limit)
    else:
        solution, selected_edges = solve(cities, paths, time, simulations, time_limit)

    check = lambda fc, tc: ((fc, tc) in selected_edges) or ((tc, fc) in selected_edges)

    cities = [City(name, x, y, q) for name, x, y, q in cities.values]
    edges = [(from_c, to_c, {'time': t, 'solution': check(from_c, to_c)})
             for from_c, to_c, t in paths.values]

    return solution, cities, edges


def data_from_solution(cities: Union[pd.DataFrame, None],
                       paths: Union[pd.DataFrame, None],
                       solution: Output) -> Tuple[list, list]:
    """
    Utilises provided solution and additional info for recreating
    data for app.helpers.make_graph.

    Parameters
    ----------
    cities: validated data frame with cities
    paths: validated data frame with paths
    solution: Output representing a solution

    Returns
    -------
    Tuple[list, list]
    """
    if (cities is not None) and (paths is not None):
        cities['name'] = cities.name.apply(lambda x: str(x))
        paths['city_from'] = paths.city_from.apply(lambda x: str(x))
        paths['city_to'] = paths.city_to.apply(lambda x: str(x))

        selected_edges = [(cf.name, ct.name) for cf, ct in zip(solution.path[:-1], solution.path[1:])]

        check = lambda fc, tc: ((fc, tc) in selected_edges) or ((tc, fc) in selected_edges)

        cities = [City(name, x, y, q) for name, x, y, q in cities.values]
        edges = [(from_c, to_c, {'time': t, 'solution': check(from_c, to_c)})
                 for from_c, to_c, t in paths.values]

        return cities, edges

    edges = [(cf.name, ct.name, {'time': '?', 'solution': True}) for
             cf, ct in zip(solution.path[:-1], solution.path[1:])]

    return solution.path, edges
