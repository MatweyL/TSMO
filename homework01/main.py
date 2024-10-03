import pprint
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

from api import generate_input_file, read_from_input_file
from solver import lambda_storage_to_system_lae, solve_system_of_linear_algebraic_equations


def main():
    input_file_name = "input"
    is_generated = generate_input_file(input_file_name)
    if is_generated:
        print(f"Enter values to '{input_file_name}' file and run program again")
        return
    lambda_storage = read_from_input_file(input_file_name)
    system_lae = lambda_storage_to_system_lae(lambda_storage)
    probabilities = solve_system_of_linear_algebraic_equations(system_lae)
    pprint.pprint(probabilities)


if __name__ == '__main__':
    main()
