import numpy as np
import pandas as pd


# tsp solver
def tsp(cities: pd.DataFrame, coords: pd.DataFrame, info: pd.DataFrame):
    assert isinstance(cities, pd.DataFrame), 'Wrong data format!'
    assert isinstance(coords, pd.DataFrame), 'Wrong data format!'
    assert isinstance(info, pd.DataFrame), 'Wrong data format!'

    print(cities.head())
    print(coords.head())
    print(info.head())
    print('Works')

