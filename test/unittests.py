# -*- coding: utf-8 -*-

# auxilium
# --------
# A Python project for an automated test and deploy toolkit - 100%
# reusable.
#
# Author:   sonntagsgesicht
# Version:  0.1.4, copyright Sunday, 11 October 2020
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)

import sys
import os
from os import getcwd
from os.path import basename
from unittest import TestCase


from GeolocationUpdate.getconfig import get_config

config = get_config()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import colimit
from colimit import Connection as _Connection, way
from GeolocationUpdate.getlimit import getNearestPointToWay, getScattering
from GeolocationUpdate.getlimit import getDegreeDifference
from GeolocationUpdate.getlimit import getDirectionWay
from GeolocationUpdate.getlimit import getScatFromWayandLocation
from GeolocationUpdate.getlimit import get_limit

class getLimitTests(TestCase):
    def setUp(self):
        self.connect = _Connection(username=config["user"],
                          password=config["password"],
                          url=config["url"],
                          port=config["port"])

        self.pos_ways = self.connect.get_ways(latitude=47.644548,
                                longitude=-122.326897,
                                radius=20)
        
        self.point = colimit.location.Location(latitude=47.644548,
                                longitude=-122.326897,
                                direction=30)

    def test_getScattering(self):
        self.assertAlmostEqual(getScattering(1, 2, 3), 1.24721912892464)
    
    def test_getDegreeDifference(self):
        self.assertEqual(getDegreeDifference(180, 120), 60)
        self.assertEqual(getDegreeDifference(189, 19), 10)
        self.assertEqual(getDegreeDifference(269, 9), 80)
        self.assertEqual(getDegreeDifference(350, 10), 20)

    def test_getDirectionWay(self):
        self.assertAlmostEqual(getDirectionWay(self.pos_ways[0]), 359.6978098729106)

    def test_getNearestPointToWay(self):
        self.assertAlmostEqual(getNearestPointToWay(self.point, self.pos_ways[0])[0], 47.64449853808478)
        self.assertAlmostEqual(getNearestPointToWay(self.point, self.pos_ways[0])[1], -122.3268972608751)

    def test_getScatFromWayandLocation(self):
        self.assertAlmostEqual(getScatFromWayandLocation(self.pos_ways[0], self.point, 14.0), 42.99480443949462)
    
    def test_get_limit(self):
        self.assertEqual(get_limit(latitude=47.644548, speed=0,
                                longitude=-122.326897,
                                direction=30, get_ways=self.connect.get_ways)[0], 40.23353330889518)