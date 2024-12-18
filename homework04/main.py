from dataclasses import dataclass

import numpy as np
from matplotlib import pyplot as plt

from homework05.utils import create_numpy_meshgrid


def calculate_mu(t: float) -> float:
    return 1 / t


def calculate_y(lambda_: float, mu: float) -> float:
    return lambda_ / mu


def calculate_time_in_priority_queue(y: float, mu: float) -> float:
    return y / mu * (1 - y)


def calculate_disabled_time_system(time_in_priority_queue: float, t: float) -> float:
    return time_in_priority_queue + t


def calculate_wait_time_in_non_priority_queue(mu1: float, mu2: float, y1: float, y2: float) -> float:
    y = y1 + y2

    return mu2 / mu1 * (y1 / (1 - y) + y) / (mu2 * (1 - y))


def calculate_time_system_in_non_priority_queue(time_in_non_priority_queue: float, mu2: float) -> float:
    return time_in_non_priority_queue + 1 / mu2


@dataclass
class Solution:
    t_in_pq_1: float
    t_disabled1: float
    t_wait_time2: float
    t_in_non_pq2: float


def solve(lambda_1: float, lambda_2: float, t1: float, t2: float) -> Solution:
    mu1 = calculate_mu(t1)
    mu2 = calculate_mu(t2)
    y1 = calculate_y(lambda_1, mu1)
    y2 = calculate_y(lambda_2, mu2)
    t_in_pq_1 = calculate_time_in_priority_queue(y1, mu1)
    t_disabled1 = calculate_disabled_time_system(t_in_pq_1, t1)
    t_wait_time2 = calculate_wait_time_in_non_priority_queue(mu1, mu2, y1, y2)
    t_in_non_pq2 = calculate_time_system_in_non_priority_queue(t_wait_time2, mu2)
    return Solution(t_in_pq_1=t_in_pq_1,
                    t_disabled1=t_disabled1,
                    t_wait_time2=t_wait_time2,
                    t_in_non_pq2=t_in_non_pq2)


def main():
    lambda_1 = 0.1
    lambda_2 = 0.2
    t1_range, t2_range = create_numpy_meshgrid(0.5, 3, 3, 5, 64)
    solutions = [solve(lambda_1, lambda_2, t1, t2)
                 for t1, t2 in zip(t1_range.flatten(), t2_range.flatten())]
    t_in_pq_1 = np.array([solution.t_in_pq_1 for solution in solutions])
    t_disabled1 = np.array([solution.t_disabled1 for solution in solutions])
    t_wait_time2 = np.array([solution.t_wait_time2 for solution in solutions])
    t_in_non_pq2 = np.array([solution.t_in_non_pq2 for solution in solutions])

    t_in_pq_1 = t_in_pq_1.reshape(t1_range.shape)
    t_disabled1 = t_disabled1.reshape(t1_range.shape)
    t_wait_time2 = t_wait_time2.reshape(t1_range.shape)
    t_in_non_pq2 = t_in_non_pq2.reshape(t1_range.shape)
    fig, axes = plt.subplots(1,4, subplot_kw={'projection': '3d'}, figsize=(15, 10))

    for ax, function_values, function_name in zip(axes,
                                                  [t_in_pq_1,
                                                   t_disabled1,
                                                   t_wait_time2,
                                                   t_in_non_pq2],
                                                  ['Среднее время пребывания в очереди \nзаявок,\n обладающих приоритетом',
                                                   'Среднее время пребывания\n в отключенном \nсостоянии потребителей 1-ой категории',
                                                   'Среднее время ожидания\n в очереди заявки,\n не обладающей приоритетом',
                                                   'Среднее время пребывания\n в системе заявки,\n не обладающей приоритетом']):
        ax.plot_surface(t1_range, t2_range, function_values, cmap='viridis')
        ax.set_xlabel('Ср. время обсл. 1')
        ax.set_ylabel('Ср. время обсл. 2')
        # ax.set_zlabel(function_name)
        ax.set_title(function_name)
    # Показываем графики
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
