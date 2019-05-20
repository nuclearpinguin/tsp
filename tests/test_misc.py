import pandas as pd

from app.file_handlers import validate_cities, validate_paths, validate_time, Result


class TestCityCsvValidation:
    def test_cities_ok(self):
        xs = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 12},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 12},
            {'name': 'C', 'x': 2, 'y': 0, 'quantity': 12},
        ]

        df = pd.DataFrame(xs, columns=['name', 'x', 'y', 'quantity'])
        print(df.columns)

        result: Result = validate_cities(df)
        assert result.status
        assert result.msg.lower() == 'success'

    def test_cities_error1(self):
        xs = [
            {'name1': 'A', 'x': 0, 'y': 0, 'quantity': 12},
        ]

        df = pd.DataFrame(xs)
        result: Result = validate_cities(df)
        assert not result.status
        assert 'wrong columns' in result.msg.lower()

    def test_cities_error2(self):
        xs = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 12},
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 12},
        ]

        df = pd.DataFrame(xs, columns=['name', 'x', 'y', 'quantity'])
        result: Result = validate_cities(df)
        assert not result.status
        assert 'duplicated' in result.msg.lower()

    def test_cities_error3(self):
        xs = [
            {'name': 'A', 'x': 12.3, 'y': 0, 'quantity': 12},
            {'name': 'B', 'x': 0, 'y': 0, 'quantity': 12},
        ]

        df = pd.DataFrame(xs, columns=['name', 'x', 'y', 'quantity'])
        result: Result = validate_cities(df)
        assert not result.status
        assert 'not integer' in result.msg.lower()

    def test_cities_error4(self):
        xs = [
            {'name': 'A', 'x': 12, 'y': 0, 'quantity': -2},
            {'name': 'B', 'x': 0, 'y': 0, 'quantity': 12},
        ]

        df = pd.DataFrame(xs, columns=['name', 'x', 'y', 'quantity'])
        result: Result = validate_cities(df)
        assert not result.status
        assert 'below zero' in result.msg.lower()


class TestPathsCsvValidation:
    def test_paths_ok(self):
        xs = [
            {'city_from': 'A', 'city_to': 'B', 'time': 1},
            {'city_from': 'B', 'city_to': 'C', 'time': 1},
        ]

        df = pd.DataFrame(xs, columns=['city_from', 'city_to', 'time'])
        result: Result = validate_paths(df)
        assert result.status
        assert result.msg.lower() == 'success'

    def test_paths_error1(self):
        xs = [
            {'city_from1': 'A', 'city_to': 'B', 'time': 1},
        ]

        df = pd.DataFrame(xs)
        result: Result = validate_paths(df)
        assert not result.status
        assert 'wrong columns' in result.msg.lower()

    def test_paths_error2(self):
        xs = [
            {'city_from': 'A', 'city_to1': 'B', 'time': 1},
        ]

        df = pd.DataFrame(xs)
        result: Result = validate_paths(df)
        assert not result.status
        assert 'wrong columns' in result.msg.lower()

    def test_paths_error3(self):
        xs = [
            {'city_from': 'A', 'city_to': 'B', 'time1': 1},
        ]

        df = pd.DataFrame(xs)
        result: Result = validate_paths(df)
        assert not result.status
        assert 'wrong columns' in result.msg.lower()


class TestTimeCsvValidation:
    def test_ok(self):
        df = pd.DataFrame([{'time': 12}])
        result: Result = validate_time(df)
        assert result.status
        assert result.msg.lower() == 'success'

    def test_error1(self):
        df = pd.DataFrame([{'tim1e': 12}])
        result: Result = validate_time(df)
        assert not result.status
        assert 'wrong columns' in result.msg.lower()

    def test_error2(self):
        df = pd.DataFrame([{'time': 'test'}, {'time': 'test'}])
        result: Result = validate_time(df)
        assert not result.status
        assert 'wrong format' in result.msg.lower()

    def test_error3(self):
        df = pd.DataFrame([{'time': 'test'}])
        result: Result = validate_time(df)
        assert not result.status
        assert 'not an integer' in result.msg.lower()

        df = pd.DataFrame([{'time': 12.34}])
        result: Result = validate_time(df)
        assert not result.status
        assert 'not an integer' in result.msg.lower()
