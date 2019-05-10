from mind.generator import validate_input, generate_csv
import pandas as pd


def make_cities(cities: list):
    return pd.DataFrame(cities, columns=['x', 'y', 'name', 'quantity'])


def make_paths(paths: list):
    return pd.DataFrame(paths, columns=['city_from', 'city_to', 'time'])


class TestValidation:
    def test_unknown_city(self):
        cities = make_cities([
            (0, 0, 'A', 1),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', 5), ('_', 'C', 5)])

        s, msg = validate_input(cities, paths)
        assert not s
        assert 'unplottable' in msg

    def test_not_connected_cities(self):
        cities = make_cities([
            (0, 0, 'A', 1),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', 5)])

        s, msg = validate_input(cities, paths)
        assert not s
        assert 'lonely' in msg

    def test_not_negative_dist(self):
        cities = make_cities([
            (0, 0, 'A', 1),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', -4), ('A', 'C', 5)])

        s, msg = validate_input(cities, paths)
        assert not s
        assert 'Distance' in msg
        assert 'less than 0.' in msg

    def test_not_coordinates1(self):
        cities = make_cities([
            (0, 0, 'A', 1),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', 4), ('D', 'A', 5)])

        s, msg = validate_input(cities, paths)
        assert not s
        assert 'No coordinates' in msg
        assert 'D' in msg

    def test_not_coordinates2(self):
        cities = make_cities([
            (0, 0, 'A', 1),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', 4), ('A', 'D', 5)])

        s, msg = validate_input(cities, paths)
        assert not s
        assert 'No coordinates' in msg
        assert 'D' in msg

    def test_x_not_int(self):
        cities = make_cities([
            ('str', 0, 'A', 1),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', 4), ('A', 'C', 5)])

        s, msg = validate_input(cities, paths)
        assert not s
        assert 'Coordinate x' in msg
        assert 'A' in msg

    def test_negative_quantity(self):
        cities = make_cities([
            (0, 0, 'A', -12),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', 4), ('A', 'C', 5)])

        s, msg = validate_input(cities, paths)
        assert not s
        assert 'Commodity amount' in msg
        assert 'A' in msg

    def test_off_grid(self):
        cities = make_cities([
            (0, 0, 'A', 12),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', 4), ('A', 'C', 5)])

        s, msg = validate_input(cities, paths)
        assert not s
        assert 'off the grid' in msg
        assert 'A' in msg
        assert 'C' in msg

    def test_success(self):
        cities = make_cities([
            (0, 0, 'A', 12),
            (0, 1, 'B', 1),
            (0, 2, 'C', 1),
        ])

        paths = make_paths([('A', 'B', 4), ('B', 'C', 5)])

        s, msg = validate_input(cities, paths)
        assert s
        assert 'Success' in msg


class TestGenerator:
    sample_range = range(3, 7)
    samples = [generate_csv(size=n) for n in sample_range]

    def test_output_size(self):
        for i, (cities, _) in zip(self.sample_range, self.samples):
            assert cities.shape[0] in [i, i+1, i-1]

    def test_is_valid(self):
        for cities, paths in self.samples:
            s, msg = validate_input(cities, paths)
            assert s
