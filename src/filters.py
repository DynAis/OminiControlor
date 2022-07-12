import numpy as np

"""
a filter receives a np.array[3] and returns a np.array[3], should not have other parameters.
you can self define a filter, and then pass it to the filter_list.
"""


def half(input_vec: np.ndarray) -> np.ndarray:
    return input_vec * 0.5
