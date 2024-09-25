from fractions import Fraction
from typing import List

from schemas import SystemLAE, Probability, LambdaStorage, LAE


def lambda_storage_to_system_lae(ls: LambdaStorage) -> SystemLAE:
    # Записываем исходную СЛАУ
    system_lae = SystemLAE([
        LAE.from_float([ls.get(0, 1) + ls.get(0, 2), -ls.get(1, 0), -ls.get(2, 0), 0, 0]),
        LAE.from_float([-ls.get(0, 1), ls.get(1, 0) + ls.get(1, 3), 0, -ls.get(3, 1), 0]),
        LAE.from_float([-ls.get(0, 2), 0, ls.get(2, 0) + ls.get(2, 3), -ls.get(3, 2), 0]),
        LAE.from_float([1, 1, 1, 1, 1])
    ])
    return system_lae


def solve_system_of_linear_algebraic_equations(system: SystemLAE) -> List[Probability]:
    equation_index = 0
    # Прямой ход
    while equation_index < system.equations_number:
        system.make_step_view()

        deductible_equation = system.equations[equation_index]
        deductible_equation.make_element_one(equation_index)

        for diminutive_equation in system.equations[equation_index + 1:]:
            diminutive_equation.make_element_one(equation_index)
            diminutive_equation.minus(deductible_equation)

        equation_index += 1

    # Обратный ход
    equation_index = system.equations_number - 1
    while equation_index > 0:

        for diminutive_equation in system.equations[equation_index - 1::-1]:
            deductible_equation = system.equations[equation_index].copy()
            deductible_equation.make_element_one(equation_index)
            diminutive_param = diminutive_equation.values[equation_index]
            deductible_equation.multiply(diminutive_param)
            diminutive_equation.minus(deductible_equation)
        equation_index -= 1

    # Получение ответа из единичной матрицы и вектора значений
    probabilities = []
    for equation in system.equations:
        for index, value in enumerate(equation.values):
            if value == 1:
                probability_value = float(equation.values[-1])
                probabilities.append(Probability(index, probability_value))
                break
    return probabilities
