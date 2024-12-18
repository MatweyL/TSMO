from dataclasses import dataclass

import numpy as np
from matplotlib import pyplot as plt

from homework03.main import calculate_p0, calculate_pi
from homework05.utils import create_numpy_meshgrid


def calculate_A(lambda_: float, Q: float) -> float:
    return lambda_ * Q


def calculate_Q_without_mutual_assistance(p_failure: float) -> float:
    return 1 - p_failure


def calculate_Q_with_mutual_assistance(y: float, n: float, m: float) -> float:
    xsi = y / n
    return (1 - xsi ** (n + m)) / (1 - xsi ** (n + m + 1))


@dataclass
class Solution:
    Q1: float
    A1: float
    Q2: float
    A2: float


def solve(n: int, lambda_: int, m: float, t_ob: float) -> Solution:
    mu = 1 / t_ob
    y = lambda_ / mu
    p0 = calculate_p0(y, n, m)
    p_failure = calculate_pi(y, n, m, p0)
    Q1 = calculate_Q_without_mutual_assistance(p_failure)
    A1 = calculate_A(lambda_, Q1)
    Q2 = calculate_Q_with_mutual_assistance(y, n, m)
    A2 = calculate_A(lambda_, Q2)
    return Solution(Q1=Q1, A1=A1, Q2=Q2, A2=A2)


def main():
    n = 3
    lambda_ = 4
    m_range, t_ob_range = create_numpy_meshgrid(2, 100, 10, 250, 64)  # m, t_ob

    solutions = [solve(n, lambda_, m, t_ob)
                 for m, t_ob in zip(m_range.flatten(), t_ob_range.flatten())]
    Q1 = np.array([solution.Q1 for solution in solutions])
    A1 = np.array([solution.A1 for solution in solutions])
    Q2 = np.array([solution.Q2 for solution in solutions])
    A2 = np.array([solution.A2 for solution in solutions])

    Q1 = Q1.reshape(m_range.shape)
    A1 = A1.reshape(m_range.shape)
    Q2 = Q2.reshape(m_range.shape)
    A2 = A2.reshape(m_range.shape)
    fig, axes = plt.subplots(1, 4, subplot_kw={'projection': '3d'}, figsize=(15, 10))

    for ax, function_values, function_name in zip(axes,
                                                  [Q1,
                                                   A1,
                                                   Q2,
                                                   A2],
                                                  [
                                                      'Относительная пропускная \nспособность без взаимопомощи',
                                                      'Абсолютная пропускная \nспособность без взаимопомощи',
                                                      'Относительная пропускная \nспособность с \nравномерной взаимопомощью',
                                                      'Абсолютная пропускная \nспособность с \nравномерной взаимопомощью']):
        ax.plot_surface(m_range, t_ob_range, function_values, cmap='viridis')
        ax.set_xlabel('Ср. время обсл.')
        ax.set_ylabel('Макс. кол-во заявок')
        ax.set_title(function_name)
    # Показываем графики
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
