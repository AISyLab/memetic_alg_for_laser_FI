import numpy as np
import random


def randrange_float(start, stop, step, precision=0.1):
    """
    Helper function for getting random float values from a given interval with a step and precision.
    Random value is from an interval [start, stop), the value is < stop.

    :param start: lower bound for the random value, inclusive
    :param stop: upper bound for the random value, exclusive
    :param step: step of the random float values
    :param precision: precision of the float number
    :return: Random value from an interval [start, stop) with a given step and precision.
    """
    f = 1 / precision
    return random.randrange(start * f, stop * f, step * f) / f


def converter(obj):
    # added because numpy int32 and int64 are not json serializable
    # this is then a fallback function to catch those kind of objects
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj.__str__()


def closest_multiple(n, x):
    if x > n:
        return x
    n = n + int(x / 2)
    n = n - (n % x)
    return n