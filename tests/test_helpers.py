import pandas as pd

from app.solvers import make_plot_data
from app.solvers.random_solver import Output, solve
from app.solvers.exact_solver import exact_solve
from app.solvers.city import City


class TestSolver:
    def test_random_solver(self):
        paths = [
            {'city_from': 'A', 'city_to': 'B', 'travel_time': 1},
            {'city_from': 'B', 'city_to': 'C', 'travel_time': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
            {'name': 'C', 'x': 2, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        paths = pd.DataFrame(paths, columns=['city_from', 'city_to', 'travel_time'])

        time = pd.DataFrame([{'time': 2}])

        solution, edges = solve(cities, paths, time)

        assert isinstance(solution, Output)
        assert isinstance(edges, list)

        assert len(solution.path) == 3
        for c in solution.path:
            assert isinstance(c, City)

        assert solution.time_left == 0
        assert solution.total == 30

    def test_random_solver_time_limit(self):
        paths = [
            {'city_from': 'A', 'city_to': 'B', 'travel_time': 1},
            {'city_from': 'B', 'city_to': 'C', 'travel_time': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
            {'name': 'C', 'x': 2, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        paths = pd.DataFrame(paths, columns=['city_from', 'city_to', 'travel_time'])

        time = pd.DataFrame([{'time': 2}])

        solution, edges = solve(cities, paths, time, time_limit=-2)

        assert isinstance(solution, Output)
        assert isinstance(edges, list)

        assert len(solution.path) == 0

    def test_exact_solver(self):
        paths = [
            {'city_from': 'A', 'city_to': 'B', 'travel_time': 1},
            {'city_from': 'B', 'city_to': 'C', 'travel_time': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
            {'name': 'C', 'x': 2, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        paths = pd.DataFrame(paths, columns=['city_from', 'city_to', 'travel_time'])

        time = pd.DataFrame([{'time': 2}])

        solution, edges = exact_solve(cities, paths, time)

        assert isinstance(solution, Output)
        assert isinstance(edges, list)

        assert len(solution.path) == 2
        for c in solution.path:
            assert isinstance(c, City)

        assert solution.time_left == 0
        assert solution.total == 30

    def test_new_data(self):
        paths = [
            {'city_from': 'A', 'city_to': 'B', 'travel_time': 1},
            {'city_from': 'B', 'city_to': 'C', 'travel_time': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
            {'name': 'C', 'x': 2, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        paths = pd.DataFrame(paths, columns=['city_from', 'city_to', 'travel_time'])

        time = pd.DataFrame([{'time': 2}])

        solution, cts, edges = make_plot_data(cities, paths, time)

        assert isinstance(solution, Output)
        assert isinstance(cts, list)
        assert isinstance(edges, list)

        for c in cts:
            assert isinstance(c, City)

        for edge in edges:
            assert isinstance(edge, tuple)
            assert len(edge) == 3
            cf, ct, params = edge
            assert isinstance(ct, str)
            assert isinstance(cf, str)
            assert isinstance(params, dict)

            assert params.get('time')
            assert params.get('solution')
