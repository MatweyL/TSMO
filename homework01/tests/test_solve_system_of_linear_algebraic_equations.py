from schemas import SystemLAE, LAE
from solver import solve_system_of_linear_algebraic_equations


def test_solve():
    system = SystemLAE([LAE.from_float([5, 6, 4]),
                        LAE.from_float([3, 5, 1])])
    print(system)
    probabilities = solve_system_of_linear_algebraic_equations(system)
    for probability in probabilities:
        if probability.state == 0:
            assert probability.value == 2
        elif probability.state == 1:
            assert probability.value == -1
