# -*- coding: utf-8 -*-

# GeolocationUpdate
# -----------------
# Know your limits! (created by auxilium)
#
# Author:   Dilara Goeksu
# Version:  0.1, copyright Wednesday, 01 December 2021
# Website:  https://github.com/Dilara Goeksu/Geolocation
# License:  Apache License 2.0 (see LICENSE file)

import sys
import os
 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from GeolocationUpdate.getlimit import get_limit


class work_on_clientside():

    def get_result_getlimit_client(self, lat=49.870210, lon=8.632949,
                                   rad=20., spd=10., dir=10., sec=1.):
        r"""
        Get the result for the getlimit function on the clientside.

        :param float lat: latitude
        :param float lon: longitude
        :param float rad: radius
        :param float dir: direction
        :param float sec: seconds
        :return: tuple

        """
        result = False
        try:
            result = get_limit(latitude=lat, longitude=lon, speed=spd,
                               direction=dir, get_ways=None)
            print(f"Result ways: {result}")
        except Exception as e:
            print(f"Error occured: {e}")
        return result


def main():
    geolocation = work_on_clientside()
    geolocation.get_result_getlimit_client()

    


if __name__ == "__main__":
    main()
