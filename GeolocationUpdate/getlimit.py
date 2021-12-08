# -*- coding: utf-8 -*-

# GeolocationUpdate
# -----------------
# Know your limits! (created by auxilium)
#
# Author:   Dilara Goeksu
# Version:  0.1, copyright Wednesday, 01 December 2021
# Website:  https://github.com/Dilara Goeksu/Geolocation
# License:  Apache License 2.0 (see LICENSE file)

from math import atan2 as _arctan2
from math import pi as _pi
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
        raise ValueError("Error: Input args must have len 3!")

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
        raise ValueError("Error: Length from input args are not 2 or 3!")

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
        raise ValueError("Error: Length from input args are not 2 or 3!")
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


def s_mul(scalar, vector1):
    r"""
    Scalar multiplication from scalar and vector1.

    :param float scalar: scalar
    :param list vector1: two-/ or three-dimensional vector
    :return: list

    """
    if type(scalar) != float and type(scalar) != int:
        raise TypeError("Error: scalar must be from type float or integer!")
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


def angle_north(point1, point2):
    r"""
    Returns the clockwise angle (in degree) between the vector
    from point1 to point2 and the vector (0, 1).

    :param list point1: first two-dimensional vector
    :param list point2: second two-dimensional vector
    :returns: float

    """
    if type(point1) != list or type(point2) != list:
        raise TypeError("Input args must be from type list!")
    if len(point1) != 2 or len(point2) != 2:
        raise ValueError("Input args must have length 2!")
    # v2 equals the vektor that connects point1 and point2
    v2 = [point2[0] - point1[0], point2[1] - point1[1]]
    angle_rad = _arctan2(v2[0], v2[1])
    angle_degree = angle_rad / (2 * _pi) * 360
    if angle_degree < 0:
        angle_degree = 360 + angle_degree
    return angle_degree


def find_distance(point, line_point1, line_point2):
    r"""
    Finds the distance between point and
    the vector between line_point1 and line_point2.

    :param list point: two-dimensional vector
    :param list line_point1: two-dimensional vector
    :param list line_point2: two-dimensional vector
    :returns: float

    """
    # input Points
    hom_point = [point[0], point[1], 1]
    point1 = [line_point1[0], line_point1[1], 1]
    point2 = [line_point2[0], line_point2[1], 1]

    # berechne Richtungsvektor für Gerade aus point1
    # und point2
    line_dir = diff(point2, point1)

    # Normalenrichtungsverktor  und Normalenvektor
    # in impliziter Form
    impl_line = [line_dir[1], -1 * line_dir[0], 0]

    # Kreuzprodukt der beiden Normalenvektoren
    # zwischen Gerade (hom_point, impl_line)
    # und der Geraden (point1, point2)
    # ist Punkt mit kleinstem Abstand zwischen
    # Gerade impl_1nd_line und hom_point
    impl_1st_line = cross(point1, line_dir)
    impl_2nd_line = cross(hom_point, impl_line)

    point3 = cross(impl_1st_line, impl_2nd_line)
    n_point3 = s_mul(float(1 / point3[2]), point3)

    # aus beiden Punkten einen Vektor machen,
    # von diesem Vektor die Länge nehmen
    line_dist = norm(diff(n_point3, hom_point))

    return line_dist


def get_limit(latitude, longitude, speed, direction, get_ways):
    r"""
    Get the limit and possible ways.

    :param float latitude: Latitude of current location
    :param float longitude: Longitude of current location
    :param float speed: Speed of driver
    :param float direction: Direction of driver
    :param function get_ways: function handle to get possible ways:
    :returns: speed(float), ways(tuple)

    """
    # get ways near-by
    all_ways = get_ways(latitude, longitude, radius=30)
    list1 = []
    list2 = []
    for i in all_ways:
        # i is way object
        point_self = [longitude, latitude]
        point1 = [i.geometry[0].longitude, i.geometry[0].latitude]
        point2 = [i.geometry[1].longitude, i.geometry[1].latitude]

        distance = find_distance(point=point_self,
                                 line_point1=point1,
                                 line_point2=point2)

        angle = angle_north(point1, point2)
        angle_diff = abs(angle-direction)

        # print(distance)
        list1.append((distance, angle_diff, i))
        list2.append((distance, angle_diff, i))
    list1.sort(key=lambda x: x[0])  # nach Länge sortiert
    list2.sort(key=lambda x: x[1])  # nach diff_angle sortiert
    # print(list1)
    # print(list2)
    try:
        limit = (list1[0][-1].limit).kmh
        way = list1[0][-1]
    except Exception:
        print(list1)
        limit = -1
        way = None
    return limit, (way)
