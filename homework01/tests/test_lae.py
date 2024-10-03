from fractions import Fraction

from schemas import LAE


def test_start_zero_number():
    lae_0_nulls = LAE.from_float([1, 2, 3, 0])
    lae_1_nulls = LAE.from_float([0, 1, 0, 2, 3, 0])
    lae_2_nulls = LAE.from_float([0, 0, 1, 2, 3])

    assert lae_0_nulls.start_zeros_number == 0
    assert lae_1_nulls.start_zeros_number == 1
    assert lae_2_nulls.start_zeros_number == 2


def test_multiply():
    source_list =  [1, 2, 3, 4]
    lae = LAE.from_float(source_list)
    multiplier = Fraction(2)
    lae.multiply(multiplier)
    for index, value in enumerate(lae.values):
        assert source_list[index] == value / 2

def test_divide():
    source_list =  [2, 4, 8]
    lae = LAE.from_float(source_list)
    divider = Fraction(2)
    lae.divide(divider)
    for index, value in enumerate(lae.values):
        assert source_list[index] == value * 2


def test_plus():
    list_1 =  [2, 4, 8]
    list_2 = [1, 2, 4]
    lae_1 = LAE.from_float(list_1)
    lae_2 = LAE.from_float(list_2)
    lae_1.plus(lae_2)
    for index, value in enumerate(lae_1.values):
        assert list_1[index] + list_2[index] == value

def test_minus():
    list_1 =  [2, 4, 8]
    list_2 = [1, 2, 4]
    lae_1 = LAE.from_float(list_1)
    lae_2 = LAE.from_float(list_2)
    lae_1.minus(lae_2)
    for index, value in enumerate(lae_1.values):
        assert list_1[index] - list_2[index] == value
