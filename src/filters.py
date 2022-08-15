import numpy as np

"""
a filter receives two np.array[3] and returns a np.array[3], should not have other parameters.
you can self define a filter, and then pass it to the filter_list.
"""

def zero(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return np.zeros(3)

def x_zero(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    vec3[0] = 0
    return vec3

def y_zero(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    vec3[1] = 0
    return vec3

def z_zero(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    vec3[2] = 0
    return vec3

def amp_0_001(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 0.001

def amp_0_01(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 0.01

def amp_0_05(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 0.05

def amp_0_1(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 0.1

def amp_0_2(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 0.2

def amp_0_5(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 0.5

def amp_0_8(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 0.8

def amp_0_99(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 0.99

def amp_2(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 2 

def amp_5(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 5

def amp_10(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return vec3 * 10 

def exp(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return np.exp(vec3)

def unchange(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    return pre_vec3

def x_unchange(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    vec3[0] = pre_vec3[0]
    return vec3

def y_unchange(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    vec3[1] = pre_vec3[1]
    return vec3

def z_unchange(pre_vec3, vec3: np.ndarray) -> np.ndarray:
    vec3[2] = pre_vec3[2]
    return vec3
