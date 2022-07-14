import numpy as np

"""
a filter receives a np.array[3] and returns a np.array[3], should not have other parameters.
you can self define a filter, and then pass it to the filter_list.
"""

def zero(input_vec: np.ndarray) -> np.ndarray:
    return np.zeros(3)

def amp_0_2(input_vec: np.ndarray) -> np.ndarray:
    return input_vec * 0.2

def amp_0_5(input_vec: np.ndarray) -> np.ndarray:
    return input_vec * 0.5

def amp_0_8(input_vec: np.ndarray) -> np.ndarray:
    return input_vec * 0.8

def amp_0_99(input_vec: np.ndarray) -> np.ndarray:
    return input_vec * 0.99

def exp(input_vec: np.ndarray) -> np.ndarray:
    return np.exp(input_vec)
