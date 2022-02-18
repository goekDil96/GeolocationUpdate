# -*- coding: utf-8 -*-

# GeolocationUpdate
# -----------------
# Know your limits! (created by auxilium)
#
# Author:   Dilara Goeksu
# Version:  0.1, copyright Wednesday, 01 December 2021
# Website:  https://github.com/Dilara Goeksu/Geolocation
# License:  Apache License 2.0 (see LICENSE file)


import colimit.location

vorgaenger = None


def getNearestPointToWay(point, way):
    """
    Get nearest langitude and longitude from point object
    on way object.

    :param location point: location object
    :param way way: way object
    :returns: tuple

    """
    point1RV = way.geometry[0].coordinate
    point2RV = way.geometry[1].coordinate

    rV = (point2RV[0] - point1RV[0], point2RV[1] - point1RV[1])
    a = rV[0] * point.coordinate[0] + rV[1] * point.coordinate[1]

    newList = [(rV[0], point1RV[0]), (rV[1], point1RV[1])]

    b = sum([i * j for i, j in newList])
    m = sum([i ** 2 for i in rV])

    r = (a - b) / m
    xResult = point1RV[0] + r * rV[0]
    yResult = point1RV[1] + r * rV[1]

    return (xResult, yResult)


def getDegreeDifference(angle1, angle2):
    """
    Get difference between angle1 and angle2.

    :param float angle1: float
    :param float angle2: float
    :returns: float

    """
    degree = (angle1 - angle2) % 360
    if degree < 90:
        pass
    elif degree < 180:
        degree = 180 - degree
    elif degree < 270:
        degree = degree - 180
    else:
        degree = 360 - degree
    return degree


def getDirectionWay(way):
    """Returns direction (in Degree) from way object.

    :param way way: way object
    :returns: int

    """
    dirWay = colimit.location.Location.polar(way.geometry[0].coordinate[0],
                                             way.geometry[0].coordinate[1],
                                             way.geometry[1].coordinate[0],
                                             way.geometry[1].coordinate[1])
    return dirWay[1]


def getScattering(*a):
    """
    For every Element in tuple a, calculate scattering.

    :param tuple a: tuple
    :returns: float

    """
    result = 0
    for i in a:
        result += i ** 2
    result **= 1 / 2
    result /= len(a)
    return result


def getScatFromWayandLocation(way, pointSelf, directionSelf):
    """
    Get Scattering Value from way, location and
    direction.

    :param way way: way ocject
    :param location pointSelf: Location of user
    :param float directionSelf: degree to north from user
    :returns: float

    """
    # get distance from location to street
    nearPoint = getNearestPointToWay(pointSelf, way)
    nearPoint = colimit.location.Location(nearPoint[0], nearPoint[1])
    abstand = colimit.location.Location.dist(nearPoint, pointSelf)

    # get difference of direction (street) and direction (user)
    dirStr = getDirectionWay(way)

    degreeReturn = getDegreeDifference(dirStr, directionSelf)
    # get quality level
    qualityLevel = getScattering(0.75 * abstand, 0.25 * degreeReturn)
    return qualityLevel


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
    allWays = []
    resultList = []
    global vorgaenger

    # get own location as location object
    pointSelf = colimit.location.Location(latitude,
                                          longitude,
                                          speed,
                                          direction)

    directionP = (direction + 180) % 360

    pSelfPPP = colimit.location.Location.next(pointSelf,
                                              direction=directionP,
                                              radius=15
                                              )

    pSelfPP = colimit.location.Location.next(pointSelf,
                                             direction=directionP,
                                             radius=10
                                             )

    pSelfP = colimit.location.Location.next(pointSelf,
                                            direction=directionP,
                                            radius=5
                                            )

    pSelfF = colimit.location.Location.next(pointSelf,
                                            direction=direction,
                                            radius=5
                                            )

    pSelfFF = colimit.location.Location.next(pointSelf,
                                             direction=direction,
                                             radius=10,
                                             )

    pSelfFFF = colimit.location.Location.next(pointSelf,
                                              direction=direction,
                                              radius=15,
                                              )

    radius = [80, 150, 300]
    while len(allWays) == 0 and len(radius) != 0:
        rad = radius.pop(0)
        allWays = get_ways(latitude=latitude, longitude=longitude, radius=rad)
        if not vorgaenger:
            vorgaenger = allWays[0]
    for way in allWays:
        qualityLevelPPP = getScatFromWayandLocation(way, pSelfPPP, direction)
        qualityLevelPP = getScatFromWayandLocation(way, pSelfPP, direction)
        qualityLevelP = getScatFromWayandLocation(way, pSelfP, direction)
        qualityLevel = getScatFromWayandLocation(way, pointSelf, direction)
        qualityLevelF = getScatFromWayandLocation(way, pSelfF, direction)
        qualityLevelFF = getScatFromWayandLocation(way, pSelfFF, direction)
        qualityLevelFFF = getScatFromWayandLocation(way, pSelfFFF, direction)
        # print(qualityLevelF)

        qL = getScattering(qualityLevelPPP, qualityLevelPP, qualityLevelP,
                           qualityLevel, qualityLevelF, qualityLevelFF,
                           qualityLevelFFF)

        if way == vorgaenger:
            # print(qL)
            qL *= 0.5
            # pass

        # append tuple (qualityLevel, way) to resultList
        resultList.append([qL, way])

    # sort resultList from lowest qualityLevel value to highest
    resultList.sort(key=lambda x: x[0])
    # get Limit from resultList
    limit = resultList[0][-1].limit.kmh
    vorgaenger = resultList[0][-1]
    # get resultTuple from resultList
    resultTuple = []
    for i in resultList:
        resultTuple.append(i[-1])
    resultTuple = tuple(resultTuple)
    return limit, resultTuple
