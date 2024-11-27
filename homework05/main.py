import math

import numpy as np
from matplotlib import pyplot as plt

from homework05.utils import create_numpy_meshgrid


def calculate_dashed_mu(mu: float, fi: float) -> float:
    return (mu * fi) / (mu + fi)


def calculate_dashed_y(lambda_: float, dashed_mu: float) -> float:
    return lambda_ / dashed_mu


def calculate_p0(dashed_y: float, n: int) -> float:
    return 1 / sum([1, *[dashed_y ** i / math.factorial(i) for i in range(1, n + 1)]])


def calculate_p_failures(dashed_y: float, n: int, p0: float) -> float:
    return dashed_y ** n * p0 / math.factorial(n)


def calculate_q(dashed_y: float, n: int, p0: float) -> float:
    return 1 - calculate_p_failures(dashed_y, n, p0)


def calculate_a(dashed_y: float, n: int, p0: float, lambda_: float) -> float:
    q = calculate_q(dashed_y, n, p0)
    return q * lambda_


def calculate_k_busy(a: float, dashed_mu: float) -> float:
    return a / dashed_mu


class SMOParams:
    def __init__(self, a: float, q: float, k_busy: float):
        self.a = a
        self.q = q
        self.k_busy = k_busy


def find_smo_params(n: int, lambda_: float, mu: float, fi: float) -> SMOParams:
    dashed_mu = calculate_dashed_mu(mu, fi)
    dashed_y = calculate_dashed_y(lambda_, dashed_mu)
    p0 = round(calculate_p0(dashed_y, n), 2)

    q = round(calculate_q(dashed_y, n, p0), 2)
    a = calculate_a(dashed_y, n, p0, lambda_)
    k_busy = calculate_k_busy(a, dashed_mu)

    return SMOParams(a, q, k_busy)


def assert_with_lecture_example():
    n = 2
    lambda_ = 0.2
    mu = 0.5
    fi = 2

    dashed_mu = calculate_dashed_mu(mu, fi)
    assert dashed_mu == 0.4

    dashed_y = calculate_dashed_y(lambda_, dashed_mu)
    assert dashed_y == 0.5

    p0 = round(calculate_p0(dashed_y, n), 2)
    assert p0 == 0.62

    p_failures = round(calculate_p_failures(dashed_y, n, p0), 2)
    assert p_failures == 0.08

    q = round(calculate_q(dashed_y, n, p0), 2)
    assert q == 0.92

    a = calculate_a(dashed_y, n, p0, lambda_)
    assert a == 0.1845

    k_busy = round(calculate_k_busy(a, dashed_mu), 2)
    assert k_busy == 0.46


def main():
    n = 2
    lambda_ = 0.2
    time_preparation_range, time_repairing_range = create_numpy_meshgrid(0.5, 4, 1, 5, 64)  # mu, fi
    smo_params_list = [find_smo_params(n, lambda_, mu, fi)
                       for mu, fi in zip(time_preparation_range.flatten(), time_repairing_range.flatten())]
    relative_efficiency = np.array([smo_params.q for smo_params in smo_params_list])
    absolute_efficiency = np.array([smo_params.a for smo_params in smo_params_list])
    average_busy_count = np.array([smo_params.k_busy for smo_params in smo_params_list])

    relative_efficiency = relative_efficiency.reshape(time_preparation_range.shape)
    absolute_efficiency = absolute_efficiency.reshape(time_preparation_range.shape)
    average_busy_count = average_busy_count.reshape(time_preparation_range.shape)

    fig, axes = plt.subplots(1, 3, subplot_kw={'projection': '3d'}, figsize=(14, 7))

    for ax, function_values, function_name in zip(axes,
                                                  [relative_efficiency,
                                                   absolute_efficiency,
                                                   average_busy_count],
                                                  ['Относительная эффективность',
                                                   'Абсолютная эффективность',
                                                   'Среднее число занятых каналов']):
        ax.plot_surface(time_preparation_range, time_repairing_range, function_values, cmap='viridis')
        ax.set_xlabel('Время подготовки к ремонту')
        ax.set_ylabel('Время ремонта')
        ax.set_zlabel(function_name)
        ax.set_title(function_name)
    # Показываем графики
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
