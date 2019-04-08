import numpy as np
import pandas as pd


def make_matrix(df: pd.DataFrame) -> np.ndarray:
    '''
    Input :
    From  | To    | Time
    City1 | City2 | 6
    ...

    Parameters
    ----------
    df - dataframe with cities connections

    Returns
    -------
    np.ndarray - it has size N x N where N is the number
                of unique cities in the input dataframe

    '''
    assert 'from' in df.columns, "The input dataframe must have 'from' column"
    assert 'to' in df.columns, "The input dataframe must have 'to' column"
    assert 'time' in df.columns, "The input dataframe must have 'time' column"

    cities = np.sort(np.unique(np.concatenate( [df['from'].unique(), df['to'].unique()])))
    n = cities.size
    mat = np.zeros((n, n))
    for i, c1 in enumerate(cities):
        tmp = df[df['from'] == c1]
        for c2, dist in zip(tmp.to, tmp.time):
            j, = np.where(cities == c2)
            mat[i, j] = dist
            mat[j, i] = dist
    return mat


# tsp solver
def tsp(cities: pd.DataFrame, coords: pd.DataFrame, info: pd.DataFrame):
    assert isinstance(cities, pd.DataFrame), 'Wrong data format!'
    assert isinstance(coords, pd.DataFrame), 'Wrong data format!'
    assert isinstance(info, pd.DataFrame), 'Wrong data format!'

    print(cities.head())
    print(coords.head())
    print(info.head())
    print('Works')

