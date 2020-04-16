from numpy.core.records import ndarray
from numpy.ma import empty, append, array


def fill(destination: ndarray, source: ndarray):
    predictable_size: int

    if destination.size == 0:
        return array([array([member]) for member in source])
    else:
        predictable_size: int = destination.shape[1] + 1

    result: ndarray = empty((0, predictable_size), complex)

    for to_append in destination:
        for item in source:
            to_store = append(to_append, item)
            result = append(result, array([to_store]), axis=0)
    return result
