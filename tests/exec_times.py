import time

from generator import generate_csv, validate_input


def check_time(size: int):
    name = str(size)

    tic = time.time()
    city, paths = generate_csv(size=size, filename=name, save=True)
    print(f'Prepare data: {time.time() - tic}')

    tic = time.time()
    print(validate_input(city, paths))
    print(f'Validation time: {time.time() - tic}')

    tic = time.time()
    # graph_data = tsp(cities=city,
    #                  coords=paths,
    #                  info=20)

    print(f'Solving time: {time.time() - tic}')


if __name__ == '__main__':
    check_time(500)


