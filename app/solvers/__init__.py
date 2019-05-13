import pandas as pd

from .city import City
from .random_solver import solve


def make_plot_data(cities: pd.DataFrame, paths: pd.DataFrame, time: pd.DataFrame):
    solution, selected_edges = solve(cities, paths, time)

    check = lambda fc, tc: ((fc, tc) in selected_edges) or ((tc, fc) in selected_edges)

    cities = [City(name, x, y, q) for name, x, y, q in cities.values]
    edges = ((from_c, to_c, {'time': t, 'solution': check(from_c, to_c)})
             for from_c, to_c, t in paths.values)

    return solution, cities, edges
