from fractions import Fraction
from pathlib import Path

from schemas import LambdaStorage, States, Lambda


def generate_input_file(name: str) -> bool:
    input_file = Path(name)
    if input_file.exists():
        return False
    states = States([0, 2, 3, 1])
    input_lines = []
    for left_state, state, right_state in states.iter_state():
        value_to_state_from_left = f'Lambda({left_state} -> {state}): '
        value_to_state_from_right = f'Lambda({right_state} -> {state}): '
        input_lines.append(value_to_state_from_left)
        input_lines.append(value_to_state_from_right)
    input_text = '\n'.join(input_lines)
    input_file.write_text(input_text)
    return True


def get_value_from_string(value_string: str):
    try:
        value = Fraction(float(value_string))
    except ValueError:
        slash_index = value_string.find('/')
        numerator = int(value_string[:slash_index].strip())
        denominator = int(value_string[slash_index + 1:].strip())
        value = Fraction(numerator, denominator)
    return value


def read_from_input_file(name: str) -> LambdaStorage:
    lambda_storage = LambdaStorage()
    lines = Path(name).read_text('utf-8').split('\n')
    for line in lines:
        value_start_index = line.find(':')
        to_state_start_index = line.find('->')
        from_state_start_index = line.find('(')
        value = get_value_from_string(line[value_start_index + 2:].strip())
        from_state = int(line[from_state_start_index + 1:to_state_start_index].strip())
        to_state = int(line[to_state_start_index + 2:value_start_index - 1].strip())
        lambda_to_state = Lambda(from_state, to_state, value)
        lambda_storage.append(lambda_to_state)
    return lambda_storage


def read_from_console() -> LambdaStorage:
    lambda_storage = LambdaStorage()
    states = States([0, 2, 3, 1])
    for left_state, state, right_state in states.iter_state():
        value_to_state_from_left = get_value_from_string(input(f'State {state}. Enter value of Lambda({left_state} -> {state}): '))
        value_to_state_from_right = get_value_from_string(input(f'State {state}. Enter value of Lambda({right_state} -> {state}): '))
        lambda_to_state_from_left = Lambda(left_state, state, value_to_state_from_left)
        lambda_to_state_from_right = Lambda(right_state, state, value_to_state_from_right)
        lambda_storage.append(lambda_to_state_from_left)
        lambda_storage.append(lambda_to_state_from_right)
    return lambda_storage
