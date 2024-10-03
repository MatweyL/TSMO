from copy import copy
from typing import List

import matplotlib.pyplot as plt
import numpy as np


def solve_slae(repair_time_decrease_times: float) -> List[float]:
    lambda_01 = 1
    lambda_10 = 2 * repair_time_decrease_times
    lambda_02 = 2
    lambda_20 = 3 * repair_time_decrease_times
    lambda_13 = 2
    lambda_31 = 3 * repair_time_decrease_times
    lambda_32 = 2 * repair_time_decrease_times
    lambda_23 = 1
    A = np.array(
        [
            [-(lambda_01 + lambda_02), lambda_10, lambda_20, 0],
            [lambda_01, -(lambda_10 + lambda_13), 0, lambda_31],
            [lambda_02, 0, -(lambda_20 + lambda_23), lambda_32],
            [1, 1, 1, 1]
        ])

    # Задаем вектор правых частей
    B = np.array([0,
                  0,
                  0,
                  1])

    # Решаем систему уравнений
    X: np.ndarray = np.linalg.solve(A, B)
    probabilities = X.tolist()
    return probabilities


def calculate_cost(repair_time_decrease_times: float,
                   repair_cost_increase_times: float) -> float:
    income_1 = 10
    income_2 = 6
    repair_cost_1 = 4 * repair_cost_increase_times
    repair_cost_2 = 2 * repair_cost_increase_times
    probabilities = solve_slae(repair_time_decrease_times)
    work_probability_1 = probabilities[0]  + probabilities[2]
    work_probability_2 = probabilities[0] + probabilities[1]
    repair_probability_1 = probabilities[1]  + probabilities[3]
    repair_probability_2 = probabilities[2]  + probabilities[3]

    income = work_probability_1 * income_1 + work_probability_2 * income_2
    repair_cost = repair_probability_1 * repair_cost_1 + repair_probability_2 * repair_cost_2
    clean_income = income - repair_cost
    return clean_income



def calculate_economic_efficiency(repair_time_decrease_times: float,
                                  repair_cost_increase_times: float) -> float:
    return (calculate_cost(repair_time_decrease_times, repair_cost_increase_times) - 8.18) * 100 / 8.18


def main():
    # Создаем данные
    start = 0.1
    end = 10
    points_number = 64
    step = (end - start) / points_number
    repair_time_decrease_times = [start + i * step for i in range(points_number)]
    repair_cost_increase_times = copy(repair_time_decrease_times)
    repair_time_decrease_times, repair_cost_increase_times = np.meshgrid(repair_time_decrease_times,
                                                                         repair_cost_increase_times)
    costs = np.array([calculate_economic_efficiency(repair_decrease, cost_increase)
                      for repair_decrease, cost_increase in
                      zip(repair_time_decrease_times.flatten(), repair_cost_increase_times.flatten())])
    costs = costs.reshape(repair_time_decrease_times.shape)

    # Создаем фигуру и оси
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Строим поверхность
    ax.plot_surface(repair_time_decrease_times, repair_cost_increase_times, costs, cmap='viridis')

    # Добавляем метки осей
    ax.set_xlabel('Уменьшение времени ремонта')
    ax.set_ylabel('Увеличение стоимости ремонта')
    ax.set_zlabel('Экономическая эффективность (Д1 - Д)')

    # Показываем график
    plt.show()


if __name__ == '__main__':
    main()
