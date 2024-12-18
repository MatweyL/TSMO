from homework05.main import calculate_p0
from homework05.utils import create_numpy_meshgrid


def calculate_A(lambda_: float, Q: float) -> float:
    return lambda_ * Q


def calculate_Q() -> float:
    pass


def calculate_x() -> float:
    pass


def calculate_L() -> float:
    pass


def main():
    n = 3
    lambda_ = 4
    mu = 1 / 0.5
    dashed_y = lambda_ / mu
    m_range, t_ob_range = create_numpy_meshgrid(2, 100, 10, 250, 64)  # m, t_ob
    print(calculate_p0(dashed_y, n))


if __name__ == '__main__':
    main()
