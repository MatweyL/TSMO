from homework05.utils import create_numpy_meshgrid


def main():
    n = 3
    lambda_ = 4
    places_range, service_time_range = create_numpy_meshgrid(2, 100, 10, 250, 64)  # m, t_ob


if __name__ == '__main__':
    main()
