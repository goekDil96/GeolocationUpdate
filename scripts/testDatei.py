import sys
import os
import colimit
 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from colimit import Connection as _Connection, way
from GeolocationUpdate.getconfig import get_config
from GeolocationUpdate.getlimit import get_limit


config = get_config()
# filename = 'ecke.gpx'
# filename = 'dornheimerWeg_gerade.gpx'
# filename = "Fiedlersee_Ecke.gpx"
filename = "traubenweg_gerade.gpx"
# filename = 'ecken.gpx'
# filename = 'geraderWeg.gpx'
# filename = '15-Dez.-2021-1511.gpx'
# filename = "around_hda.gpx"

def read_gpx_file(filename):
    posLocation = colimit.testing.gpx(config["path_to_gpx"] + filename)
    return posLocation


def main():
    connect = _Connection(username=config["user"],
                          password=config["password"],
                          url=config["url"],
                          port=config["port"])

    pos_ways = connect.get_ways(latitude=47.644548,
                                longitude=-122.326897,
                                radius=20)
    
    # print(pos_ways)

    posLocation = read_gpx_file(filename)
    # print(posLocation)
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
        print(get_limit(latitude=lat,
                        longitude=lon,
                        speed=spd,
                        direction=dir,
                        get_ways=connect.get_ways))
        print("  ")




if __name__ == "__main__":
    main()
