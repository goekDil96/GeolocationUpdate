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

from colimit import Connection as _Connection
from GeolocationUpdate.getconfig import get_config as _get_config


class work_on_server():
    def __init__(self, config):
        self.user = config["user"]
        self.password = config["password"]
        self.url = config["url"]
        self.port = config["port"]
        self.path_to_getlimit_file = config["path_to_getlimit_file"]

    def get_getlimit_code(self):
        r"""
        Print getlimit code.

        :return: string

        """
        result = False
        try:
            ci = _Connection(self.user, self.password, self.url, self.port)
            print(ci.get_limit_code)
            result = True
        except Exception as e:
            print(f"Error occured: {e}")
        return result

    def update_getlimit_code_to_server(self):
        r"""
        Update the getlimit code on clientside to serveride.

        :return: bool

        """
        result = False
        try:
            ci = _Connection(self.user, self.password, self.url, self.port)
            print(self.path_to_getlimit_file)
            ci.update_get_limit_code(self.path_to_getlimit_file)
            print(ci.get_limit_code)
            result = True
        except Exception as e:
            print(f"Error occured: {e}")
        return result

    def get_result_getlimit_server(self, lat=49.87342, lon=8.619549,
                                   rad=20., spd=10., dir=10., sec=1.):
        r"""
        Get the result for the getlimit function on the serverside.

        :param float lat: latitude
        :param float lon: longitude
        :param float rad: radius
        :param float dir: direction
        :param float sec: seconds
        :return: tuple

        """
        result = False
        try:
            ci = _Connection(self.user, self.password, self.url, self.port)
            result = ci.get_limit(latitude=lat,
                                  longitude=lon,
                                  speed=spd, 
                                  direction=dir,
                                  get_ways=ci.get_ways
                                  )
            print(f"Result ways: {result}")
        except Exception as e:
            print(f"Error occured: {e}")
        return result


def main():
    config = _get_config()
    geolocation = work_on_server(config=config)

    # geolocation.get_getlimit_code()
    geolocation.get_result_getlimit_server()
    # geolocation.update_getlimit_code_to_server()


if __name__ == "__main__":
    main()
