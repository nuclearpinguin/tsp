import time
import pandas as pd

from app.solver import tsp
from mind.generator import generate_csv


def check_time(size: int):
    name = 'time_test'

    tic = time.time()
    generate_csv(size=size, filename=name)
    print(f'Prepare data: {time.time() - tic}')

    tic = time.time()
    city = pd.read_csv(f'{name}_cities.csv')
    paths = pd.read_csv(f'{name}_paths.csv')

    print(f'Cities number: {city.shape[0]}')
    # graph_data = tsp(cities=city,
    #                  coords=paths,
    #                  info=20)

    print(f'Solving time: {time.time() - tic}')


if __name__ == '__main__':
    check_time(5000)


