import copy
from dataclasses import dataclass
from math import factorial

import numpy as np
from matplotlib import pyplot as plt


def calculate_p0(y: float, n: int, M: int, ) -> float:
    y_div_n = y / n

    common_sum = 0
    for i in range(n + 1):  # n - включительно
        value = y ** i / factorial(i)
        common_sum += value

    last_value = y ** (n + 1) / (n * factorial(n)) * (1 - y_div_n ** M) / (1 - y_div_n)
    p0 = 1 / (common_sum + last_value)
    return p0


def calculate_l(n: int, p0: float, y: float, M: int, ) -> float:
    return y ** (n + 1) / (n * factorial(n)) * ((1 - (y / n) ** M * (M + 1 - M / n * y)) * p0 / (1 - y / n) ** 2)


def calculate_pi(y: float, n: int, M: int, p0: float) -> float:
    return y ** (n + M) / (n ** M * factorial(n)) * p0


def calculate_A(lambda_: float, Q: float) -> float:
    return lambda_ * Q


def calculate_Q(pi: float) -> float:
    return 1 - pi


def calculate_mean_k_busy(A: float, mu: float) -> float:
    return A / mu


def calculate_m(l: float, mean_k_busy: float) -> float:
    return l + mean_k_busy


def calculate_u(mean_k_busy: float, l: float, lambda_: float) -> float:
    return (mean_k_busy + l) / lambda_


@dataclass
class SMOParams:
    Q: float  # Относительная пропускная способность
    A: float  # Абсолютная пропускная способность
    mean_k_busy: float  # Среднее число занятых кресел (парикмахеров)
    l: float  # Средняя длина очереди
    u: float  # Среднее время, которое проводит клиент в парикмахерской


def solve(n: int, M: int, lambda_: int, mu: int) -> SMOParams:
    y = lambda_ / mu
    p0 = calculate_p0(y, n, M)
    pi = calculate_pi(y, n, M, p0)
    Q = calculate_Q(pi)
    A = calculate_A(lambda_, Q)
    mean_k_busy = calculate_mean_k_busy(A, mu)
    l = calculate_l(n, p0, y, M)
    u = calculate_u(mean_k_busy, l, lambda_)
    return SMOParams(Q=Q, A=A, mean_k_busy=mean_k_busy, l=l, u=u)


def plot_smo_params(lambda_range, mu_range, smo_params_list):
    fig = plt.figure(figsize=(20, 15))

    params = ['Q', 'A', 'mean_k_busy', 'l', 'u']
    titles = ['Относительная пропускная способность', 'Абсолютная пропускная способность',
              'Среднее число занятых кресел', 'Средняя длина очереди',
              'Среднее время пребывания клиента']

    for i, param in enumerate(params, 1):
        ax = fig.add_subplot(2, 3, i, projection='3d')
        X, Y = np.meshgrid(lambda_range, mu_range)
        Z = np.array([[getattr(smo, param) for smo in smo_params_list]])

        surf = ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('λ (интенсивность входящего потока)')
        ax.set_ylabel('μ (интенсивность обслуживания)')
        ax.set_zlabel(param)
        ax.set_title(titles[i - 1])
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

    plt.tight_layout()
    plt.show()


def solve_test():
    smo_params = solve(2, 4, 2, 2 / 3)

    assert round(smo_params.Q, 2) == 0.64
    assert round(smo_params.A, 2) == 1.28
    assert round(smo_params.mean_k_busy, 2) == 1.92
    assert round(smo_params.l, 1) == 2.6
    assert round(smo_params.u, 2) == 2.25


def main():
    # Номер в списке - 18, вариант - четный => задача №2

    # Условие
    n = 3  # количество мастеров в задаче 1.2
    M = 3  # Число стульев в парикмахерской
    step = (10 - 0.1) / 64
    lambda_range = [0.1 + step * i for i in range(64)]
    mu_range = copy.copy(lambda_range)

    # Решение
    smo_params_list = [solve(n, M, lambda_, mu) for lambda_, mu in zip(lambda_range, mu_range)]

    # 5 графиков по каждому полю (зависимость от lambda_ и mu)
    plot_smo_params(lambda_range, mu_range, smo_params_list)

if __name__ == '__main__':
    main()
