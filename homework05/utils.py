from typing import Tuple

import numpy
import numpy as np


def create_numpy_meshgrid(x_start: float, x_end: float,
                          y_start: float, y_end: float,
                          points_number: float, ) -> Tuple[numpy.ndarray, numpy.ndarray]:
    x_step = (x_end - x_start) / points_number
    x_range = [x_start + i * x_step for i in range(points_number)]
    y_step = (y_end - y_start) / points_number
    y_range = [y_start + i * y_step for i in range(points_number)]
    return np.meshgrid(x_range, y_range)
