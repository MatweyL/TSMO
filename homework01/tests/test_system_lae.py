from schemas import SystemLAE, LAE


def test_sort():
    system_lae = SystemLAE([LAE.from_float([0, 2, 1, 3]),
                            LAE.from_float([0, 0, 3, 4]),
                            LAE.from_float([1, 0, 0, 4]),
                            LAE.from_float([0, 0, 0, 1])])
    system_lae.make_step_view()
    zero_number = 0
    for lae in system_lae.equations:
        assert lae.start_zeros_number == zero_number
        zero_number += 1