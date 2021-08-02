import numpy as np
from enum import Enum


class fault_type(Enum):
    PASS = 0
    FAIL = 1
    MUTE = 2
    CHANGING = 3


class dummy_cartography:
    def apply_bench_parameter(self, parameter_set):
        x_min = 0
        x_max = 2000
        x = parameter_set.x
        y = parameter_set.y
        if x < x_min or x > x_max:
            raise ValueError(x, "is not in the allowed limits: [", x_min, ", ", x_max, "].")
        if x < x_max * 0.2:
            return np.random.choice([fault_type.PASS.value, fault_type.MUTE.value])
        if x - x_max * 0.1 < y < x + x_max * 0.1:
            return fault_type.FAIL.value
        if x > x_max * 0.5 and (x_max - x - x_max * 0.1 < y < x_max - x + x_max * 0.1):
            return fault_type.MUTE.value
        return fault_type.PASS.value


def apply_bench_params(x, y, d, pw, i):
    """
    Takes bench parameters and returns the device response.
    The function should connect to the bench and perform the laser attacks with the given parameter set.

    :param x: x position
    :param y: y position
    :param d: trigger delay
    :param pw: power width
    :param i: intensity of the laser
    :return: reader status, command status
    """
    # TODO: implement actual real LFI (connection to bench, actual responses from device...)
    x_min = 0
    x_max = 2000
    if x < x_min or x > x_max:
        raise ValueError(x, "is not in the allowed limits: [", x_min, ", ", x_max, "].")
    if x < x_max * 0.2:
        return np.random.choice([fault_type.PASS.value, fault_type.MUTE.value]), ""
    if x - x_max * 0.1 < y < x + x_max * 0.1:
        return fault_type.FAIL.value, ""
    if x > x_max * 0.5 and (x_max - x - x_max * 0.1 < y < x_max - x + x_max * 0.1):
        return fault_type.MUTE.value, ""
    return fault_type.PASS.value, ""


def dummy_apply_on_bench(x, y, d, pw, i):
    """
    Takes bench parameters and returns the device response.
    The function should connect to the bench and perform the laser attacks with the given parameter set.

    :param x: x position
    :param y: y position
    :param d: trigger delay
    :param pw: power width
    :param i: intensity of the laser
    :return: reader status, command status
    """
    x_min = 0
    x_max = 2000
    if x < x_min or x > x_max:
        raise ValueError(x, "is not in the allowed limits: [", x_min, ", ", x_max, "].")
    if x < x_max * 0.2:
        return np.random.choice([fault_type.PASS.value, fault_type.MUTE.value]), ""
    if x - x_max * 0.1 < y < x + x_max * 0.1:
        return fault_type.FAIL.value, ""
    if x > x_max * 0.5 and (x_max - x - x_max * 0.1 < y < x_max - x + x_max * 0.1):
        return fault_type.MUTE.value, ""
    return fault_type.PASS.value, ""