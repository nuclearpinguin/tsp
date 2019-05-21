import pandas as pd
import base64

from app.file_handlers import (validate_cities, validate_paths,
                               validate_time, Result, validate_solution,
                                save_solution, parse_solution)

from app.solvers.city import City
from app.solvers.random_solver import Output


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

    def test_cities_ok_city_numbers(self):
        xs = [
            {'name': 1, 'x': 0, 'y': 0, 'quantity': 12},
            {'name': 2, 'x': 1, 'y': 0, 'quantity': 12},
            {'name': 3, 'x': 2, 'y': 0, 'quantity': 12},
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
        assert 'x' in result.msg.lower()
        assert 'not integer' in result.msg.lower()

    def test_cities_error4(self):
        xs = [
            {'name': 'A', 'x': 1, 'y': 12.3, 'quantity': 12},
            {'name': 'B', 'x': 0, 'y': 0, 'quantity': 12},
        ]

        df = pd.DataFrame(xs, columns=['name', 'x', 'y', 'quantity'])
        result: Result = validate_cities(df)
        assert not result.status
        assert 'y' in result.msg.lower()
        assert 'not integer' in result.msg.lower()

    def test_cities_error5(self):
        xs = [
            {'name': 'A', 'x': 12, 'y': 0, 'quantity': -2},
            {'name': 'B', 'x': 0, 'y': 0, 'quantity': 12},
        ]

        df = pd.DataFrame(xs, columns=['name', 'x', 'y', 'quantity'])
        result: Result = validate_cities(df)
        assert not result.status
        assert 'below zero' in result.msg.lower()

    def test_cities_error6(self):
        xs = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 'ab'},
        ]

        df = pd.DataFrame(xs, columns=['name', 'x', 'y', 'quantity'])
        result: Result = validate_cities(df)
        assert not result.status
        assert 'amount' in result.msg.lower()
        assert 'is not integer' in result.msg.lower()


class TestPathsCsvValidation:
    def test_paths_ok(self):
        xs = [
            {'city_from': 'A', 'city_to': 'B', 'travel_time': 1},
            {'city_from': 'B', 'city_to': 'C', 'travel_time': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
            {'name': 'C', 'x': 2, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        df = pd.DataFrame(xs, columns=['city_from', 'city_to', 'travel_time'])

        result: Result = validate_paths(df, cities)
        assert result.status
        assert result.msg.lower() == 'success'

    def test_paths_ok_city_numbers(self):
        xs = [
            {'city_from': 1, 'city_to': 2, 'travel_time': 1},
            {'city_from': 2, 'city_to': 3, 'travel_time': 1},
        ]

        cities = [
            {'name': 1, 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 2, 'x': 1, 'y': 0, 'quantity': 10},
            {'name': 3, 'x': 2, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        df = pd.DataFrame(xs, columns=['city_from', 'city_to', 'travel_time'])

        result: Result = validate_paths(df, cities)
        assert result.status
        assert result.msg.lower() == 'success'

    def test_paths_error1(self):
        xs = [
            {'city_from1': 'A', 'city_to': 'B', 'travel_time': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        df = pd.DataFrame(xs, columns=['city_from1', 'city_to', 'travel_time'])

        result: Result = validate_paths(df, cities)
        assert not result.status
        assert 'wrong columns' in result.msg.lower()

    def test_paths_error2(self):
        xs = [
            {'city_from': 'A', 'city_to1': 'B', 'travel_time': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        df = pd.DataFrame(xs, columns=['city_from', 'city_to1', 'travel_time'])

        result: Result = validate_paths(df, cities)
        assert not result.status
        assert 'wrong columns' in result.msg.lower()

    def test_paths_error3(self):
        xs = [
            {'city_from': 'A', 'city_to': 'B', 'time1': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        df = pd.DataFrame(xs, columns=['city_from', 'city_to', 'time1'])

        result: Result = validate_paths(df, cities)
        assert not result.status
        assert 'wrong columns' in result.msg.lower()

    def test_paths_error4(self):
        xs = [
            {'city_from': 'A', 'city_to': 'B', 'travel_time': 1},
            {'city_from': 'A', 'city_to': 'C', 'travel_time': 1},
            {'city_from': 'A', 'city_to': 'D', 'travel_time': 1},
            {'city_from': 'A', 'city_to': 'E', 'travel_time': 1},
            {'city_from': 'A', 'city_to': 'F', 'travel_time': 1},
        ]

        cities = [
            {'name': 'A', 'x': 0, 'y': 0, 'quantity': 10},
            {'name': 'B', 'x': 1, 'y': 0, 'quantity': 10},
            {'name': 'C', 'x': 2, 'y': 0, 'quantity': 10},
            {'name': 'D', 'x': 3, 'y': 0, 'quantity': 10},
            {'name': 'E', 'x': 4, 'y': 0, 'quantity': 10},
            {'name': 'F', 'x': 5, 'y': 0, 'quantity': 10},
        ]

        cities = pd.DataFrame(cities, columns=['name', 'x', 'y', 'quantity'])
        df = pd.DataFrame(xs, columns=['city_from', 'city_to', 'travel_time'])

        result: Result = validate_paths(df, cities)
        assert not result.status
        assert 'more than 4' in result.msg.lower()


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


class TestSolution:
    @staticmethod
    def write_read(solution) -> str:
        save_solution(solution, time=20)

        with open('app/tmp/solution.txt', 'r') as file:
            contents = file.read()

        print(contents)
        contents = str.encode('filename,') + base64.b64encode(str.encode(contents))
        return contents.decode('utf8')

    @staticmethod
    def prepare(contents: str):
        contents = str.encode('filename,') + base64.b64encode(str.encode(contents))
        return contents.decode('utf8')

    def test_saving(self):
        path = [
            City(name='A', x=0, y=0),
            City(name='B', x=1, y=0)
        ]

        solution = Output(time_left=12, total=45, path=path)
        contents = self.write_read(solution)

        result: Result = validate_solution(contents)
        assert result.status
        assert result.msg.lower() == 'success'

        parsed = parse_solution(contents)
        cities, total, time = parsed.split('\n')
        assert int(total) == 45
        assert int(time) == 8

    def test_parsing(self):
        contents = self.prepare('[(name,1,2,3)]\n12\n23')

        result: Result = validate_solution(contents)
        assert result.status
        assert 'success' in result.msg.lower()

    def test_parsing_city_number(self):
        contents = self.prepare('[(12,1,2,3)]\n12\n23')

        result: Result = validate_solution(contents)
        assert result.status
        assert 'success' in result.msg.lower()

    def test_error_1(self):
        contents = self.prepare('someinfo')

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'parse error' in result.msg.lower()

    def test_error_2(self):

        contents = self.prepare('[(1,2)\n12\n23')

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'Cities list has wrong format' in result.msg

    def test_error_3(self):
        contents = self.prepare('(1,2)\n12\n23')

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'Cities list has wrong format' in result.msg

    def test_error_4(self):
        contents = self.prepare('[1,2]\n12\n23')

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'Cities list has wrong format' in result.msg

    def test_error_5(self):
        contents = self.prepare('[(1,2)]\n12\n23')

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'Cities list has wrong format' in result.msg

    def test_error_6(self):
        contents = self.prepare("[(name,x,0,2)]\n12\n23")

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'Cities list has wrong format' in result.msg

    def test_error_7(self):
        contents = self.prepare("[(name,0,y,2)]\n12\n23")

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'Cities list has wrong format' in result.msg

    def test_error_8(self):
        contents = self.prepare("[(name,0,0,q)]\n12\n23")

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'Cities list has wrong format' in result.msg

    def test_error_9(self):
        contents = self.prepare("[(name,0,0,-2)]\n12\n23")

        result: Result = validate_solution(contents)
        assert not result.status
        assert 'Quantity' in result.msg
        assert 'negative' in result.msg