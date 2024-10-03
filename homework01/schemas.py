from fractions import Fraction
from typing import Dict, List


class LambdaIndex:
    def __init__(self,
                 from_state: int,
                 to_state: int, ):
        self.from_state = from_state
        self.to_state = to_state

    def __eq__(self, other):
        return self.from_state == other.from_state and self.to_state == other.to_state

    def __hash__(self):
        return hash(f"{self.from_state}{self.to_state}")

    def __repr__(self):
        return f"LambdaIndex({self.from_state} -> {self.to_state})"


class Lambda(LambdaIndex):
    def __init__(self, from_state: int, to_state: int, value: Fraction, ):
        super().__init__(from_state, to_state)
        self.value = value

    def __repr__(self):
        return f"L({self.from_state} -> {self.to_state})={self.value}"


class LambdaStorage:

    def __init__(self):
        self._lambda_by_index: Dict[LambdaIndex, Lambda] = {}

    def append(self, l: Lambda):
        self._lambda_by_index[l] = l

    def get(self, from_state: int, to_state: int) -> Fraction:
        l_index = LambdaIndex(from_state, to_state)
        return self._lambda_by_index[l_index].value


class Probability:

    def __init__(self, state: int, value: float):
        self.state = state
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Probability):

            return other.state == self.state
        elif isinstance(other, float):
            return other == self.state
        else:
            raise TypeError(f'Cannot compare {type(self)} and {type(other)}')

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return f"P({self.state})={self.value}"


class States:

    def __init__(self, clockwise_states: List[int]):
        self._clockwise_states = clockwise_states

    def iter_state(self):
        for state_index, state in enumerate(self._clockwise_states):
            left_state_index = state_index - 1
            right_state_index = state_index + 1
            if left_state_index < 0:
                left_state_index = len(self._clockwise_states) - 1
            if right_state_index >= len(self._clockwise_states):
                right_state_index = 0
            left_state = self._clockwise_states[left_state_index]
            right_state = self._clockwise_states[right_state_index]
            yield left_state, state, right_state


class LAE:

    def __repr__(self):
        return f'{self.values}'

    def __init__(self, values: List[Fraction]):
        self.values = values

    def multiply(self, multiplier: Fraction):
        for index, value in enumerate(self.values):
            self.values[index] = value * multiplier

    def divide(self, divider: Fraction):
        if divider == 0:
            return
        for index, value in enumerate(self.values):
            self.values[index] = value / divider

    def minus(self, lae: 'LAE'):
        for index, value in enumerate(self.values):
            self.values[index] = value - lae.values[index]

    def plus(self, lae: 'LAE'):
        for index, value in enumerate(self.values):
            self.values[index] = value + lae.values[index]

    def make_element_one(self, index: int):
        divider = self.values[index]
        self.divide(divider)

    def copy(self) -> 'LAE':
        return LAE([Fraction(value) for value in self.values])

    @property
    def start_zeros_number(self):
        number = 0
        for value in self.values:
            if value == 0:
                number += 1
            else:
                break
        return number

    @staticmethod
    def from_float(values: List[float]) -> 'LAE':
        return LAE([Fraction(value) for value in values])


class SystemLAE:

    def __repr__(self):
        return "\n".join([str(equation) for equation in self.equations])

    def __init__(self, equations: List[LAE]):
        self.equations = equations
        self._equations_number = len(self.equations)
        self._variables_number = len(self.equations[0].values)

    @property
    def equations_number(self):
        return self._equations_number

    @property
    def variables_number(self):
        return self._variables_number

    def make_step_view(self):
        self.equations.sort(key=lambda lae: lae.start_zeros_number)
