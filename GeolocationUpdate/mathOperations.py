from math import sqrt as _sqrt


def cross(vector1, vector2):
    r"""
    Returns the Crossproduct of vector2

    :param list vector1: three-dimensional vector
    :param list vector2: three-dimensional vector
    :return: list

    """
    if type(vector1) != list or type(vector2) != list:
        raise TypeError("Error: Input args must be from type list!")
    if len(vector1) != 3 or len(vector2) != 3:
        raise TypeError("Error: Input args must have len 3!")
    elif len(vector1) != len(vector2):
        raise ValueError("Error: Input args must have same length!")

    ax, ay, az = vector1
    bx, by, bz = vector2

    cx = ay * bz - az * by
    cy = az * bx - ax * bz
    cz = ax * by - ay * bx
    vector3 = [cx, cy, cz]
    return vector3


def norm(vector1):
    r"""
    Length of vector1.

    :param list vector1: two-/ or three-dimensional vector
    :return: float

    """
    if type(vector1) != list:
        raise TypeError("Error: Input args must be from type list!")
    elif len(vector1) not in [2, 3]:
        raise TypeError("Error: Length from input args are not 2 or 3!")

    x = vector1[0]
    y = vector1[1]
    if len(vector1) == 3:
        z = vector1[2]
    else:
        z = 0

    vecNorm = float(_sqrt(x ** 2 + y ** 2 + z ** 2))

    return vecNorm


def diff(vector1, vector2):
    r"""
    Build difference of vector1 and vector2

    :param list vector1: two-/ or three-dimensional vector
    :param list vector2: two-/ or three-dimensional vector
    :return: list

    """
    if type(vector1) != list or type(vector2) != list:
        raise TypeError("Error: Input args must be from type list!")
    elif len(vector1) not in [2, 3] or len(vector2) not in [2, 3]:
        raise TypeError("Error: Length from input args are not 2 or 3!")
    elif len(vector1) != len(vector2):
        raise ValueError("Error: Input args must have same length!")

    x = vector1[0] - vector2[0]
    y = vector1[1] - vector2[1]
    if len(vector1) == 3:
        z = vector1[2] - vector2[2]

        vector3 = [x, y, z]
    else:
        vector3 = [x, y]

    return vector3


def scalar_multiplication(scalar, vector1):
    r"""
    Scalar multiplication from scalar and vector1.

    :param float scalar: scalar
    :param list vector1: two-/ or three-dimensional vector
    :return: list

    """
    if type(scalar) != float:
        raise TypeError("Error: scalar must be from type float!")
    elif type(vector1) != list:
        raise TypeError("Error: vector1 must be from type list!")
    elif len(vector1) not in [2, 3]:
        raise ValueError("Error: len from vector1 must be 2 or 3!")

    x = scalar * vector1[0]
    y = scalar * vector1[1]
    if len(vector1) == 3:
        z = scalar * vector1[2]
        vector2 = [x, y, z]
    else:
        vector2 = [x, y]
    return vector2
