from fileinput import filename
import sys
import os
import colimit

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from colimit import Connection as _Connection, way
from GeolocationUpdate.getconfig import get_config
from GeolocationUpdate.getlimit_einfach  import get_limit
from GeolocationUpdate.getlimit import get_limit as _get_limit


config = get_config()
# filename = "around_hda.gpx"
# filename = "bleichstraße.gpx"
filename = "ecken_arheilgen.gpx"
# filename = "geraderWeg.gpx"

def read_gpx_file(filename):
    posLocation = colimit.testing.gpx(config["path_to_gpx"] + filename)
    return posLocation


def main():
    connect = _Connection(username=config["user"],
                          password=config["password"],
                          url=config["url"],
                          port=config["port"])

    posLocation = read_gpx_file(filename)
    print(len(posLocation))
    for loc in posLocation:
        # print(waypoint.latitude)
        # print(waypoint.longitude)
        lat = loc.latitude
        lon = loc.longitude
        dir = loc.direction
        if loc.speed:
            spd = loc.speed
            # print(spd.mph)
        else:
            spd = 30
        print("///////////////////////////////")
        print("einfach: ", get_limit(latitude=lat,
                        longitude=lon,
                        speed=spd,
                        direction=dir,
                        get_ways=connect.get_ways)[0], get_limit(latitude=lat,
                        longitude=lon,
                        speed=spd,
                        direction=dir,
                        get_ways=connect.get_ways)[1][0:1])
        print("erweitertesModell: ", _get_limit(latitude=lat,
                        longitude=lon,
                        speed=spd,
                        direction=dir,
                        get_ways=connect.get_ways)[0], _get_limit(latitude=lat,
                        longitude=lon,
                        speed=spd,
                        direction=dir,
                        get_ways=connect.get_ways)[1][0:1])
        print(" ")




if __name__ == "__main__":
    main()
